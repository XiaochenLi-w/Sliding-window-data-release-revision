import numpy as np
import math

from mechanism.common_metrics import count_mre
from mechanism.data_process import data_reader

DEBUG = False
# dim = 1
# window_size = 100
# para_eps = 0.1
para_ratio = 0.075 * 2
para_windowPID = 5
USE_PERTURBED_NUMBER_TUPLES = True
SHARE_EPS_NO_TUPLES = 0.1
NO_TUPELS_n = 500000
OWN_EPS_1_FRACTION = 0.5
OWN_EPS_1 = True
THRESHOLD_T = 0.025
TOLERANCE_DELTA = 0.05
PROP_GAIN_THETA = 0.5
USE_NON_PRIVATE_SAMPLING = False
skipping_points_M = 2

def lap_arr(v, epsilon, sensitivity):
    tmp = np.random.laplace(loc=0,scale=sensitivity/epsilon)
    new_arr = []
    for i in range(len(v)):
        new_arr.append(v[i] + tmp)
    
    return new_arr


def avg_dissimilarity(last_published, org_stream_t, lambda_t, sensitivity):
    avg = 0
    # calculate dissimilarity
    for location in range(len(last_published)):
        
        avg += abs(last_published[location] - org_stream_t[location])
    
    avg /= len(last_published) # normalize by dimensionality

    if (USE_NON_PRIVATE_SAMPLING == False):
        avg += np.random.laplace(loc = 0, scale = sensitivity * lambda_t) # add noise
    
    return avg


def computeK(cuttoff_point_c, dimensionality_U, delta, no_time_points_N, no_tuples_n):
    # Theorem 5.4
    root1 = no_tuples_n * no_tuples_n
    root2 = (8 * delta * delta + 32 * cuttoff_point_c * cuttoff_point_c * delta * delta) / (dimensionality_U * cuttoff_point_c * cuttoff_point_c)
    root = round(math.pow(root1 * root2, 1.0 / 3.0))
    return min(root, 1 - cuttoff_point_c / no_time_points_N)

 

def dsat_workflow(epsilon, sensitivity, raw_stream, window_size, dim):

    # res = [[0 for j in range(dim)] for i in range(len(raw_stream))]

    publish_num = 0
    length_N = len(raw_stream)
    dimensionality_U = dim        
    CUTOFFPOINT_RATION = para_ratio # each time stamp in window
    sanitized_stream = []
    # ArrayList<double[]> sanitized_stream = new ArrayList<double[]>(length_N)
    delta = sensitivity * 2 / dimensionality_U # sensitivity L1 distance
    cuttoff_point_c = math.ceil(window_size * CUTOFFPOINT_RATION)  # in paper for user-level: length_N * 0.01 in paper

    used_budgets_eps_2 = [0 for i in range(length_N)]
    used_budgets_eps_1 = [0 for i in range(length_N)]
    samplingpoint = [0 for i in range(length_N)]

    # repair function
    no_tuples_n = 0
    eps_for_determining_n = 0
    reducedEpsFirstWindow = 0
    if (USE_PERTURBED_NUMBER_TUPLES):
        eps_for_determining_n = epsilon * SHARE_EPS_NO_TUPLES
        reducedEpsFirstWindow =eps_for_determining_n
        lambda_t = 1 / eps_for_determining_n

        sum = 0
        for ii in range(dim):
            sum += raw_stream[0][ii]

        san_sum = sum + np.random.laplace(loc = 0, scale = sensitivity * lambda_t)
        no_tuples_n = san_sum
        if (no_tuples_n == 0):
            no_tuples_n = NO_TUPELS_n
        
    else:
        no_tuples_n = NO_TUPELS_n
    

    k = computeK(cuttoff_point_c, dimensionality_U, delta, window_size, no_tuples_n) # before: length N instead of k


    eps_1_per_window_paper  = epsilon * k
    eps_1_per_window_paper_first  = (epsilon - reducedEpsFirstWindow) * k

    eps_1_per_window_own = epsilon * OWN_EPS_1_FRACTION
    eps_1_per_window_own_frist = (epsilon - reducedEpsFirstWindow) * OWN_EPS_1_FRACTION

    eps_1_per_window=0
    noisy_threshold=0
    eps_1_per_window_first=0
    # @SuppressWarnings("unused")
    noisy_threshold_first=0
    if (OWN_EPS_1):
        eps_1_per_window  =eps_1_per_window_own
        eps_1_per_window_first=eps_1_per_window_own_frist
        noisy_threshold = THRESHOLD_T + np.random.laplace(loc = 0, scale = 2 * delta / (eps_1_per_window_first/cuttoff_point_c))
        used_budgets_eps_1[0] = eps_1_per_window_first/cuttoff_point_c - eps_for_determining_n
    else:
        eps_1_per_window = eps_1_per_window_paper
        eps_1_per_window_first=eps_1_per_window_paper_first
        noisy_threshold = THRESHOLD_T + np.random.laplace(loc = 0, scale = 2 * delta / (eps_1_per_window_first/cuttoff_point_c))
        used_budgets_eps_1[0] = eps_1_per_window_first/cuttoff_point_c - eps_for_determining_n  
    

    eps_2_per_window = epsilon - eps_1_per_window  # for sanitizing
    eps_2_per_window_first = epsilon - eps_1_per_window_first # for sanitizing
    total_budget_spent_eps_2 = 0 # eps_1

    no_sampling_points_window = 0
    last_realize = []
    for t in range(length_N):
        org_stream_t = raw_stream[t]

        if (t <= window_size):
        # Algorithm 2
            if (t == 0):
                scale = 1 / (eps_2_per_window_first / cuttoff_point_c)
                last_realize = lap_arr(org_stream_t, 1 / scale, sensitivity=sensitivity)
                publish_num += 1
                sanitized_stream.append(last_realize)
                total_budget_spent_eps_2 += eps_2_per_window_first / cuttoff_point_c
                used_budgets_eps_2[t] = eps_2_per_window_first / cuttoff_point_c
                samplingpoint[t] = 1
                no_sampling_points_window += 1
            else:
                if (t <= skipping_points_M): # Line 2
                    sanitized_stream.append(last_realize)
                    samplingpoint[t] = False

                else:
                    # Line 4
                    if (no_sampling_points_window >= cuttoff_point_c): # ">=" is important due to line 47
                        sanitized_stream.append(last_realize)
                        samplingpoint[t] = 0
                    else: # cf. Algo 1 ("continue")
                        # Line 5
                        noisy_dist = avg_dissimilarity(org_stream_t, last_realize,
                                2 * cuttoff_point_c * delta / eps_1_per_window_first, sensitivity) # L1 distance
                        used_budgets_eps_1[t] = eps_1_per_window_first /cuttoff_point_c

                        # Line 6
                        feedback_error_E = abs(no_sampling_points_window / t - cuttoff_point_c / window_size) # use here already w instead of N
                        prop_e = abs(feedback_error_E - TOLERANCE_DELTA) / TOLERANCE_DELTA
                        prop_part_u = prop_e * PROP_GAIN_THETA
                        # Line 7+8: adapt threshold
                        if ((no_sampling_points_window / t - cuttoff_point_c / window_size) <= 0): # use here already w instead of N
                            noisy_threshold = max(0, noisy_threshold - prop_part_u)
                        else:
                            noisy_threshold = min(2, noisy_threshold + prop_part_u)
                        
                        # Line 9-12: decide whether to sample
                        if (noisy_dist >= noisy_threshold): # wir verschenken hier budget im ersten window, wenn wir nicht samplen, wegen zeile 94. man sollte hier auch mit eps_rm arbeiten?
                            # sample
                            last_realize = lap_arr(org_stream_t, (eps_2_per_window_first / cuttoff_point_c), sensitivity)
                            publish_num += 1
                            sanitized_stream.append(last_realize)
                            total_budget_spent_eps_2 += eps_2_per_window_first / cuttoff_point_c
                            no_sampling_points_window += 1
                            used_budgets_eps_2[t] = eps_2_per_window_first / cuttoff_point_c
                            samplingpoint[t] = 1

                        else:
                            sanitized_stream.append(last_realize)
                            samplingpoint[t] = 0
                        
                        # Line 14+15 -- should not happen in w event variant
                        if (t == length_N and no_sampling_points_window < cuttoff_point_c): # end of the time series
                            remaining_budget = eps_2_per_window_first - total_budget_spent_eps_2
                            last_realize = lap_arr(org_stream_t, (remaining_budget), sensitivity)
                            publish_num += 1
                            sanitized_stream.append(last_realize)
                            no_sampling_points_window += 1
                            used_budgets_eps_2[t] = remaining_budget
                            total_budget_spent_eps_2 = epsilon
                            samplingpoint[t] = 1

        else: # second window begins
            if (DEBUG):
                1
                # System.out.println(t-w-1 + " budget " + used_budgets_eps_2[t-w-1])
                # System.out.println(Arrays.toString(Arrays.copyOfRange(used_budgets_eps_2, t-w, t-1)))
            
            eps_spent = 0
            for ii in range(max(0, t - window_size), t):
                eps_spent += used_budgets_eps_2[ii]

            # eps_spent = Arrays.stream(Arrays.copyOfRange(used_budgets_eps_2, Math.max(0, t-w), t-1)).sum() # total_budget_spent_eps_2 - used_budgets_eps_2[t-w-1]
            eps_rm = eps_2_per_window - eps_spent
            # System.err.println("Use wrong eps_rm check!")
            if (eps_rm <= 0.00001): # rounding issues
                sanitized_stream.append(last_realize)
                samplingpoint[t] = False
            else:
                # line 7

                no_sampling_points_window = 0
                for ii in range(max(0, t - window_size), t):
                    if samplingpoint[ii] == 1:
                        no_sampling_points_window += 1
                # no_sampling_points_window = (int) Arrays.stream(Arrays.copyOfRange(samplingpoint, Math.max(0, t-w), t-1)).filter(x -> x.booleanValue()).count() # paper: (int) (total_budget_spent_eps_2/(eps_2_per_window / cuttoff_point_c)) //number publications current window
                # Line 8-11: -- analogous to above
                noisy_dist = avg_dissimilarity(org_stream_t, last_realize,
                        2 * cuttoff_point_c * delta / eps_1_per_window, sensitivity) # L1 distance
                # Line 6
                feedback_error_E = abs(no_sampling_points_window / t - cuttoff_point_c / window_size) # between target sampling rate and actual one
                prop_e = abs(feedback_error_E - TOLERANCE_DELTA) / TOLERANCE_DELTA
                prop_part_u = prop_e * PROP_GAIN_THETA
                # Line 7+8: adapt threshold
                if ((no_sampling_points_window / t - cuttoff_point_c / window_size) <= 0):
                    noisy_threshold = max(0, noisy_threshold - prop_part_u)
                else:
                    noisy_threshold = min(2, noisy_threshold + prop_part_u)
                
                # Line 9-12: decide whether to sample
                if (noisy_dist >= noisy_threshold):
                    # sample
                    last_realize = lap_arr(org_stream_t, (eps_2_per_window / cuttoff_point_c), sensitivity)
                    publish_num += 1
                    sanitized_stream.append(last_realize)
                    total_budget_spent_eps_2 += eps_2_per_window / cuttoff_point_c
                    used_budgets_eps_2[t] = eps_2_per_window / cuttoff_point_c
                    samplingpoint[t] = 1

                else:
                    sanitized_stream.append(last_realize)
                    samplingpoint[t] = 0

    return sanitized_stream


def run_dsat(epsilon, sensitivity, raw_stream, window_size, round_, Flag_ = 0):
    dim = len(raw_stream[0])
    MAE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            MAE_ = 0
            for r in range(round_):
                published_result = dsat_workflow(eps, sensitivity, raw_stream, window_size, dim)
                MAE_ += count_mre(raw_stream, published_result)
            
            MAE_ = MAE_ / round_
            print("epsilon:", eps, "Done!")
        
            MAE_list.append(MAE_)

        print('DSAT DONE!')

    else:
        for w in window_size:
            MAE_ = 0
            for r in range(round_):
                published_result = dsat_workflow(epsilon, sensitivity, raw_stream, w, dim)
                MAE_ += count_mre(raw_stream, published_result)
            
            MAE_ = MAE_ / round_
            print("window size:", w, "Done!")
        
            MAE_list.append(MAE_)

        print('DSAT DONE!')

    return MAE_list


if __name__ == "__main__":
    dataset_name = ["unemployment"]
    raw_stream = data_reader(dataset_name[0])
    epsilon = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    sensitivity_s = 1
    sensitivity_p = 1
    window_size = 100
    dim = 1
    round_ = 1
    
    error_ = run_dsat(epsilon, sensitivity_p, raw_stream, window_size, dim, round_)
    print(error_)
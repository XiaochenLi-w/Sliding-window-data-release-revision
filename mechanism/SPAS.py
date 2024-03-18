import numpy as np
from mechanism.common_metrics import count_mae
from mechanism.data_process import data_reader

# Add Laplace noise

def add_noise(sensitivity, eps, histo, dim):
    noisy_arr = []
    
    for i in range(dim):
        tmp = np.random.laplace(loc=0,scale=sensitivity/eps)
        noisy_arr.append(histo[i] + tmp)
        
    return noisy_arr

# Computer the distance between two histogram

def count_dis(histo_1, histo_2, dim):
    var_dis_sum = 0
    for i in range(dim):
        var_dis_sum += abs(histo_1[i]-histo_2[i])

    var_avgdis = var_dis_sum / dim

    return var_avgdis

# Computer the distance variance between two histogram

def count_vardis(histo_1, histo_2, dim):
    var_dis_sum = 0
    for i in range(dim):
        var_dis_sum += (histo_1[i]-histo_2[i]) ** 2

    var_avgdis = var_dis_sum / dim

    return var_avgdis

# Computer the average distance variance of a stream prefix

def agv_vardis(compute_num, window_size, published_stream, dim):
    length_ = len(published_stream)
    num_var = 0
    total_ = window_size * compute_num

    # only count the distance bwtween the sampled data
    count_ = 0
    
    if length_ >= total_ + 1:
        for i in range(total_ - 1):
            vardis = count_vardis(published_stream[length_ - 1 - i], published_stream[length_ - 2 - i], dim)
            if vardis > 0:
                num_var += vardis
                count_ += 1
        if count_ == 0:
            return 0
        else:
            return num_var / count_

    else:
        for i in range(length_ - 2):
            vardis = count_vardis(published_stream[length_ - 1 - i], published_stream[length_ - 2 - i], dim)
            if vardis > 0:
                num_var += vardis
                count_ += 1
        if count_ == 0:
            return 0
        else:
            return num_var / count_

# Update the optimal C
# epsilon_p: total privacy budegt in a sliding window
# sensitivity_p: sensitivity for adding noise to the released histogram
    
def update_optimalc(epsilon_p, sensitivity_p, compute_num, window_size, published_stream, dim):
    E_dis = agv_vardis(compute_num, window_size, published_stream, dim)

    #optimal_c = max(int(epsilon_p * np.sqrt(3 * E_dis) / (6 * sensitivity_p)), 1)
    theta_ = 1 / 2
    optimal_c = max(int((np.sqrt((1 - 2 * theta_)**2 * window_size**2 + (3 * theta_**2 * E_dis * epsilon_p**2) / sensitivity_p**2) - (1 - 2 * theta_) * window_size) / (6 * theta_)), 1)

    #test for using T to control svt
    # q = 10
    # optimal_c = max(int(epsilon_p * np.sqrt((theta_ * int(E_dis) + (1 - theta_) * q**2 * sensitivity_p**2) / (6 * (theta_ + 1))) / sensitivity_p), 1)

    return optimal_c

# Publish the data in the first window or first several windows

def warm_up_stage(epsilon, sensitivity_p, raw_stream, c_init, window_size, window_num, dim):
    c_init = int(epsilon * 15 + 5)
    sample_interval = int(window_size / c_init)
    total_for_warmup = window_size * window_num
    published_stream = []
    eps_consumed = []
    epsilon_warmup = epsilon / c_init

    for i in range(total_for_warmup):
        if i % sample_interval == 0:
            published_stream.append(add_noise(sensitivity_p, epsilon_warmup, raw_stream[i], dim))
            eps_consumed.append(epsilon_warmup)
        else:
            published_stream.append(published_stream[i - 1])
            eps_consumed.append(0)

    return published_stream, eps_consumed

# Compute the remaining epsilon at the last timestamp of a window

def compute_epsremain(epsilon_p, eps_consume, window_size):
    eps_con = 0
    length_ = len(eps_consume)

    for i in range(window_size - 1):
        eps_con += eps_consume[length_ - 1 - i]

    return epsilon_p - eps_con


# find the first sampled data in the current window
def find_firstsample(eps_con, window_size):
    current = len(eps_con)
    for i in range(current - window_size + 1, current):
        if eps_con[i] > 0:
            return i
    
    return current

# The whole workflow of SPAS

def SPAS_workflow(epsilon, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim):
    epsilon_s = epsilon / 4
    epsilon_p = epsilon - epsilon_s
    eps_1 = epsilon_s / 2
    eps_2 = epsilon_s - eps_1

    # warm_up stage
    published_stream, eps_consumed = warm_up_stage(epsilon, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, dim)

    optimal_c = update_optimalc(epsilon_p, sensitivity_p, windownum_updateE, window_size, published_stream, dim)

    # follow-up stage
    start_ = windownum_warm * window_size
    end_ = len(raw_stream)
    
    rho_ = add_noise(sensitivity_s / dim, eps_1, [0], 1)
    for i in range(start_, end_):
        diff = count_dis(raw_stream[i], raw_stream[i - 1], dim)
        v_ = add_noise(sensitivity_s / dim, eps_2 / (2 * optimal_c), [0], 1)
        eps_remain = compute_epsremain(epsilon_p, eps_consumed, window_size)
        T_ = optimal_c * sensitivity_p / epsilon_p
        #T_ = 10 * sensitivity_p
        
        first_sample_inwindow = find_firstsample(eps_consumed, window_size)
        if window_size - (i - first_sample_inwindow) <= int(eps_remain / (epsilon_p / optimal_c)):
            tmp = add_noise(sensitivity_p, epsilon_p / optimal_c + epsilon_s, raw_stream[i], dim)
            published_stream.append(tmp)
            eps_consumed.append(epsilon_p / optimal_c)

        elif diff + v_[0] > T_ + rho_[0] and eps_remain > (epsilon_p / optimal_c):
            tmp = add_noise(sensitivity_p, epsilon_p / optimal_c, raw_stream[i], dim)
            published_stream.append(tmp)
            eps_consumed.append(epsilon_p / optimal_c)

        else:
            published_stream.append(published_stream[i - 1])
            eps_consumed.append(0)
        
        optimal_c = update_optimalc(epsilon_p, sensitivity_p, windownum_updateE, window_size, published_stream, dim)
        #print(optimal_c)

    return published_stream

# Test the SPAS and compute the corresponding metrics
# Flag == 0, varying epsilon
# Flag ==1, varying window size

def run_SPAS(epsilon, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim, round_, Flag_ = 0):
    MAE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            MAE_ = 0
            for i in range(round_):
                published_result = SPAS_workflow(eps, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim)
                MAE_ += count_mae(raw_stream, published_result)

            MAE_ = MAE_ / round_
            print("epsilon:", eps, "Done!")
        
            MAE_list.append(MAE_)
        
        print('SPAS DONE!')

    else:
        for w in window_size:
            MAE_ = 0
            for i in range(round_):
                published_result = SPAS_workflow(epsilon, sensitivity_s, sensitivity_p, raw_stream, c_init, w, windownum_warm, windownum_updateE, dim)
                MAE_ += count_mae(raw_stream, published_result)

            MAE_ = MAE_ / round_
            print("window size:", w, "Done!")
        
            MAE_list.append(MAE_)
        
        print('SPAS DONE!')

    return MAE_list

if __name__ == "__main__":
    
    dataset_name = ["unemployment"]
    raw_stream = data_reader(dataset_name[0])
    epsilon = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    sensitivity_s = 1
    sensitivity_p = 1
    window_size = 100
    c_init = window_size / 5
    windownum_warm = 1
    windownum_updateE = 4
    dim = 1
    round_ = 1
    
    error_ = run_SPAS(epsilon, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim, round_)
    print(error_)
    
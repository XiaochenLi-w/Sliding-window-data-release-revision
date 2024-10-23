# from asyncio.windows_events import NULL
import numpy as np
import math
import sys
DEBUG = False
# para_d = 1
# para_w = 100
# para_eps = 0.5

from mechanism.common_metrics import count_mre, sum_query, count_query
from mechanism.data_process import data_reader



DEBUG_FORCE_NEW_GROUP_EACH_TIMESTAMP = False
DEBUG_ENABLE_DIMENSIONGROUPING = False
DEBUG_ENABLE_TIMEGROUPINGFILTER = True
    
def lap_arr(v, epsilon, sensitivity):
    tmp = np.random.laplace(loc=0,scale=sensitivity/epsilon)
    new_arr = []
    for i in range(len(v)):
        new_arr.append(v[i] + tmp)
    
    return new_arr

class Adapub:

    seed = 123456
    g = 20 # number of hash functions to use set as in paper (20)
    SHARE_EPS_P = 0.8 # as in paper
    SHARE_EPS_C = 0.2 # as in paper
    KP = 0.9 # as in paper
    KI = 0.1 # as in paper
    KD = 0.0 # as in paper
    GAMMA_FEEDBACK_ERROR = 1 # as in paper
    
    # rand = np.random()
    partition_buffer = []
    all_clusters = []

    newGrou = []

    def __init__(self, para_eps_, para_w_, para_d_, para_sen_):
        global para_eps, para_w, para_d, sensitivity
        para_eps = para_eps_
        para_w = para_w_
        para_d = para_d_
        sensitivity = para_sen_
        self.sensitivity = para_sen_
        self.epsilon = para_eps


    def run(self, org_stream):


        publish_num = 0
        length = len(org_stream)
        self.newGrou = [0 for i in range(length)]
        self.partition_buffer = [0 for i in range(self.g + 1)]
        eps_p = self.SHARE_EPS_P * self.epsilon
        eps_c = self.SHARE_EPS_C * self.epsilon
        if (DEBUG_ENABLE_TIMEGROUPINGFILTER == False):
            eps_p = self.epsilon
            eps_c = 0
        


        lambda_perturb = 1 / (eps_p / para_w) # venly distribute whole \epsilon to each time stamp in window
        # System.out.println("Lambda perturb: " + lambda_perturb)
        sanitized_stream = []
        san_t = []

        # t=0 is special and not considered in the paper: I cannot use a prior release for grouping.
        san_t = lap_arr(org_stream[0],  epsilon = 1 / lambda_perturb, sensitivity=self.sensitivity) # one time stamp sanitized as in uniform
        sanitized_stream.append(san_t)
        # init the clusters
        # all_clusters = [self.Cluster(self) for i in range(para_d)] # one cluster per dimension
        all_clusters = []
        for dim in range(para_d):
            all_clusters.append(self.Cluster(len(org_stream), dim, self)) # Also performs init with meaningful values
        

        for t in range(1, length): 
            # Group
            partions = {}

            if (DEBUG_ENABLE_DIMENSIONGROUPING == False):
                partions = self.get_dummy_partition(sanitized_stream[t - 1], self.g) # provide last release as argument
            else:
                partions = self.get_partition(sanitized_stream[t - 1], self.g) # provide last release as argument

            # Perturb individual dimensions exploiting the groups
            san_t = self.laplace_pertubation(partions, org_stream[t], lambda_perturb)
            # Smooth sanitized values
            if (DEBUG_ENABLE_TIMEGROUPINGFILTER):
                for dim in range(para_d):
                    all_clusters[dim].cluster(t, eps_c, org_stream, sanitized_stream, san_t)
                    san_t[dim] = all_clusters[dim].median_smoother(sanitized_stream, all_clusters[dim].current_group_begin_timestamp, t - 1, san_t[dim])
                    # if (Mechansim.TRUNCATE)
                    #     san_t[dim] = Mechansim.truncate(san_t[dim])
                
            
            sanitized_stream.append(san_t)
        
        partition_buffer = None

        return sanitized_stream
    

    def get_dummy_partition(self, last_release, g):
        groups = {} # {group_key,{dims}}

        for dim in range(len(last_release)):
            myGroup = []
            myGroup.append(dim)
            groups[dim] = myGroup


        
        return groups
    

    def get_partition(self, last_release, g):
        d = len(last_release) # dimensionality of the stream
        groups = {} # {group_key,{dims}}

        self.partition_buffer[0] = - sys.maxsize - 1


        max_count = 0
		
        max_count = max(last_release)
        min_count = min(last_release)

        for i in range(1, g + 1):
            pivot = 0
            if (min_count == max_count):
                pivot = min_count
            else:
                pivot = np.random.randint(min_count, max(1, max_count), 1) # must be > 0 ints() function returns only one, but needed to specify lower limit
            
            self.partition_buffer[i] = pivot # duplicates may occur according to the paper
        
        self.partition_buffer.sort(reverse = True) # I want the pivots to be sorted. self makes determining the partition simpler.

        # (2) Use the pivots for grouping
        for dim in range(d):
            old_release = last_release[dim]

            for p in range(len(self.partition_buffer)):
                group_key = self.partition_buffer[p]
                if (old_release > group_key): # Recap: pivots are orderer. So, its the first one to big.
                    my_group = groups[group_key]
                    if (my_group == None): # Group does not exist so far. Create it.
                        my_group = []
                        groups[group_key] = my_group
                    
                    my_group.append(dim)
                    break
                
            
        

        return groups
    
    def laplace_pertubation(self, groups, org_values, lambda_t):
        sant_t = [0 for i in range(len(org_values))] # first version of the sanitized timestamp data
        # for each partition

        for e in groups.keys():
            sum = 0.0

            # (1) Apply first filter exploiting that the values in the group have almost the same value, due to correlation.
            group = groups[e]
            group_size = len(group)
            for i in range(group_size):
                dim = group[i]
                sum += org_values[dim] # We compute a sum() query
            
            san_sum = sum + np.random.laplace(0, self.sensitivity * lambda_t) # self is the trick: we add the noise to the sum meaning that we reduce the noise by 1/|p|
            san_sum /= float(group_size)
            x_k_t = san_sum # value for partition p at time t

            # (2) create sanitized release values. Those values are smoothed shortly.
            for i in range(group_size):
                dim = group[i]
                sant_t[dim] = x_k_t
            
        
        return sant_t
    

    def dev(self, org_stream, t, dim, t_group_start):
        dev = 0
        average_count = 0

        for i in range(t_group_start, t + 1): # Including current value, i.e., <= t
            average_count += org_stream[i][dim]
        
        num_values = t - t_group_start + 1
        average_count /= num_values

        for i in range(t_group_start, t + 1): # Including current value, i.e., <= t
            dev += abs(org_stream[i][dim] - average_count)
        
        return dev
    
    def feedbackError(self, lastRelease, currentPerturbedValue):
        return abs(lastRelease - currentPerturbedValue) / max(currentPerturbedValue, self.GAMMA_FEEDBACK_ERROR)

    def pid_error(self, t, cluster, san_stream, intermediate_san_stream_t):

        feedbackError = self.feedbackError(san_stream[t - 1][cluster.my_dim], intermediate_san_stream_t[cluster.my_dim])
        cluster.feedback_errors[t] = feedbackError

        pidError = feedbackError * self.KP
        pidError += self.KI * cluster.feedback_error_integral(t)
        pidError += self.KD * (feedbackError - cluster.feedback_errors[t - 1]) / 1 # t-(t-1) is wrong in paper. however, we devide here by 1, as we do not sample.

        return pidError
    

    class Cluster:
        feedback_errors = []
        my_dim = 1
        current_group_begin_timestamp = 0
        is_closed = False

        # def __init__(self, obj):
        #     self.obj = obj

        def __init__(self, num_timestamps, dim, obj):
            self.current_group_begin_timestamp = 0
            self.is_closed = False
            self.feedback_errors = [0 for i in range(num_timestamps)]
            self.my_dim = dim
            self.obj = obj

        def cluster(self, t, eps_c, org_stream, san_stream, san_stream_t):
            theta = 0

            if (t == 0):
                theta = 1.0 / para_eps # never used nothing to group at first timestamp
            
            if (t > 0):
                delta_err_k_t = self.obj.pid_error(t, self, san_stream, san_stream_t)
                theta = max(1.0, delta_err_k_t * delta_err_k_t / para_eps) # In self approach the theta is not updated but entirely recomputed each time
                # pidError[t]=theta
            else:
                print("called grouper() at t=0")
            

            if (self.is_closed):
                self.current_group_begin_timestamp = t # open new group
                self.is_closed = False
                if (DEBUG_FORCE_NEW_GROUP_EACH_TIMESTAMP):
                    self.is_closed = True
                
                self.obj.newGrou[t] = 1

            else:
                # print(t, self.obj.newGrou)
                self.obj.newGrou[t] = 0

                dev = self.obj.dev(org_stream, t, self.my_dim, self.current_group_begin_timestamp)
                lamdba_dev = 2 * para_w / eps_c
                noisy_dev = max(dev + np.random.laplace(0,  sensitivity * lamdba_dev), 0)
                noisy_dev = theta + 1
                if (noisy_dev < theta):
                    1
                    # Nothing to do. The feedback error is added in any case above when computing the pid_error.
                else:
                    self.current_group_begin_timestamp = t # singular value group
                    self.is_closed = True
        
        def feedback_error_integral(self, t):
            num_timestamps = t - self.current_group_begin_timestamp # without t
            sum = 0.0
            for i in range(self.current_group_begin_timestamp, t):
                sum += self.feedback_errors[i]
            
            return sum / num_timestamps
        
        def median_smoother(self, san_stream, begin, end, san_t):
            sorted_sanStream_last_group = []
            sorted_sanStream_last_group.append(san_t)
            for i in range(begin, end + 1): # t has no valid san_stream yet
                sorted_sanStream_last_group.append(san_stream[i][self.my_dim])
            

            sorted_sanStream_last_group.sort()
            group_size = len(sorted_sanStream_last_group)
            median = 0

            if (group_size % 2 == 0):
                median = (sorted_sanStream_last_group[((int) (group_size / 2))] + sorted_sanStream_last_group[((int) (group_size / 2 - 1))]) / 2
            else:
                median = sorted_sanStream_last_group[((int) (group_size / 2))]
            
            return median
        
        
def diff_MAE(a1, a2):
    # print(len(a2))
    if len(a1) != len(a2):
        print("error")
        return
    
    sum = 0
    for i in range(len(a1)):
        sum_ts = 0
        for j in range(para_d):
            sum_ts = sum_ts + abs(a1[i][j] - a2[i][j]) ** 2
        
        sum += sum_ts ** (1 / 2)

    return sum


def run_adapub(epsilon, sensitivity, raw_stream, window_size, round_, Flag_ = 0):
    dim = len(raw_stream[0])
    MAE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            MAE_ = 0
            for r in range(round_):
                mech = Adapub(eps, window_size, dim, sensitivity)
                published_result = mech.run(raw_stream)
                MAE_ += count_mre(raw_stream, published_result)
            
            MAE_ = MAE_ / round_
            print("epsilon:", eps, "Done!")
        
            MAE_list.append(MAE_)

        print('Adapub DONE!')

    else:
        for w in window_size:
            MAE_ = 0
            for r in range(round_):
                mech = Adapub(epsilon, w, dim, sensitivity)
                published_result = mech.run(raw_stream)
                MAE_ += count_mre(raw_stream, published_result)
            
            MAE_ = MAE_ / round_
            print("window size:", w, "Done!")
        
            MAE_list.append(MAE_)

        print('Adapub DONE!')

    return MAE_list

def run_adapub_sum_query(epsilon, sensitivity, raw_stream, window_size, round_, query_num, Flag_ = 0):
    dim = len(raw_stream[0])
    query_MRE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            query_MRE = 0
            for r in range(round_):
                mech = Adapub(eps, window_size, dim, sensitivity)
                published_result = mech.run(raw_stream)
                query_MRE += sum_query(raw_stream, published_result, query_num)
            
            query_MRE = query_MRE / round_
            print("epsilon:", eps, "Done!")
        
            query_MRE_list.append(query_MRE)

        print('Adapub sum query DONE!')

    else:
        for w in window_size:
            query_MRE = 0
            for r in range(round_):
                mech = Adapub(epsilon, w, dim, sensitivity)
                published_result = mech.run(raw_stream)
                query_MRE += sum_query(raw_stream, published_result, query_num)
            
            query_MRE = query_MRE / round_
            print("window size:", w, "Done!")
        
            query_MRE_list.append(query_MRE)

        print('Adapub sum query DONE!')

    return query_MRE_list

def run_adapub_count_query(epsilon, sensitivity, raw_stream, window_size, round_, query_num, Flag_ = 0):
    dim = len(raw_stream[0])
    query_MRE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            query_MRE = 0
            for r in range(round_):
                mech = Adapub(eps, window_size, dim, sensitivity)
                published_result = mech.run(raw_stream)
                query_MRE += count_query(raw_stream, published_result, query_num)
            
            query_MRE = query_MRE / round_
            print("epsilon:", eps, "Done!")
        
            query_MRE_list.append(query_MRE)

        print('Adapub count query DONE!')

    else:
        for w in window_size:
            query_MRE = 0
            for r in range(round_):
                mech = Adapub(epsilon, w, dim, sensitivity)
                published_result = mech.run(raw_stream)
                query_MRE += count_query(raw_stream, published_result, query_num)
            
            query_MRE = query_MRE / round_
            print("window size:", w, "Done!")
        
            query_MRE_list.append(query_MRE)

        print('Adapub count query DONE!')

    return query_MRE_list
    

# if __name__ == "__main__":
#     # ex = []
#     UP = 10000
#     ex = [[int(UP / 2 * math.sin(i / 40 * 6.28) + UP / 2)] for i in range(1000)]
#     mech = Adapub()
#     adapub = mech.run(org_stream=ex)
#     uni_op = perturb_l(ex, para_eps / para_w)
#     print(diff_MAE(ex, adapub))
#     print(diff_MAE(ex, uni_op))

if __name__ == "__main__":

    raw_stream = data_reader('Uem')
    epsilon = [0.1, 0.3, 0.5, 0.7, 0.9]
    sensitivity_s = 1
    sensitivity_p = 1
    window_size = 100
    dim = 1
    round_ = 1
    
    # error_ = run_adapub(epsilon, sensitivity_p, raw_stream, window_size, dim, round_)
    # print(error_)
    sum_query_err = run_adapub_sum_query(epsilon, sensitivity_p, raw_stream, window_size, round_, 1000)
    print(sum_query_err)
import numpy as np
from mechanism.common_metrics import count_mre, sum_query, count_query
from mechanism.data_process import data_reader

# Add Laplace noise

def add_noise(sensitivity, eps, histo, dim):
    noisy_arr = []

    for i in range(dim):
        tmp = np.random.laplace(loc=0,scale=sensitivity/eps)
        noisy_arr.append(histo[i] + tmp)
        
    return noisy_arr

def uniform_workload(epsilon, sensitivity, raw_stream, window_size, dim):
    length_ = len(raw_stream)
    published_stream = []

    for i in range(length_):
        tmp = add_noise(sensitivity, epsilon / window_size, raw_stream[i], dim)
        published_stream.append(tmp)

    return published_stream

def run_uniform(epsilon, sensitivity, raw_stream, window_size, round_, Flag_ = 0):
    dim = len(raw_stream[0])
    MAE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            MAE_ = 0
            for i in range(round_):
                published_result = uniform_workload(eps, sensitivity, raw_stream, window_size, dim)
                MAE_ += count_mre(raw_stream, published_result)

            MAE_ = MAE_ / round_
            print("epsilon:", eps, "Done!")
        
            MAE_list.append(MAE_)

        print('uniform DONE!')

    else:
        for w in window_size:
            MAE_ = 0
            for i in range(round_):
                published_result = uniform_workload(epsilon, sensitivity, raw_stream, w, dim)
                MAE_ += count_mre(raw_stream, published_result)

            MAE_ = MAE_ / round_
            print("window size:", w, "Done!")
        
            MAE_list.append(MAE_)

        print('uniform DONE!')

    return MAE_list

def run_uniform_sum_query(epsilon, sensitivity, raw_stream, window_size, round_, query_num, Flag_ = 0):
    dim = len(raw_stream[0])
    query_MRE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            query_MRE = 0
            for i in range(round_):
                published_result = uniform_workload(eps, sensitivity, raw_stream, window_size, dim)
                query_MRE += sum_query(raw_stream, published_result, query_num)

            query_MRE = query_MRE / round_
            print("epsilon:", eps, "Done!")
        
            query_MRE_list.append(query_MRE)

        print('uniform sum query DONE!')

    else:
        for w in window_size:
            query_MRE = 0
            for i in range(round_):
                published_result = uniform_workload(epsilon, sensitivity, raw_stream, w, dim)
                query_MRE += sum_query(raw_stream, published_result, query_num)

            query_MRE = query_MRE / round_
            print("window size:", w, "Done!")
        
            query_MRE_list.append(query_MRE)

        print('uniform sum query DONE!')

    return query_MRE_list

def run_uniform_count_query(epsilon, sensitivity, raw_stream, window_size, round_, query_num, Flag_ = 0):
    dim = len(raw_stream[0])
    query_MRE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            query_MRE = 0
            for i in range(round_):
                published_result = uniform_workload(eps, sensitivity, raw_stream, window_size, dim)
                query_MRE += count_query(raw_stream, published_result, query_num)

            query_MRE = query_MRE / round_
            print("epsilon:", eps, "Done!")
        
            query_MRE_list.append(query_MRE)

        print('uniform count query DONE!')

    else:
        for w in window_size:
            query_MRE = 0
            for i in range(round_):
                published_result = uniform_workload(epsilon, sensitivity, raw_stream, w, dim)
                query_MRE += count_query(raw_stream, published_result, query_num)

            query_MRE = query_MRE / round_
            print("window size:", w, "Done!")
        
            query_MRE_list.append(query_MRE)

        print('uniform count query DONE!')

    return query_MRE_list

if __name__ == "__main__":
    
    raw_stream = data_reader('Uem')
    epsilon = [0.1, 0.3, 0.5, 0.7, 0.9]
    sensitivity = 1
    window_size = 100
    round_ = 1
    
    # error_ = run_uniform(epsilon, sensitivity, raw_stream, window_size, round_)
    # print(error_)
    sum_query_err = run_uniform_sum_query(epsilon, sensitivity, raw_stream, window_size, round_, 1000)
    print(sum_query_err)
    
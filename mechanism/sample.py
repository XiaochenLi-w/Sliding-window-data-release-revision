import numpy as np
from mechanism.common_metrics import count_mre
from mechanism.data_process import data_reader

# Add Laplace noise

def add_noise(sensitivity, eps, histo, dim):
    noisy_arr = []

    for i in range(dim):
        tmp = np.random.laplace(loc=0,scale=sensitivity/eps)
        noisy_arr.append(histo[i] + tmp)
        
    return noisy_arr

def sample_workload(epsilon, sensitivity, raw_stream, window_size, dim):
    length_ = len(raw_stream)
    published_stream = []

    for i in range(length_):
        if i % int(window_size) == 0:
            tmp = add_noise(sensitivity, epsilon, raw_stream[i], dim)
            published_stream.append(tmp)
        else:
            published_stream.append(published_stream[i - 1])
        
    return published_stream

def run_sample(epsilon, sensitivity, raw_stream, window_size, dim, round_, Flag_ = 0):
    MAE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            MAE_ = 0
            for i in range(round_):
                published_result = sample_workload(eps, sensitivity, raw_stream, window_size, dim)
                MAE_ += count_mre(raw_stream, published_result)

            MAE_ = MAE_ / round_
            print("epsilon:", eps, "Done!")
        
            MAE_list.append(MAE_)

        print('Sample DONE!')

    else:
        for w in window_size:
            MAE_ = 0
            for i in range(round_):
                published_result = sample_workload(epsilon, sensitivity, raw_stream, w, dim)
                MAE_ += count_mre(raw_stream, published_result)

            MAE_ = MAE_ / round_
            print("window size:", w, "Done!")
        
            MAE_list.append(MAE_)

        print('Sample DONE!')

    return MAE_list

if __name__ == "__main__":
    
    dataset_name = ["unemployment"]
    raw_stream = data_reader(dataset_name[0])
    epsilon = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    sensitivity = 1
    window_size = 100
    dim = 1
    round_ = 1
    
    error_ = run_sample(epsilon, sensitivity, raw_stream, window_size, dim, round_)
    print(error_)
    
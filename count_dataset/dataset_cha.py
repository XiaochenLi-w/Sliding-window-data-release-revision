import numpy as np

import mechanism.data_process

def count_dis(histo_1, histo_2, dim):
    dis_sum = 0
    for i in range(dim):
        dis_sum += abs(histo_1[i]-histo_2[i])

    avgdis = dis_sum / dim

    return avgdis

def count_rdis(histo_1, histo_2, dim):
    dis_sum = 0
    for i in range(dim):
        if histo_1[i] > 0:
            dis_sum += abs(histo_1[i]-histo_2[i]) / histo_1[i]
        else:
            dis_sum += abs(histo_1[i]-histo_2[i])

    avgdis = dis_sum / dim

    return avgdis

def count_vardis(histo_1, histo_2, dim):
    dis_sum = 0
    for i in range(dim):
        dis_sum += abs(histo_1[i]-histo_2[i])**2

    avgdis = dis_sum / dim

    return avgdis

def count_charac():
    datasets_list = ["F1d", "Dth", "Uem", "Fmd", "Tdv", "Tpt", "Ret", "syn_uniform", "syn_mix"]
    dataset_num = len(datasets_list)
    change_ = np.zeros(dataset_num, dtype=float)
    
    for i, dataset in enumerate(datasets_list):
        raw_stream = mechanism.data_process.data_reader(dataset)
        dim = len(raw_stream[0])
        length_ = len(raw_stream)
        for j in range(1, length_):
            change_[i] += count_rdis(raw_stream[j], raw_stream[j - 1], dim)
        change_[i] = change_[i] / length_

    return change_


def count_varcharac():
    datasets_list = ["F1d", "Dth", "Uem", "Fmd", "Tdv", "Tpt", "Ret", "syn_uniform", "syn_mix"]
    dataset_num = len(datasets_list)
    change_ = np.zeros(dataset_num, dtype=float)
    epsilon = 0.1
    
    for i, dataset in enumerate(datasets_list):
        raw_stream = mechanism.data_process.data_reader(dataset)
        print(dataset, len(raw_stream[0]))
        dim = len(raw_stream[0])
        length_ = len(raw_stream)
        for j in range(1, length_):
            change_[i] += count_vardis(raw_stream[j], raw_stream[j - 1], dim)
        change_[i] = change_[i] / length_
        change_[i] = change_[i] * epsilon**2 / 12

    return change_


def count_eachwindoweps():
    datasets_list = ["F1d", "Dth", "Uem",  "syn_uniform", "syn_mix", "Fmd", "Tdv", "syn_multi", "Ret"]
    window_size = 120
    epsilon = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    var_lap = np.zeros(len(epsilon), dtype=float)
    for i in range(len(epsilon)):
        var_lap[i] = 2 * (window_size / epsilon[i])**2

    for q, dataset in enumerate(datasets_list):
        raw_stream = mechanism.data_process.data_reader(dataset)
        dim = len(raw_stream[0])
        length_ = len(raw_stream)
        i = 0
        sum_ = 0
        c_ = 0
        while i <  (length_ - window_size):
            tmp = 0
            for j in range(i, i + window_size):
                tmp += count_dis(raw_stream[j], raw_stream[j - 1], dim)

            c_ += 1
            sum_ += tmp
            i += window_size
        
        avg_sum = sum_ / c_
        ratio_ = np.zeros(len(epsilon), dtype=float)
        for k in range(len(epsilon)):
            ratio_[k] = avg_sum / var_lap[k]


        print(dataset, ": [", end='')
        for j in range(len(epsilon)):
            print(ratio_[j], ",", end='')
        print("]")


def count_eachwindoww():
    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix", "Fmd", "Tdv", "syn_multi", "Ret"]
    epsilon = 0.1
    window_size = [40, 80, 120, 160, 200]
    
    var_lap = np.zeros(len(window_size), dtype=float)
    for i in range(len(window_size)):
        var_lap[i] = 2 * (window_size[i] / epsilon)**2
    
    ratio_ = np.zeros([len(window_size), len(datasets_list)], dtype=float)
    for k in range(len(window_size)):
        for q, dataset in enumerate(datasets_list):
            raw_stream = mechanism.data_process.data_reader(dataset)
            dim = len(raw_stream[0])
            length_ = len(raw_stream)      
            i = 0
            sum_ = 0
            c_ = 0
            while i <  (length_ - window_size[k]):
                tmp = 0
                for j in range(i, i + window_size[k]):
                    tmp += count_dis(raw_stream[j], raw_stream[j - 1], dim)

                c_ += 1
                sum_ += tmp
                i += window_size[k]
            
            avg_sum = sum_ / c_
            
            ratio_[k][q] = avg_sum / var_lap[k]

    
    ratio_ = ratio_.T
    for i, dataset in enumerate(datasets_list):
        print(dataset, ": [", end='')
        for j in range(len(window_size)):
            print(ratio_[i][j], ",", end='')
        print("]")



if __name__ == "__main__":

    #print(count_charac())
    #print(count_varcharac())
    count_eachwindoww()


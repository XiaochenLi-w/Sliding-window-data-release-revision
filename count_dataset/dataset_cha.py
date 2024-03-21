import numpy as np

import mechanism.data_process

def count_dis(histo_1, histo_2, dim):
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
            change_[i] += count_dis(raw_stream[j], raw_stream[j - 1], dim)
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

if __name__ == "__main__":

    #print(count_charac())
    print(count_varcharac())


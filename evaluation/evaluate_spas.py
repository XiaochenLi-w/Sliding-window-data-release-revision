import mechanism.SPAS
import mechanism.uniform
import mechanism.sample
import mechanism.fast_w_event
import mechanism.dsat
import mechanism.bd
import mechanism.adapub
import mechanism.pegasus
import mechanism.common_metrics
import mechanism.data_process
import run_def
import pickle

import matplotlib.pyplot as plt


# run all methods with varying epsilon
    
def run_evalu_spas(epsilon_list, sensitivity_s, sensitivity_p, window_size, windownum_warm, windownum_updateE, round_):
    methods_list = ['spas']
    #datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix", "Fmd", "Tdv", "syn_multi", "Ret"]
    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix"]
    #datasets_list = ["Fmd", "Tdv", "syn_multi", "Ret"]

    err_all = []
    for i in range(len(datasets_list)):
        err_all.append([])
        for j in range(len(epsilon_list)):
            err_all[i].append([])

    for i, dataset_name in enumerate(datasets_list):    
        raw_stream = run_def.run_dataset(dataset_name)
        for j, method_name in enumerate(methods_list):
            err_tmp = run_def.run_method(method_name, epsilon_list, sensitivity_s, sensitivity_p, raw_stream, window_size, windownum_warm, windownum_updateE, round_)
            print(dataset_name, ":", err_tmp)
            err_all[i][j] = err_tmp
        print('********dataset', datasets_list[i], 'Done!********')

    print(err_all)


if __name__ == "__main__":
    
    epsilon_list = [1]
    sensitivity_s = 1
    sensitivity_p = 1

    window_size = 120
 
    windownum_warm = 1
    windownum_updateE = 2
    round_ = 5

    run_evalu_spas(epsilon_list, sensitivity_s, sensitivity_p, window_size, windownum_warm, windownum_updateE, round_)
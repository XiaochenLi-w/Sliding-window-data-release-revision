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

def run_all_sum_query(epsilon_list, sensitivity_s, sensitivity_p, window_size, windownum_warm, windownum_updateE, round_, query_num):
    methods_list = ['spas', 'sample', 'uniform', 'dsat', 'fast', 'bd', 'adapub', 'pegasus']
    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix"]
    # only 1-dimensional datasets are included

    err_all = []
    for i in range(len(datasets_list)):
        err_all.append([])
        for j in range(len(epsilon_list)):
            err_all[i].append([])

    for i, dataset_name in enumerate(datasets_list):    
        raw_stream = run_def.run_dataset(dataset_name)
        for j, method_name in enumerate(methods_list):
            err_tmp = run_def.run_method_sum_query(method_name, epsilon_list, sensitivity_s, sensitivity_p, raw_stream, window_size, windownum_warm, windownum_updateE, round_, query_num)
            for k in range(len(epsilon_list)):
                err_all[i][k].append(err_tmp[k])
        print('********dataset', datasets_list[i], 'Done!********')
    
    with open("./output/" + "error_eps_sum_query.pickle", "wb") as f:
        pickle.dump(err_all, f)

    print(err_all)
    
def runw_all_sum_query(epsilon, sensitivity_s, sensitivity_p, window_size_list, windownum_warm, windownum_updateE, round_, query_num):
    methods_list = ['spas', 'sample', 'uniform', 'dsat', 'fast', 'bd', 'adapub', 'pegasus']
    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix"]

    err_all = []
    for i in range(len(datasets_list)):
        err_all.append([])
        for j in range(len(window_size_list)):
            err_all[i].append([])

    for i, dataset_name in enumerate(datasets_list):    
        raw_stream = run_def.run_dataset(dataset_name)
        for j, method_name in enumerate(methods_list):
            # set Flag_ = 1 means varying window size, the default is 0
            err_tmp = run_def.run_method_sum_query(method_name, epsilon, sensitivity_s, sensitivity_p, raw_stream, window_size_list, windownum_warm, windownum_updateE, round_, query_num, 1)
            for k in range(len(window_size_list)):
                err_all[i][k].append(err_tmp[k])
        print('********dataset', datasets_list[i], 'Done!********')
    
    with open("./output/" + "error_w_sum_query.pickle", "wb") as f:
        pickle.dump(err_all, f)

    print(err_all)
    
def run_all_count_query(epsilon_list, sensitivity_s, sensitivity_p, window_size, windownum_warm, windownum_updateE, round_, query_num):
    methods_list = ['spas', 'sample', 'uniform', 'dsat', 'fast', 'bd', 'adapub', 'pegasus']
    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix"]
    # only 1-dimensional datasets are included

    err_all = []
    for i in range(len(datasets_list)):
        err_all.append([])
        for j in range(len(epsilon_list)):
            err_all[i].append([])

    for i, dataset_name in enumerate(datasets_list):    
        raw_stream = run_def.run_dataset(dataset_name)
        for j, method_name in enumerate(methods_list):
            err_tmp = run_def.run_method_count_query(method_name, epsilon_list, sensitivity_s, sensitivity_p, raw_stream, window_size, windownum_warm, windownum_updateE, round_, query_num)
            for k in range(len(epsilon_list)):
                err_all[i][k].append(err_tmp[k])
        print('********dataset', datasets_list[i], 'Done!********')
    
    with open("./output/24.7.9/" + "error_eps_count_query.pickle", "wb") as f:
        pickle.dump(err_all, f)

    print(err_all)
    
def runw_all_count_query(epsilon, sensitivity_s, sensitivity_p, window_size_list, windownum_warm, windownum_updateE, round_, query_num):
    methods_list = ['spas', 'sample', 'uniform', 'dsat', 'fast', 'bd', 'adapub', 'pegasus']
    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix"]

    err_all = []
    for i in range(len(datasets_list)):
        err_all.append([])
        for j in range(len(window_size_list)):
            err_all[i].append([])

    for i, dataset_name in enumerate(datasets_list):    
        raw_stream = run_def.run_dataset(dataset_name)
        for j, method_name in enumerate(methods_list):
            # set Flag_ = 1 means varying window size, the default is 0
            err_tmp = run_def.run_method_count_query(method_name, epsilon, sensitivity_s, sensitivity_p, raw_stream, window_size_list, windownum_warm, windownum_updateE, round_, query_num, 1)
            for k in range(len(window_size_list)):
                err_all[i][k].append(err_tmp[k])
        print('********dataset', datasets_list[i], 'Done!********')
    
    with open("./output/24.7.9/" + "error_w_count_query.pickle", "wb") as f:
        pickle.dump(err_all, f)

    print(err_all)
    
if __name__ == "__main__":
    
    sensitivity_s = 1
    sensitivity_p = 1
    #### For varying epsilon #####
    # epsilon_list = [0.1, 0.3, 0.5, 0.7, 0.9]
    # window_size = 120
    ##############

    #### For varying window size ####
    epsilon = 1
    window_size_list = [40, 80, 120, 160, 200]
    ##############
    windownum_warm = 1
    windownum_updateE = 2
    round_ = 5
    query_num = 1000

    # run_all_sum_query(epsilon_list, sensitivity_s, sensitivity_p, window_size, windownum_warm, windownum_updateE, round_, query_num)
    #run_all_count_query(epsilon_list, sensitivity_s, sensitivity_p, window_size, windownum_warm, windownum_updateE, round_, query_num)
    #runw_all_sum_query(epsilon, sensitivity_s, sensitivity_p, window_size_list, windownum_warm, windownum_updateE, round_, query_num)
    runw_all_count_query(epsilon, sensitivity_s, sensitivity_p, window_size_list, windownum_warm, windownum_updateE, round_, query_num)
    
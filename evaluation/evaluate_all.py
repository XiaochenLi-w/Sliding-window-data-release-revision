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

def run_all(epsilon_list, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim, round_):
    error_spas = mechanism.SPAS.run_SPAS(epsilon_list, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim, round_)
    error_uniform = mechanism.uniform.run_uniform(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)
    error_sample = mechanism.sample.run_sample(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)
    error_fast = mechanism.fast_w_event.run_fast(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)
    error_dsat = mechanism.dsat.run_dsat(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)
    error_bd = mechanism.bd.run_bd(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)
    error_adapub = mechanism.adapub.run_adapub(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)
    error_pegasus = mechanism.pegasus.run_pegasus(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)
    

    print('spas:', error_spas)
    print('uniform:', error_uniform)
    print('sample:', error_sample)
    print('fast:', error_fast)
    print('dsat', error_dsat)
    print('bd', error_bd)
    print('adapub', error_adapub)
    print('pegasus', error_pegasus)

    plt.plot(epsilon_list, error_spas, label='SPAS')
    plt.plot(epsilon_list, error_uniform, label='Uniform')
    plt.plot(epsilon_list, error_sample, label='Sample')
    plt.plot(epsilon_list, error_fast, label='FAST')
    plt.plot(epsilon_list, error_dsat, label='DSAT')
    #plt.plot(epsilon_list, error_bd, label='BD')
    plt.plot(epsilon_list, error_adapub, label='AdaPub')
    plt.plot(epsilon_list, error_pegasus, label='PeGaSus')


    plt.legend()
    plt.show()


# run all methods with varying epsilon
    
def run_allfix(epsilon_list, sensitivity_s, sensitivity_p, c_init, window_size, windownum_warm, windownum_updateE, round_):
    methods_list = ['spas', 'sample', 'uniform', 'dsat', 'fast', 'bd', 'adapub', 'pegasus']
    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix", "Fmd", "Tdv", "Tpt", "Ret"]

    err_all = []
    for i in range(len(datasets_list)):
        err_all.append([])
        for j in range(len(epsilon_list)):
            err_all[i].append([])

    for i, dataset_name in enumerate(datasets_list):    
        raw_stream = run_def.run_dataset(dataset_name)
        for j, method_name in enumerate(methods_list):
            err_tmp = run_def.run_method(method_name, epsilon_list, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, round_)
            for k in range(len(epsilon_list)):
                err_all[i][k].append(err_tmp[k])
        print('********dataset', datasets_list[i], 'Done!********')
    
    with open("./output/" + "error4.pickle", "wb") as f:
        pickle.dump(err_all, f)

    print(err_all)

# Only update part of results recorded in error.pickle

def run_part(epsilon_list, sensitivity_s, sensitivity_p, c_init, window_size, windownum_warm, windownum_updateE, round_):
    methods_list = ['spas', 'sample', 'uniform', 'dsat', 'fast', 'bd', 'adapub', 'pegasus']
    datasets_list = ["Fmd", "Tdv", "Tpt", "Ret"]
    methods_num = [0, 1, 2, 3, 4, 5, 6, 7]
    dataset_num = [5, 6, 7, 8]
    

    with open("./output/error_eps.pickle", "rb") as f:
        err_all = pickle.load(f)
    

    for i, dataset_name in enumerate(datasets_list):    
        raw_stream = run_def.run_dataset(dataset_name)
        if dataset_num[i] > len(err_all) - 1:
            err_all.append([])
            for qq in range(len(epsilon_list)):
                err_all[dataset_num[i]].append([])
                for pp in range(len(methods_list)):
                    err_all[dataset_num[i]][qq].append(0)

        for j, method_name in enumerate(methods_list):
            err_tmp = run_def.run_method(method_name, epsilon_list, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, round_)
            for k in range(len(epsilon_list)):
                err_all[dataset_num[i]][k][methods_num[j]] = err_tmp[k]
        print('********dataset', datasets_list[i], 'Done!********')
    
    with open("./output/" + "error1.pickle", "wb") as f:
        pickle.dump(err_all, f)

    print(err_all)


# run all methods with varying window size
    
def runw_allfix(epsilon, sensitivity_s, sensitivity_p, c_init, window_size_list, windownum_warm, windownum_updateE, round_):
    methods_list = ['spas', 'sample', 'uniform', 'dsat', 'fast', 'bd', 'adapub', 'pegasus']
    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix", "Fmd", "Tdv", "Tpt", "Ret"]

    err_all = []
    for i in range(len(datasets_list)):
        err_all.append([])
        for j in range(len(window_size_list)):
            err_all[i].append([])

    for i, dataset_name in enumerate(datasets_list):    
        raw_stream = run_def.run_dataset(dataset_name)
        for j, method_name in enumerate(methods_list):
            # set Flag_ = 1 means varying window size, the default is 0
            err_tmp = run_def.run_method(method_name, epsilon, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size_list, windownum_warm, windownum_updateE, round_, 1)
            for k in range(len(window_size_list)):
                err_all[i][k].append(err_tmp[k])
        print('********dataset', datasets_list[i], 'Done!********')
    
    with open("./output/" + "error5.pickle", "wb") as f:
        pickle.dump(err_all, f)

    print(err_all)


# Only update part of results recorded in error.pickle
    
def runw_part(epsilon, sensitivity_s, sensitivity_p, c_init, window_size_list, windownum_warm, windownum_updateE, round_):
    methods_list = ['pegasus']
    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix", "Fmd", "Tdv", "Tpt", "Ret"]
    methods_num = [7]
    dataset_num = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    with open("./output/error5.pickle", "rb") as f:
        err_all = pickle.load(f)
    

    for i, dataset_name in enumerate(datasets_list):    
        raw_stream = run_def.run_dataset(dataset_name)
        if dataset_num[i] > len(err_all) - 1:
            err_all.append([])
            for qq in range(len(window_size_list)):
                err_all[dataset_num[i]].append([])
                for pp in range(len(methods_list)):
                    err_all[dataset_num[i]][qq].append(0)

        for j, method_name in enumerate(methods_list):
            err_tmp = run_def.run_method(method_name, epsilon, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size_list, windownum_warm, windownum_updateE, round_, 1)
            for k in range(len(window_size_list)):
                err_all[dataset_num[i]][k][methods_num[j]] = err_tmp[k]
        print('********dataset', datasets_list[i], 'Done!********')
    
    with open("./output/" + "error7.pickle", "wb") as f:
        pickle.dump(err_all, f)

    print(err_all)

if __name__ == "__main__":
    
    epsilon_list = [0.1, 0.3, 0.5, 0.7, 0.9]
    sensitivity_s = 1
    sensitivity_p = 1
    #### For varying epsilon #####
    window_size = 120
    c_init = window_size / 20
    ##############
    
    #### For varying window size ####
    # epsilon = 0.1
    # window_size_list = [40, 80, 120, 160, 200]
    # c_init = 20
    ##############
    windownum_warm = 1
    windownum_updateE = 2
    round_ = 5

    #run_all(epsilon_list, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim, round_)
    run_part(epsilon_list, sensitivity_s, sensitivity_p, c_init, window_size, windownum_warm, windownum_updateE, round_)
    #runw_part(epsilon, sensitivity_s, sensitivity_p, c_init, window_size_list, windownum_warm, windownum_updateE, dim, round_)
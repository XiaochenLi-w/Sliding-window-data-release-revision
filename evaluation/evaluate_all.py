import mechanism.SPAS
import mechanism.uniform
import mechanism.sample
import mechanism.fast_w_event
import mechanism.common_metrics
import mechanism.data_process

import matplotlib.pyplot as plt

def run_all(epsilon_list, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim, round_):
    error_spas = mechanism.SPAS.run_SPAS(epsilon_list, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim, round_)
    error_uniform = mechanism.uniform.run_uniform(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)
    error_sample = mechanism.sample.run_sample(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)
    error_fast = mechanism.fast_w_event.run_fast(epsilon_list, sensitivity_p, raw_stream, window_size, dim, round_)

    print('spas:', error_spas)
    print('uniform:', error_uniform)
    print('sample:', error_sample)
    print('fast:', error_fast)

    plt.plot(epsilon_list, error_spas, label='SPAS')
    plt.plot(epsilon_list, error_uniform, label='Uniform')
    plt.plot(epsilon_list, error_sample, label='Sample')
    plt.plot(epsilon_list, error_fast, label='FAST')


    plt.legend()
    plt.show()

if __name__ == "__main__":
    
    #dataset_name = ["unemployment"]
    #dataset_name = ["syn_uniform"]
    #dataset_name = ["syn_gauss"]
    dataset_name = ["syn_mix"]
    raw_stream = mechanism.data_process.data_reader(dataset_name[0])
    #epsilon_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    epsilon_list = [0.1, 0.3, 0.5, 0.7, 0.9]
    sensitivity_s = 1
    sensitivity_p = 1
    window_size = 200
    c_init = window_size / 10
    windownum_warm = 1
    windownum_updateE = 3
    dim = 1
    round_ = 10

    run_all(epsilon_list, sensitivity_s, sensitivity_p, raw_stream, c_init, window_size, windownum_warm, windownum_updateE, dim, round_)

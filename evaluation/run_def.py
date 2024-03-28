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

def run_method(method_name, epsilon_list, sensitivity_s, sensitivity_p, raw_stream, window_size, windownum_warm, windownum_updateE, round_, Flag_ = 0):
    if method_name == "spas":
        error_ = mechanism.SPAS.run_SPAS(epsilon_list, sensitivity_s, sensitivity_p, raw_stream, window_size, windownum_warm, windownum_updateE, round_, Flag_)
        
    elif method_name == "sample":

        error_ = mechanism.sample.run_sample(epsilon_list, sensitivity_p, raw_stream, window_size, round_, Flag_)

    elif method_name == "uniform":

        error_ = mechanism.uniform.run_uniform(epsilon_list, sensitivity_p, raw_stream, window_size, round_, Flag_)
    
    elif method_name == "dsat":

        error_ = mechanism.dsat.run_dsat(epsilon_list, sensitivity_p, raw_stream, window_size, round_, Flag_)

    elif method_name == "pegasus":

        error_ = mechanism.pegasus.run_pegasus(epsilon_list, sensitivity_p, raw_stream, window_size, round_, Flag_)

    elif method_name == "fast":

        error_ = mechanism.fast_w_event.run_fast(epsilon_list, sensitivity_p, raw_stream, window_size, round_, Flag_)

    elif method_name == "bd":

        error_ = mechanism.bd.run_bd(epsilon_list, sensitivity_p, raw_stream, window_size, round_, Flag_)

    elif method_name == "adapub":
        
        error_ = mechanism.adapub.run_adapub(epsilon_list, sensitivity_p, raw_stream, window_size, round_, Flag_)


    return error_


def run_method_sum_query(method_name, epsilon_list, sensitivity_s, sensitivity_p, raw_stream, window_size, windownum_warm, windownum_updateE, round_, query_num, Flag_ = 0):
    if method_name == "spas":
        error_ = mechanism.SPAS.run_SPAS_sum_query(epsilon_list, sensitivity_s, sensitivity_p, raw_stream, window_size, windownum_warm, windownum_updateE, round_, query_num, Flag_)
        
    elif method_name == "sample":

        error_ = mechanism.sample.run_sample_sum_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "uniform":

        error_ = mechanism.uniform.run_uniform_sum_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)
    
    elif method_name == "dsat":

        error_ = mechanism.dsat.run_dsat_sum_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "pegasus":

        error_ = mechanism.pegasus.run_pegasus_sum_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "fast":

        error_ = mechanism.fast_w_event.run_fast_sum_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "bd":

        error_ = mechanism.bd.run_bd_sum_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "adapub":
        
        error_ = mechanism.adapub.run_adapub_sum_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)


    return error_


def run_method_count_query(method_name, epsilon_list, sensitivity_s, sensitivity_p, raw_stream, window_size, windownum_warm, windownum_updateE, round_, query_num, Flag_ = 0):
    if method_name == "spas":
        error_ = mechanism.SPAS.run_SPAS_count_query(epsilon_list, sensitivity_s, sensitivity_p, raw_stream, window_size, windownum_warm, windownum_updateE, round_, query_num, Flag_)
        
    elif method_name == "sample":

        error_ = mechanism.sample.run_sample_count_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "uniform":

        error_ = mechanism.uniform.run_uniform_count_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)
    
    elif method_name == "dsat":

        error_ = mechanism.dsat.run_dsat_count_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "pegasus":

        error_ = mechanism.pegasus.run_pegasus_count_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "fast":

        error_ = mechanism.fast_w_event.run_fast_count_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "bd":

        error_ = mechanism.bd.run_bd_count_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)

    elif method_name == "adapub":
        
        error_ = mechanism.adapub.run_adapub_count_query(epsilon_list, sensitivity_p, raw_stream, window_size, round_, query_num, Flag_)


    return error_


def run_dataset(dataset_name):
    raw_stream = mechanism.data_process.data_reader(dataset_name)

    return raw_stream
    
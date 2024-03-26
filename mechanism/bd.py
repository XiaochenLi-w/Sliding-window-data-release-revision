import math
import numpy as np

from mechanism.common_metrics import count_mre
from mechanism.data_process import data_reader

def lap(v, epsilon, sensitivity):
    return v + np.random.laplace(loc=0,scale=sensitivity/epsilon)

def lap_arr(v, epsilon, sensitivity):
    tmp = np.random.laplace(loc=0,scale=sensitivity/epsilon)
    new_arr = []
    for i in range(len(v)):
        new_arr.append(v[i] + tmp)
    
    return new_arr


def find_last_element(list):
    ls = [i for i, j in enumerate(list) if j != []]
    # if len(ls) == 0:
    #     return NULL
    return list[ls[-1]]


def dis_func(ls1, ls2, d):
    sum_dis = 0
    for i in range(d):
        sum_dis = sum_dis + abs(ls1[i] - ls2[i])
    
    return sum_dis / d


def mech1(epsilon, sensitivity, c, op_arr, window_size, dim):
    ls = find_last_element(op_arr)
    dis = dis_func(ls, c, dim)
    # global total_dis, dis_arr
    # total_dis[0] += dis
    # dis_arr[0].append(dis)
    tmp_eps = epsilon / 2 if dim > window_size else epsilon * dim / 8 / window_size
    return lap(dis, tmp_eps, sensitivity)
    

def mech2(epsilon, sensitivity, c, dis, op_arr, ep_arr, window_size, dim):
    eps_rm = (epsilon - (window_size * epsilon / 2 / dim if dim > window_size else epsilon / 8)) - sum(ep_arr)
    # eprm_arr.append(eps_rm)
    # print(eps_rm)
    tmp_eps = eps_rm * 3 / 4
    # print(dis, tmp_eps)
    # global publish_num
    if tmp_eps != 0 and dis > 1 / tmp_eps:
        # publish_num[0] += 1
        op_arr.append(lap_arr(c, tmp_eps, sensitivity))
        ep_arr.append(tmp_eps)
    else:
        op_arr.append([])
        ep_arr.append(0)
    return op_arr[-1]


def bd_workflow(epsilon, sensitivity, ex, window_size, dim):
    res = []
    eps_arr = []
    dis = 10000000
    for i in range(len(ex)):

        if len(res) != 0:
            dis = mech1(epsilon, sensitivity, ex[i], res, window_size, dim)

        mech2(epsilon, sensitivity, ex[i], dis, res, eps_arr, window_size, dim)

    publish_num = 0
    for i in range(len(res)):
        if res[i] == []:
            res[i] = res[i-1]
        else:
            publish_num += 1

    return res


def run_bd(epsilon, sensitivity, raw_stream, window_size, dim, round_, Flag_ = 0):
    MAE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            MAE_ = 0
            for r in range(round_):
                published_result = bd_workflow(eps, sensitivity, raw_stream, window_size, dim)
                MAE_ += count_mre(raw_stream, published_result)
            
            MAE_ = MAE_ / round_
            print("epsilon:", eps, "Done!")
        
            MAE_list.append(MAE_)

        print('BD DONE!')

    else:
        for w in window_size:
            MAE_ = 0
            for r in range(round_):
                published_result = bd_workflow(epsilon, sensitivity, raw_stream, w, dim)
                MAE_ += count_mre(raw_stream, published_result)
            
            MAE_ = MAE_ / round_
            print("window size:", w, "Done!")
        
            MAE_list.append(MAE_)

        print('BD DONE!')

    return MAE_list


if __name__ == "__main__":
    dataset_name = ["unemployment"]
    raw_stream = data_reader(dataset_name[0])
    epsilon = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    sensitivity_s = 1
    sensitivity_p = 1
    window_size = 100
    dim = 1
    round_ = 1
    
    error_ = run_bd(epsilon, sensitivity_p, raw_stream, window_size, dim, round_)
    print(error_)
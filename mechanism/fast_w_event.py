import numpy as np
import math

from mechanism.common_metrics import count_mae
from mechanism.data_process import data_reader

para_ratio = 0.075
para_windowPID = 5

def publish(epsilon, sensitivity, raw_stream):


    P = 100.0
    Q = 100000.0
    R = 1000000.0
    K = 0.0
    Cp = 0.9
    Ci = 0.1
    Cd = 0.0
    theta = 5.0
    xi = 0.1
    minIntvl = 1
    publish_num = 0

    query = [0 for i in range(len(raw_stream))]
    predict = [0 for i in range(len(raw_stream))]
    publish = [0 for i in range(len(raw_stream))]
    m = para_ratio * len(raw_stream)
    if m <= 0:
        m = 1

    eps_per_sample = epsilon / m

    interval = 1

    nextquery = max(1, para_windowPID) + interval - 1

    for i in range(len(raw_stream)):
            # begin: Algorithm 3
            if (i == 0):
                publish[i] = raw_stream[i] + np.random.laplace(loc = 0,scale = sensitivity / eps_per_sample)
                publish_num += 1
                query[i] = 1
            else:
                # Line 2 'obtain prior estimate from prediction'
                predct = 0
                for ii in range(len(query)):
                    if query[len(query) - 1 - ii] == 1:
                        predct = publish[len(query) - 1 - ii]
                        break

                P += Q
                predict[i] = int(predct)
                card = 0
                for ii in range(len(query)):
                    if query[ii] == 1:
                        card += 1

                # if (Mechansim.TRUNCATE)
                #     this.predict[i] = Mechansim.truncate(predct);
                # // (not covered in algo just in text) exception handling; integral value can only be calculated when there have been >= windowPID samples
                if ((card < para_windowPID) and (card < m)):

                    publish[i] = raw_stream[i] + np.random.laplace(loc = 0,scale = sensitivity / eps_per_sample)
                    publish_num += 1
                    query[i] = 1
                    # correctKF(i, predct)
                    K = P / (P + R)
                    correct = predct + K * (publish[i] - predct)
                    publish[i] = correct
                    P = 1.0 - K

                    # Line 3 'if sampling point and numSamples < M'
                elif ((i == nextquery) and (card < m)):
                    # Line 4 'perturb'
                    publish[i] = raw_stream[i] + np.random.laplace(loc = 0,scale = sensitivity / eps_per_sample)
                    publish_num += 1
                    query[i] = 1
                    # line 6: obtain posterior estimate from correction
                    # correctKF(i, predct)
                    K = P / (P + R)
                    correct = predct + K * (publish[i] - predct)
                    publish[i] = correct
                    P = 1.0 - K

                    # line 8: adjust sampling rate by adaptive sampling =>
                    # begin: Algo. 9
                    # ratio = PID(i); // PID error


                    sum = 0.0
                    lastValue = 0.0
                    change = 0.0
                    timeDiff = 0
                    next = i
                    for j in range(para_windowPID -1, -1, -1):
                        index = 0
                        for index in range(next, -1, -1):

                            if (query[index] == 1):
                                next = index - 1
                                break
                        
                        
                        if (j == para_windowPID - 1):
                            # Feedback error (cf. Def. 4)
                            lastValue = abs(publish[index] - predict[index]) / (1.0 * max(publish[index], 1))
                            change = abs(publish[index] - predict[index]) / (1.0 * max(publish[index], 1))
                            timeDiff = index
                        
                        if (j == para_windowPID - 2):
                            change -= abs(publish[index] - predict[index]) / (1.0 * max(publish[index], 1))
                            timeDiff -= index
                        
                        sum += abs(publish[index] - predict[index]) / (1.0 * max(publish[index], 1))
                    
                    # Eq. (29) . last value = e_k_n = feedback error
                    ratio = Cp * lastValue + Ci * sum + Cd * change / timeDiff
                    
                    try:
                        deltaI = (int) (theta * (1.0 - math.exp((ratio - xi) / xi))); # (32) - max fehlt
                    
                    except Exception as e:
                        # print(Cp, lastValue, Ci, sum, Cd, change, timeDiff, theta, ratio, xi)
                        deltaI = 0

                    interval += deltaI
                    if (interval < minIntvl):
                        interval = minIntvl
                    
                    nextquery += interval
                    # end: Algo 9
                else:
                    # line 10
                    publish[i] = int(predct)
                
            
            # end: Algorithm 3

        
    return publish, publish_num

def run_fast(epsilon, sensitivity, raw_stream, window_size, dim, round_):

    publish_num = 0
    res = [[0 for j in range(dim)] for i in range(len(raw_stream))]
    MAE_list = []
    
    for eps in epsilon:
        MAE_ = 0
        for r in range(round_):
            for t in range(0, len(raw_stream), window_size + 1):

                end_index = min(t + window_size, len(raw_stream) - 1) + 1
                for d in range(dim):  
                    substream_of_dimension = []
                    for i in range(t, end_index - 1):
                        substream_of_dimension.append(raw_stream[i][d])
                    fast = substream_of_dimension
                    published, tmp_publish_num = publish(eps, sensitivity, fast)
                    publish_num += tmp_publish_num / dim

                    for i in range(len(published)):
                        res[t + i][d] = published[i]
            MAE_ += count_mae(raw_stream, res)

        MAE_ = MAE_ / round_
        print("epsilon:", eps, "Done!")

        MAE_list.append(MAE_)

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
    
    error_ = run_fast(epsilon, sensitivity_p, raw_stream, window_size, dim, round_)
    print(error_)

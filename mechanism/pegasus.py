import numpy as np
import math

from mechanism.common_metrics import count_mae
from mechanism.data_process import data_reader

class Pegasus:

    DEBUG_FORCE_NEW_GROUP_EACH_TIMESTAMP = False
    # smoother
    AVG_SMOOTHER = 0
    MEDIAN_SMOOTHER = 1
    JS_SMOOTHER = 2
    USE_SMOOTHER = MEDIAN_SMOOTHER

    eps_per_ts = 0

    eps_p = 0
    eps_g = 0
    # grouper
    init_theta = 0
    tempDataDim = []

    def __init__(self, para_eps_, para_w_, para_d_, para_sen):
        
        self.eps_per_ts = para_eps_ / para_w_
        self.eps_p = self.eps_per_ts * 0.8
        self.eps_g = self.eps_per_ts * 0.2
        self.init_theta = 5.0 / self.eps_g
        self.sensitivity = para_sen

    def run(self, org_stream):

        # init
        # init() # aederung des w von außen..
        length = len(org_stream)
        sanitized_stream = []
        no_dim = len(org_stream[0])
        self.tempDataDim = [self.PegasusDataDim(self) for i in range(no_dim)]
        

        for t in range(length):
            origStream_t = org_stream[t]
            sanStream_t = [0 for i in range(no_dim)]

            for dim in range(no_dim): # separate pegasus for each dimension
                # init
                tempDataOfDim = self.PegasusDataDim(self) 
                if (t == 0):
                    tempDataOfDim = self.PegasusDataDim(self)
                    self.tempDataDim[dim] = tempDataOfDim
                else:
                    tempDataOfDim = self.tempDataDim[dim]

                
                # go
                c_t = origStream_t[dim]
                san_c_t = self.perturber(c_t, self.eps_p)
                self.grouper(t, c_t, tempDataOfDim)
                # tempDataOfDim.perturbedStream_last_group.add(san_c_t) #  important. otherwise, smoother does not work correctly.
                tempDataOfDim.perturbedStream_last_group_stat.append(san_c_t)
                # 
                smoothed_c_t = self.smoother(tempDataOfDim.perturbedStream_last_group_stat)
                #  replace with smoothed value

                # if (smoothed_c_t == 0)
                #     System.out.print("")

                # if (Mechansim.TRUNCATE) {
                #     double smoothed_c_t_and_trunc = truncate(smoothed_c_t)
                #     smoothed_c_t = smoothed_c_t_and_trunc
                # }
                # if (abs(smoothed_c_t - c_t) > abs(san_c_t - c_t))
                #     System.out.print("")

                # tempDataOfDim.perturbedStream_last_group.set(tempDataOfDim.perturbedStream_last_group.size() - 1, smoothed_c_t)
                # tempDataOfDim.perturbedStream_last_group.remove(tempDataOfDim.perturbedStream_last_group.size() - 1)
                # tempDataOfDim.perturbedStream_last_group.add(smoothed_c_t)

                sanStream_t[dim] = smoothed_c_t

            
            # System.out.println(Math.abs(start-System.currentTimeMillis())/1000d + " ms for one timestamp")
            sanitized_stream.append(sanStream_t)

        

        return sanitized_stream
    

    def perturber(self, c_t, eps_p):
        return c_t + np.random.laplace(0, self.sensitivity / eps_p)
    


    def dev(self, trueStream_last_group, c_t):
        dev = 0

        average_count = (sum(trueStream_last_group) + c_t) / (len(trueStream_last_group) + 1)
        for c in trueStream_last_group:
            dev += abs(c - average_count)
        
        dev += abs(c_t - average_count)
        return dev
    

    def grouper(self, t, c_t, tempDataDim):
        noisy_theta = 0

        #  Line 1-5  -- already done
        # if (t==0) {
        # ArrayList<Double> last_group = new ArrayList<Double>()
        # 	last_group = new ArrayList<Double>()
        # 	self.last_group_closed = true
        # } else {
        # last_group = last_partition_P_t_1.get(last_partition_P_t_1.size() - 1)
        # }
        #  Line 6-8
        xx = []
        xx.clear()
        if (self.DEBUG_FORCE_NEW_GROUP_EACH_TIMESTAMP or tempDataDim.last_group_closed):
            tempDataDim.idx_last_group.clear() # new group
            tempDataDim.idx_last_group.append(t)
            tempDataDim.trueStream_last_group.clear() # new group
            tempDataDim.trueStream_last_group.append(c_t)
            # tempDataDim.perturbedStream_last_group.clear() # new group
            tempDataDim.perturbedStream_last_group_stat.clear()
            tempDataDim.last_group_closed = False

            lamdba_thres = 4.0 / self.eps_g
            noisy_theta = self.init_theta + np.random.laplace(0, self.sensitivity * lamdba_thres) # reset theta
            #  Line 9-16
        else:
            noisy_theta = tempDataDim.noisy_theta_prev

            dev = self.dev(tempDataDim.trueStream_last_group, c_t)
            lamdba_dev = 8.0 / self.eps_g
            noisy_dev = dev + np.random.laplace(0, self.sensitivity * lamdba_dev)# sanitize(dev, lamdba_dev)
            if (abs(noisy_dev) < abs(noisy_theta)): 
                tempDataDim.idx_last_group.append(t)
                tempDataDim.trueStream_last_group.append(c_t)
                tempDataDim.last_group_closed = False
            else:
                tempDataDim.idx_last_group.clear() #  new ArrayList<Double>() # new group
                tempDataDim.idx_last_group.append(t)
                tempDataDim.trueStream_last_group.clear() # new group
                tempDataDim.trueStream_last_group.append(c_t)
# 				tempDataDim.perturbedStream_last_group.clear() # new group
                tempDataDim.perturbedStream_last_group_stat.clear()
                tempDataDim.last_group_closed = True
            
        
        #  Line 17
        tempDataDim.noisy_theta_prev = noisy_theta
        return tempDataDim.idx_last_group
    

    def smoother(self, sanStream_last_group):
        smoothed_c_t = 0
        if (Pegasus.USE_SMOOTHER == Pegasus.AVG_SMOOTHER):
            smoothed_c_t = self.averageSmoother(sanStream_last_group)
        elif (Pegasus.USE_SMOOTHER == Pegasus.MEDIAN_SMOOTHER):
            smoothed_c_t = self.medianSmoother(sanStream_last_group)
        elif (Pegasus.USE_SMOOTHER == Pegasus.JS_SMOOTHER):
            smoothed_c_t = self.jsSmoother(sanStream_last_group)
        
        return smoothed_c_t
    

    def smoother(self, sanStream_last_group):
        smoothed_c_t = 0
        if (Pegasus.USE_SMOOTHER == Pegasus.AVG_SMOOTHER):
            smoothed_c_t = self.averageSmoother(sanStream_last_group)
        elif (Pegasus.USE_SMOOTHER == Pegasus.MEDIAN_SMOOTHER):
            smoothed_c_t = self.medianSmoother(sanStream_last_group)
        elif (Pegasus.USE_SMOOTHER == Pegasus.JS_SMOOTHER):
            smoothed_c_t = self.jsSmoother(sanStream_last_group)
        
        return smoothed_c_t
    

    def averageSmoother(self, sanStream_last_group):
        return sum(sanStream_last_group) / len(sanStream_last_group)
    


    def medianSmoother(self, sanStream_last_group):
        return np.mean(sanStream_last_group)
    

    def jsSmoother(self, sanStream_last_group):
        avg = self.averageSmoother(sanStream_last_group)
        group_size = len(sanStream_last_group)
        noisy_c_t = sanStream_last_group[-1]
        return (noisy_c_t - avg) / group_size + avg
    

    class PegasusDataDim:
        
        # Line 1-5 from grouper
        idx_last_group = []
        trueStream_last_group = []
        # 	ArrayList<Double> perturbedStream_last_group = new ArrayList<Double>() #  NOT smoothed, only perturbed!!
        perturbedStream_last_group_stat = [] #  NOT smoothed, only perturbed!!
        last_group_closed = True
        def __init__(self, obj):

            self.obj = obj
            self.noisy_theta_prev = self.obj.init_theta


def run_pegasus(epsilon, sensitivity, raw_stream, window_size, dim, round_, Flag_ = 0):
    MAE_list = []
    
    if Flag_ == 0:
        for eps in epsilon:
            MAE_ = 0
            for r in range(round_):
                mech = Pegasus(eps, window_size, dim, sensitivity)
                published_result = mech.run(raw_stream)
                MAE_ += count_mae(raw_stream, published_result)
            
            MAE_ = MAE_ / round_
            print("epsilon:", eps, "Done!")
        
            MAE_list.append(MAE_)

        print('Pegasus DONE!')

    else:
        for w in window_size:
            MAE_ = 0
            for r in range(round_):
                mech = Pegasus(epsilon, w, dim, sensitivity)
                published_result = mech.run(raw_stream)
                MAE_ += count_mae(raw_stream, published_result)
            
            MAE_ = MAE_ / round_
            print("window size:", w, "Done!")
        
            MAE_list.append(MAE_)

        print('Pegasus DONE!')

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
    
    error_ = run_pegasus(epsilon, sensitivity_p, raw_stream, window_size, dim, round_)
    print(error_)
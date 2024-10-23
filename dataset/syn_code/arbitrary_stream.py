import numpy as np
import random
import pandas as pd

Value_low = 0
Value_high = 10000

variance_low = 1
variance_high = 20

def Randgen_normal():
    Mean_ = random.randint(Value_low, Value_high)
    Var_ = random.randint(variance_low, variance_high)

    data_point = np.random.normal(Mean_, Var_)

    return data_point

def Randgen_laplace():
    Mean_ = random.randint(Value_low, Value_high)
    Var_ = random.randint(variance_low, variance_high)

    data_point = np.random.laplace(Mean_, Var_)

    return data_point

def Randgen_stream(len, dim):
    if dim == 1:
        data_stream = np.zeros(len, dtype = int)

        for i in range(len):
            if random.random() < 0.5:
                data_stream[i] = Randgen_normal()
            else:
                data_stream[i] = Randgen_laplace()
    else:
        data_stream = np.zeros([len, dim], dtype = int)

        for i in range(len):
            if random.random() < 0.5:
                for j in range(dim):
                    data_stream[i][j] = Randgen_normal()
            else:
                for j in range(dim):
                    data_stream[i][j] = Randgen_laplace()

    return data_stream


if __name__ == "__main__":
    len = 10000
    dim = 10
    
    data_stream = Randgen_stream(len, dim)
    stream = pd.DataFrame(data_stream)
    filename = 'lArbitrary' + str(dim) + '.csv'
    stream.to_csv(filename)
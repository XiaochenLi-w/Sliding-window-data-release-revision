
def data_reader(name):

    count = 0
    data = []
    
    if name == "unemployment":
        filename = "./dataset/real_dataset/unemployment.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 2:
                    tmp = lines.split(',')
                    
                    data.append([int(tmp[-1])])

    elif name == "syn_uniform":
        #filename = "./dataset/syn_dataset/uniform_len10000dim1.csv"
        filename = "./dataset/syn_dataset/uniform_len10000dim1up1000.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 1:
                    tmp = lines.split(',')
                    
                    data.append([int(tmp[-1])])

    elif name == "syn_gauss":
        filename = "./dataset/syn_dataset/gauss_len10000dim1up200.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 1:
                    tmp = lines.split(',')
                    
                    data.append([int(tmp[-1])])

    elif name == "syn_mix":
        filename = "./dataset/syn_dataset/mix2_len10000dim1up1000 (2).csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 1:
                    tmp = lines.split(',')
                    
                    data.append([int(tmp[-1])])

    return data
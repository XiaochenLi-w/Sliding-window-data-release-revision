
def data_reader(name):

    count = 0
    data = []
    

    if name == "nation":
        filename = "./dataset/real_dataset/National_Custom_Data.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 2:
                    data.append([int(float(i)) for i in lines.split(',')])
                    # tmp = lines.split(',')
                    
                    # data.append([int(tmp[-3])])
                    

    elif name == "syn_uniform":
        filename = "./dataset/syn_dataset/uniform_len10000dim1.csv"
        #filename = "./dataset/syn_dataset/uniform_len10000dim1up1000.csv"
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


# old dataset
                    
    elif name == "F1d":
        filename = "./dataset/old_data/ILINet.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 3:
                    tmp = lines.split(',')
                    
                    data.append([int(tmp[-3])])

    elif name == "Dth":
        filename = "./dataset/old_data/death.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 3:
                    tmp = lines.split(',')
                    
                    data.append([int(tmp[-6])])

    elif name == "Uem":
        filename = "./dataset/old_data/unemployment.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 3:
                    tmp = lines.split(',')
                    
                    data.append([int(tmp[-1])])

    elif name == "Fmd":
        filename = "./dataset/old_data/flumd_output.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 3:
                    data.append([int(i) for i in lines.split(',')])

    elif name == "Tdv":
        filename = "./dataset/old_data/td_output.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 3:
                    data.append([int(i) for i in lines.split(',')])

    elif name == "Tpt":
        filename = "./dataset/old_data/tp_output.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 2:
                    data.append([int(i) for i in lines.split(',')])
    
    elif name == "Ret":
        filename = "./dataset/old_data/retail_output.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 2:
                    data.append([int(i) for i in lines.split(',')])
    
    elif name == "Wcp":
        filename = "./dataset/old_data/worldcup_output.csv"
        with open(filename, 'r', encoding='utf-8') as file_to_read:
            while True:

                lines = file_to_read.readline()
                count += 1
                if not lines:
                    break
                elif count>= 2:
                    data.append([int(i) for i in lines.split(',')])

    return data
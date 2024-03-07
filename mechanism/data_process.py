
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
    
    return data
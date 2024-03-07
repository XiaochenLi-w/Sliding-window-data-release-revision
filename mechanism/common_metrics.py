def count_mae(raw_result, published_result):
    total_time = len(raw_result)
    published_time = len(published_result)
    #print(total_time, published_time)

    if total_time != published_time:
        print("The length of the published results and raw results are mismatched!")
        return
    
    error_sum = 0

    for i in range(published_time):
        error_sum += abs(raw_result[i][0] - published_result[i][0])
    
    return error_sum / published_time
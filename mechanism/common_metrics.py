import random

def count_mre(raw_result, published_result):
    total_time = len(raw_result)
    published_time = len(published_result)
    dim = len(raw_result[0])
    #print(total_time, published_time)

    if total_time != published_time:
        print("The length of the published results and raw results are mismatched!")
        return
    
    error_sum = 0

    for i in range(published_time):
        for j in range(dim):
            if raw_result[i][j] == 0:
                error_sum += abs(published_result[i][j])
            else:
                error_sum += abs(raw_result[i][j] - published_result[i][j]) / raw_result[i][j]
    
    return error_sum / (published_time * dim)

def range_query_sum(raw_result, published_result, query_num):
    total_time = len(raw_result)
    published_time = len(published_result)
    dim = len(raw_result[0])
    query_list = []
    raw_query_result = []
    published_query_result = []
    #print(total_time, published_time)

    if total_time != published_time:
        print("The length of the published results and raw results are mismatched!")
        return
    
    while(len(query_list)<query_num):
        a = random.randint(0, total_time)
        b = random.randint(0, total_time)
        if(a == b):
            continue
        elif(a < b):
            query_list.append((a, b))
        else:
            query_list.append((b, a))
    print('random sum query generated, query_num:', len(query_list))
    
    for query in query_list:
        raw_sum = [0 for i in range(dim)]
        published_sum = [0 for i in range(dim)]
        
        for i in range(*query):
            for j in range(dim):
                raw_sum[j] += raw_result[i][j]
                published_sum[j] += published_result[i][j] 
            
        raw_query_result.append(raw_sum)
        published_query_result.append(published_sum)
    
    if (len(raw_query_result)!= query_num or len(published_query_result)!= query_num):
        print('The length of query result does\'t match' )
        return
        
    return count_mre(raw_query_result, published_query_result)

def range_query_count(raw_result, published_result, query_num):
    total_time = len(raw_result)
    published_time = len(published_result)
    dim = len(raw_result[0])
    raw_query_result = [[] for i in range(query_num)]
    published_query_result = [[] for i in range(query_num)]
    #print(total_time, published_time)

    if total_time != published_time:
        print("The length of the published query results and the length of raw query results mismatch!")
        return
    
    max_values = [max(ts[i] for ts in raw_result) for i in range(dim)]
    
    for dim_num in range(dim):
        query_list = []
        
        while(len(query_list) < query_num):
            a = random.uniform(0, max_values[dim_num])
            b = random.uniform(0, max_values[dim_num])
            
            if(a == b):
                continue
            elif(a < b):
                query_list.append((a, b))
            else:
                query_list.append((b, a))
        print('random count query for dim', dim_num, 'generated, query_num:', len(query_list))
        
        for query_index in range(len(query_list)):
            raw_count = 0
            published_count = 0
            for ts in range(total_time):
                if(raw_result[ts][dim_num] >= query_list[query_index][0] and raw_result[ts][dim_num] < query_list[query_index][1]):
                    raw_count += 1
                if(published_result[ts][dim_num] >= query_list[query_index][0] and published_result[ts][dim_num] < query_list[query_index][1]):
                    published_count += 1
            raw_query_result[query_index].append(raw_count)
            published_query_result[query_index].append(published_count)  
        
    for i in range(query_num):
        if(len(raw_query_result[i]) != dim or len(published_query_result[i]) != dim):
            print(f"The length of the published query result[{i}] and the length of raw query results[{i}] mismatch!")
    
    return count_mre(raw_query_result, published_query_result)

if __name__ == "__main__":
    a = [[1] for i in range(30)]+[[0.5] for i in range(70)]
    b = [[0.5] for i in range(100)]
    print(range_query_sum(a, b, 100))
    print(range_query_count(a, b, 100))
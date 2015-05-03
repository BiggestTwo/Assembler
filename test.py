arr = [1,2,1,3,9]
for i in range(len(arr)) :
    print i, arr[i], arr
    if i == 2 :
        arr.insert(2, 0)
        arr.insert(2, 0)
import random,copy,time
#======================================================

def bubbleSort(arr):
    n = len(arr)
    for i in range(n):#모든 element에 대해서 반복
        for j in range(n - i - 1):
            #이거 한 루프가 끝날때마다 가장 큰 숫자가 맨 뒤로 감
            #그래서 이미 맨 뒤로 보내버린 숫자를 제외해서 len(a) - i - 1인거임
            if arr[j] > arr[j+1]:
                #쉬운 swap 방법: t1,t2 = t2,t1하면 잘 바뀜
                arr[j], arr[j+1] = arr[j+1], arr[j]

#======================================================
                
##  ===처음 시작할때===
##  i
##   j
##   192670 4

def partition(low,high,arr):
    pivot = arr[high]#맨 뒤에 있는애가 pivot
    i = low - 1#나까지 해서 내 뒤에 몇명이 pivot보다 작은지 저장. 예를 들어서 3이면 4번째 요소를 가리키고 있다는 거임. 즉, arr[low]부터 arr[i]까지는 pivot들보다 작은 애들이 있다는 뜻.
    for j in range(low,high):#pivot 바로 전까지만 루프 돌아감
        if a[j] < pivot:
            i += 1#pivot보다 작은 애가 한명 생김
            a[i],a[j] = a[j],a[i]#그 둘이 자리를 바꿈
            
    arr[i+1],arr[high] = arr[high],arr[i+1]#pivot을 올바른 위치로 이동
    return i+1
            
        
def quickSort(low,high,arr):
    if len(arr) == 1:
        return
    if low < high:
        pi = partition(low,high,arr)
        quicksort(low,pi-1,arr)
        quicksort(pi+1,high,arr)
    
#======================================================
        
def merge(left,right):
    ReturnList = []
    i,j = 0,0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            ReturnList.append(left[i])
            i += 1
        else:
            ReturnList.append(right[j])
            j += 1
    if i == len(left):
        ReturnList = ReturnList + right[j:]
    if j == len(right):
        ReturnList = ReturnList + left[i:]
    return ReturnList
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    m = len(arr) // 2
    left = merge_sort(arr[:m])
    right = merge_sort(arr[m:])
    return merge(left,right)

#======================================================

def bogoSort(a): 
    n = len(a) 
    while not is_sorted(a): 
        shuffle(a) 
  
# To check if array is sorted or not 
def is_sorted(a): 
    n = len(a) 
    for i in range(0, n-1): 
        if (a[i] > a[i+1] ): 
            return False
    return True
  
# To generate permuatation of the array 
def shuffle(a): 
    n = len(a) 
    for i in range (0,n): 
        r = random.randint(0,n-1) 
        a[i], a[r] = a[r], a[i]

#======================================================

def countingSort(arr):
    n = len(arr)
    arr1 = [0] * n

    x = [0] * 10

    for i in range(0, n):
        x[arr[i]] += 1

    for i in range(1, 10):
        x[i] += x[i - 1]


    i = n - 1
    while i >= 0:
        arr1[x[arr[i]] - 1] = arr[i]
        x[arr[i]] -= 1
        i -= 1

    for i in range(0, n):
        arr[i] = arr1[i]

#======================================================

def selectionSort(arr):
    n = len(arr)
    for i in range(n):#모든 element에 대해서 반복
        min_idx = i
        for j in range(i + 1, n): 
            if arr[min_idx] > arr[j]: 
                min_idx = j#가장 작은 숫자의 index 찾기
                  
        arr[i], arr[min_idx] = arr[min_idx], arr[i]#가장 작은 숫자와 arr[i] 자리 바꾸기(이렇게 하면 이 for문이 한 번 돌때마다 가장 작은 숫자가 앞에 옴)


#======================================================

def insertionSort(arr):
    n = len(arr)
    for i in range(1,n):#맨 앞의 수를 제외한 모든 element에 대해서 반복
        key = arr[i]
        idx = i - 1
        for j in range(i - 1, -1, -1):#역순으로 배열 조사
            if arr[j] > key:
                arr[j+1] = arr[j]
            else:
                break
            idx -= 1
            
        arr[idx + 1] = key


    
#======================================================
        
def heapSort(arr):
    n = len(arr)

    for i in range(n):#max heap 만들기
        child = i
        while child != 0:
            root = (child - 1) // 2
            if arr[child] > arr[root]:
                arr[child], arr[root] = arr[root], arr[child]
            child = root

    for i in range(n - 1, -1, -1):
        arr[0], arr[i] = arr[i], arr[0]
        root = 0
        child = 1
        while child < i:
            child = 2 * root + 1
            if child < i - 1 and arr[child] < arr[child + 1]:
                child += 1

            if child < i and arr[child] > arr[root]:
                arr[child], arr[root] = arr[root], arr[child]

            root = child

#======================================================


#=== Types of Sorts ===#
# bubbleSort, quickSort, mergeSort, bogoSort, countingSort, selectionSort, heapSort

a = [3,5,1]
#a = [random.randint(-10,10) for i in range(10)]
insertionSort(a)
print(a)

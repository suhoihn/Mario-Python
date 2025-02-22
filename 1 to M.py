n = int(input("Write a number to count ChoHap(1,2,3으로 만들 수 있는 경우의 수)"))
print("got it")

result = [1,2,4]+[0]*n

for i in range(3,n):
    result[i] = result[i-1]+result[i-2]+result[i-3]


print(result[n-1])

#출처 https://pangsblog.tistory.com/8

import sys,copy
sys.setrecursionlimit(1010)

#IMC 2021 Q1
#Broken Calculator -> only +1 or ^2.
#How many ways to get 1000 from inputting 2?

start = 2
tar = 1000
possible_answers = []

cnt = 0

ExactAnswersIncluded = False

print("Calculating... Please Wait")

if not ExactAnswersIncluded:
    def add(n):
        global cnt 
        if n + 1 == tar:
            cnt += 1
            return
        if n + 1 > tar:
            return
        
        add(n + 1)
        sqr(n + 1)
        
    def sqr(n):
        global cnt
        if n ** 2 == tar:
            cnt += 1
            return
        if n ** 2 > tar:
            return
        
        add(n ** 2)
        sqr(n ** 2)

    add(start)
    sqr(start)

else:
    def add(n,lst):
        global cnt 
        if n + 1 == tar:
            cnt += 1
            lst.append(n+1)
            possible_answers.append(lst)
            return
        if n + 1 > tar:
            return
        lst.append(n + 1)
        l1 = copy.deepcopy(lst)#copy안하면 이상해짐
        l2 = copy.deepcopy(lst)#서로 다른 리스트 사용
        add(n + 1,l1)
        sqr(n + 1,l2)
    def sqr(n,lst):
        global cnt
        if n ** 2 == tar:
            cnt += 1
            lst.append(n**2)
            possible_answers.append(lst)
            return
        if n ** 2 > tar:
            return


        lst.append(n ** 2)
        l1 = copy.deepcopy(lst)
        l2 = copy.deepcopy(lst)

        add(n ** 2,l1)
        sqr(n ** 2,l2)
    
    add(start,[start])
    sqr(start,[start])

print(cnt)
##for idx,case in enumerate(possible_answers):
##    print("("+ str(idx + 1) + ") ", end  = "")
##    for n,i in enumerate(case):
##        if n == len(case) - 1:
##            print(str(i),end = "")
##        else:
##            print(str(i),end = ", ")
##    print("\n")

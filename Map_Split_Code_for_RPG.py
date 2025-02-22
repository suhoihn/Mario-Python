#a=[[1,2,3], [6,7,8,9,0], [1,2,3,4,5], [6,7,8,9,0]]

def FillAllwithSameNum(Map): #Fill Empty Spaces with None Value
    MaxLen = max([len(i) for i in Map])
    for i in Map:
        if len(i)<MaxLen:
            i += (MaxLen-len(i))*[None]

    return Map

def Split(Map,x,y):# 리스트를 옆으로 두고 X * Y 사각형으로 쪼개기 (비는 부분은 None)
    import math

    Map = FillAllwithSameNum(Map)

    #print(Map)
    ReturnMap=[]
    Temp=[]

    a=math.ceil(len(Map)/x)
    b=math.ceil(len(Map[1])/y)
    
    for loop1 in range(math.ceil(len(Map)/y)):
            for loop2 in range(math.ceil(len(Map[loop1])/x)):
                    ReturnMap.append([])
                    for i in range(y):
                            Temp=[]
                            for j in range(x):
                                    try:
                                            Temp.append(Map[loop1*y+i][loop2*x+j])
                                    except:
                                            Temp.append(None)
                            ReturnMap[loop1*y+loop2].append(Temp)
    
    return ReturnMap


#Push all '1' to front
import copy
strlist = list(input("Write '1' or '0':"))

start=True    
for i in strlist:
    if i != '0' and i != '1':
        print("Wrong Input")
        start = False
        break
if start:
    idx = -1
    while idx < len(strlist) -1:
        idx+=1
        if strlist[idx] == '0':
            print(strlist)
            
            Temp = copy.deepcopy(strlist)
            for j in range(len(strlist[idx:])):
                try:
                    strlist[idx+j] = Temp[idx+j+1]
                except:
                    strlist[idx+j] = '0'
            idx = -1
            if strlist == Temp: #바뀐게 없는 경우
                break
    print("Done")
            
            
        

Alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
def main():
    start = True
    while start:
        Mode = int(input("Press 1 to change Num to Base / Press 2 to change Base to Num:"))
        if Mode != 1 and Mode != 2:
            print("Wrong Input")
            continue
            
        Base = int(input("Write base from 2~36: ")) #진법이 36을 넘어가면 알파벳 부족

        if not (2 <= Base <= 36):
            print("Wrong Input")
            continue
        
        Num = input("Write the number: ")
        if Mode == 1:
            NumToBase(int(Num),Base)
        elif Mode == 2:
            BaseToNum(Num,Base)
        
def NumToBase(Num,Base):
    #자리수 결정
    Digit = 0
    while Base ** Digit <= Num:
        Digit+=1

    OutPut = ['0'] * Digit

    for i in range(Digit):
        OutPut[i] = (Num // (Base ** (Digit-i-1))) % Base #숫자 결정(몫이 진법보다 커지면 나머지 연산)
        
        if OutPut[i] >= 10: #각 자리수가 두자리 이면
            OutPut[i] = Alphabet[OutPut[i]-10] #알파벳으로 대체
            
        if Num >= Base ** (Digit-i-1): # 0 이상일 때 (각 자리수가 음수일 수 없음)
            Num -= Base ** (Digit-i-1) # 숫자에서 진법^i 만큼 빼기



    #-----쉬운(?) 설명-----#
    #예를 들어 Num = 10 , Base = 2 라 하자
    #미리 2진법으로 변환을 해 보자 10 -> 1010(2)
    #4자리 수이므로 4번 반복하게 된다
    #첫 번째 반복에서 Num = 10 - (2^3) = 2 / 첫 번째 자리수 = (10을 8(2^3)로 나눈 몫) %2 = 1이 된다 
    #두 번째 반복에서 Num = 2 - (2^2) = -2 인데 각 자리수가 음수일 수 없으므로 두 번째 자리수를 0으로 유지한다
    #세 번째 반복에서 Num = 2 - (2^1) = 0 / 세 번째 자리수 = (2를 2(2^1)로 나눈 몫) %2 = 1이 된다
    #네 번째 반복에서 Num = 0 - (2^0) = -1 이므로 마찬가지로 네 번째 자리수도 0으로 유지한다
    #따라서 결과는 1010(2) 가 나온다

    #다른 진법에 대해 마찬가지 결과로 적용되지만 11진법 이상부터는 각 자리수에 알파벳이 들어갈 수도 있다
    #예를 들어 21을 11진법 으로 변환을 해 보자 -> 1 10(11) (x)
    #각 자리수가 10 이상인 경우 알파벳 순서대로 대체한다 (21 -> 1A(11))

    a = ''
    print("\n")
    #print(OutPut)
    for i in OutPut: a+=str(i)
    print(a)
    print("\n")

    

def BaseToNum(Num,Base):
    NumList = list(str(Num))
    Digit = len(NumList)
    OutPut=0
    for i in range(Digit):
        if NumList[i] in Alphabet:
            OutPut += (Base ** (Digit-i-1)) * (Alphabet.index(NumList[i])+10)
            if Alphabet.index(NumList[i])+10 >= Base: #각 자리수가 진법을 벗어날 때
                print("Wrong Input")
                return
        else:   
            OutPut += (Base ** (Digit-i-1)) * int(NumList[i])
            if int(NumList[i]) >= Base: #각 자리수가 진법을 벗어날 때
                print("Wrong Input")
                return

##    return OutPut
            
    print("\n")
    print(OutPut)
    print("\n")
    
main()
##Message ="663 44958 13946 481586 1068 29166156929 1375732 48784087022 1547593502 27612573869 1068 101736346631011" #36
###Message ="1010010111 1010111110011110 11011001111010 1110101100100110010 10000101100 11011001010011100000011110010000001 101001111110111110100 101101011011110000100001011111101110 1011100001111100110011100011110 11001101101110101100111000010101101 10000101100 10111001000011101010110110011010011101101100011"
##lol = Message.split(' ')
##for i in lol:
##    NumToBase(int(i),36)

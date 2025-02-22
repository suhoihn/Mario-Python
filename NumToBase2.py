print("1. Denary to Binary")
print("2. Binary to Denary")
print("3. Denary to Hexadecimal")
print("4. Hexadecimal to Denary")

Alphabet = ["A","B","C","D","E","F"]

option = int(input("What's your choice?: "))
if option == 1:
    num = int(input("Enter a denary number: "))
    orig = num
    result = ""
    while num >= 1:
        result += str(num % 2)
        num = num // 2
    print(str(orig) + " --> " + result[::-1])
        
elif option == 2:
    num = input("Enter a binary number: ")
    result = 0
    for i in range(len(num)):
        result += 2 ** (len(num) - i - 1) * int(num[i])
    print(num + " --> " + str(result))

elif option == 3:
    num = int(input("Enter a denary number: "))
    orig = num
    result = ""
    while num >= 1:
        if num % 16 >= 10:
            result += str(Alphabet[num % 16 - 10])
        else:
            result += str(num % 16)
        num = num // 16
    print(str(orig) + " --> " + result[::-1])

elif option == 4:
    num = input("Enter a hexadecimal number: ")
    result = 0
    for i in range(len(num)):
        if num[i] in Alphabet:
            result += 16 ** (len(num) - i - 1) * (Alphabet.index(num[i]) + 10)
        else:
            result += 16 ** (len(num) - i - 1) * int(num[i])
    print(num + " --> " + str(result))


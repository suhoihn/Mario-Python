AccountNo = input("Please enter 5 digit number")
total = 0
for i in range(len(AccountNo)):
    total += int(AccountNo[i]) * (i+2)
    #print(total)
CheckDigit = total % 11
if CheckDigit == int(AccountNo[4]):
    print("Account Number Accepted")
else:
    print("Check digit didnot match")


Hrs = input("How many hours do you want to die?")

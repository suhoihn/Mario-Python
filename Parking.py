Days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
CurrentDay = input("What is today's date: ").lower()
while CurrentDay not in Days:
    print("Please enter a proper date")
    CurrentDay = input("What is today's date: ").lower()
CurrentTime = int(input("What is the hour you arrived: "))
while not 8 <= CurrentTime <= 24:
    print("Sorry, parking is not allowed in that time")
    CurrentTime = int(input("What is the hour you arrived: "))


if CurrentTime <= 16:
    Discount = 50
    if CurrentDay == "saturday":
        MaxHours = 4
        PricePerHour = 3
    elif CurrentDay == "sunday":
        MaxHours = 8
        PricePerHour = 2
    else:
        MaxHours = 2
        PricePerHour = 10
else:
    MaxHours = 24 - CurrentTime
    PricePerHour = 2
    Discount = 10
    
Hours = int(input("How many hours do you want to stay?: "))
while not 1 <= Hours <= MaxHours:
    print("Please enter proper hours")
    Hours = int(input("What is the hour you arrived: "))

TotalPrice = Hours * PricePerHour
CarNum = input("Please enter your 4-digit car number")
while not (len(CarNum) == 4):
    print("Please enter a proper car number")
    CarNum = input("Please enter your 4-digit car number")


total = 0
for x in range(3):
    total += int(CarNum[x])*(x+2)
CheckDigit = total % 11

if CheckDigit == int(CarNum[3]):
    print("Congratulations! You get a " + str(Discount) + "% discount!")
else:
    print("Check digit did not match \nUnable to get discount")
    Discount = 0
TotalPrice = TotalPrice * (100 - Discount) / 100
print(str(TotalPrice) + " is your money you need to pay")

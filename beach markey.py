ItemArray = []
TotalPrice = 0
print("Bat,Ball,Shoes")
selection = input("Enter an item you want to buy(enter 'Quit' to quit)")
while selection != "Quit":
    ItemArray.append(selection)
    print(selection + " has been added to to-buy list")
    selection = input("Enter an item you want to buy(enter 'Quit' to quit)")
for item in ItemArray:
    if item == "Bat":
        TotalPrice += 4
        print("Bat is $4. Current price: " + str(TotalPrice))
    elif item == "Ball":
        TotalPrice += 9
        print("Ball is $9. Current price: " + str(TotalPrice))
    elif item == "Shoes":
        TotalPrice += 18
        print("Shoes are $18. Current price: " + str(TotalPrice))
    else:
        print("There is no item named " + str(item) + ",skipping this product")
print("Total Payment will be $" + str(TotalPrice))

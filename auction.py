import random
#Reservation Price: 물건을 제시한 사람이 최소한으로 받고 싶은 가격
class Item:
    def __init__(self,number,description,rprice):
        self.number = number
        self.description = description
        self.rprice = rprice
        self.NumofBids = 0
        self.sold = False
        self.MaxBid = 0
class User:
    def __init__(self,number,TargetItemNo,bid):
        self.number = number
        self.TargetItemNo = TargetItemNo
        self.bid = bid

Items = []
##while True:
##    #===== Item number ======#
##    ItemNo = input("Enter the number of Item Number(Type 'quit' to quit): ")
##    if ItemNo == "quit":
##        if len(Items) < 10:
##            print("You entered less than 10 items. There are {} item(s) currently identified".format(str(len(Items))))
##            continue
##        else:
##            break
##
##    try: ItemNo = int(ItemNo)
##    except:
##        print("Item number must be a number")
##        continue
##    if ItemNo in [item.number for item in Items]:
##        print("Item number {} already exists".format(str(ItemNo)))
##        continue
##
##    #===== Description =====#
##    desc = input("Enter its description: ")
##
##    #===== Reserve Price =====#
##    while True:
##        try:
##            rprice = int(input("Enter its reserve price: "))
##            break
##        except:
##            print("Reserve price should be a number")
##            continue
##    Items.append(Item(ItemNo,desc,rprice))
for i in range(10):
    Items.append(Item(random.randint(0,100),"wut",random.randint(0,100)))
print("Select an option")
option = input("1 - User bid 2 - End the auction: ")
while option != "2":
    if option == "1":
        for item in Items:
            print("===Item No.{}===".format(item.number))
            print("Descroption: " + item.description)
            print("Current highest Bid: {} \n".format(item.MaxBid))
        while True:
            SelectedItemIdx = -1
            while SelectedItemIdx == -1:
                try:
                    SelectedItemNo = int(input("Enter the item number you want to buy: "))
                except:
                    print("Item number must be a number")
                    continue
                
                for item in range(len(Items)):
                    if Items[item].number == SelectedItemNo:
                        SelectedItemIdx = item
                        break
                if SelectedItemIdx == -1:
                    print("No item number {}".format(str(SelectedItemNo)))
            while True:  
                try:
                    UserNo = int(input("Enter your user number "))
                    break
                except:
                    print("Buyer number must be a number")
            while True:
                Bid = input("Enter your Bid to the item: ")
                if int(Bid) > Items[SelectedItemIdx].MaxBid:
                    Items[SelectedItemIdx].MaxBid = int(Bid)
                    Items[SelectedItemIdx].NumofBids += 1
                    break
                else:
                    print("your have no money lol")
            useroption = input("quit? Y/N")
            if useroption == "Y":
                break
            
                
  
    print("Select an option")
    option = input("1 - User bid 2 - End the auction: ")
    

    


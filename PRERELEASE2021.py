#Num of seats
Out = [9,11,13,15]
Return = [10,12,14,16]

OutSeats = [480,480,480,480]
ReturnSeats = [480,480,480,480]

OutTotal = [0,0,0,0]
ReturnTotal = [0,0,0,0]

print("Departing Trains - seats available")
for i in range(4):
    print(str(i + 1) + ". " + str(Out[i]) + ":00" + "   Seats: " + str(OutSeats[i]))


print("Returning Trains - seats available")
for i in range(4):
    print(str(i + 5) + ". " + str(Return[i]) + ":00" + "   Seats: " + str(ReturnSeats[i]))

def checkInt(value):
    try: int(value)
    except: print("INVALID INPUT"); return False
    else: return True
    
def setOutJourney():    
    OutJourney = int(input("Please select an outbound train(1-4): "))
    while not 1 <= OutJourney <= 4:
        print("INVALID INPUT")
        OutJourney = int(input("Please select an outbound train(1-4): "))
    print("")
    return OutJourney

def setTickets():
    t = input("Input number of tickets you would like to buy(enter x to go back to choose outbound train): ")
    while t == "x":
        setOutJourney()
        t = input("Input number of tickets you would like to buy(enter x to go back to choose outbound train): ")
    t = int(t)

    while t > OutSeats[OutJourney - 1]:
        print("Insufficient amount of tickets availble")
        t = input("Input number of tickets you would like to buy(enter x to go back to choose outbound train): ")
        if t.lower() == "x":
            setOutJourney()
            t = int(input("Input number of tickets you would like to buy(enter x to go back to choose outbound train): "))
        else:
            t = int(t)

    print("")
    return t

def setReturnJourney():
    ReturnJourney = input("Please select a return train(5-8)(enter x to go back to choose the number of tickets): ")
    while ReturnJourney == "x":
        setTickets()
        ReturnJourney = input("Please select a return train(5-8)(enter x to go back to choose the number of tickets): ")
    ReturnJourney = int(ReturnJourney)
    
    while not 5 <= ReturnJourney <= 8:
        print("INVALID INPUT")
        ReturnJourney = input("Please select a return train(5-8)(enter x to go back to choose the number of tickets): ")
        if ReturnJourney == "x":
            setTickets()
        else:
            ReturnJourney = int(ReturnJourney)

    return ReturnJourney

OutJourney = setOutJourney()
Tickets = setTickets()
ReturnJourney = setReturnJourney()


if Out[OutJourney - 1] > Return[ReturnJourney - 5]:
    print("")
    print("Your return time is earlier than your departure")
    print("Please try again")
    print("")

    setReturnJourney()


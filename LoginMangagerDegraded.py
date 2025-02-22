#ATM
MachineBreak = False
LoginInfo = {"suhoihn":['20050819',6974]}
def LoginScreen():
    global MachineBreak
    Prompt = "."
    while not MachineBreak:
        Prompt = input("Hello. How may I help you?(0 - Ignore / 1 - Insert your meal card / 2 - Log In / 3 - Create an account): ")
        if Prompt == "1":
            print("Cannot read the card. \nDestroying system...")
            MachineBreak = True
        elif Prompt == "2":
            Username = input("Username?: ")
            try: LoginInfo[Username]
            except:print("No user named " + Username); continue
            for i in range(3):
                PIN = input("PIN?(You used %d out of 3 tries): "%i)
                if PIN == LoginInfo[Username][0]:
                    print("Welcome, " + Username)
                    MainScreen(Username)
                    if MachineBreak:
                        break

            print("TRIES RAN OUT. MACHINE AUTOMATICALLY DESTROYS")
            MachineBreak = True
        elif Prompt == "3":
            print("Creating an account. Please enter your personal information properly")
            Username = input("Username?: ")
            LoginInfo[Username] = []
            PIN = input("PIN?: ")
            check = '0', '.'
            while PIN != check:
                check = input("Enter the PIN Again: ")
            LoginInfo[Username] = [PIN, 0]
            print("Account Created. Enjoy... =D")
        
def MainScreen(Username):
    global MachineBreak
    PIN, balance = LoginInfo[Username]
    while not MachineBreak:
        Option = input("What would you like to do?(1 - Kick this ATM / 2 - withdraw / 3 - check balance / 4 - change PIN / 5 - deposit / 6 - Log Out): ")
        if Option == "1": print("NO MONEY FOR YOU! GET LOST!"); MachineBreak = True
        elif Option == "2":
            don = int(input("How much money would you like to withdraw?(Press 0 to go back): "))
            balance -= don
            if balance < 0:
                print("Oops! Seems you have not enough money.")
                balance += don
                continue
            if don == 0: continue
            print("$%d has been withdrawn. Thank you\nCurrent Balance: $%d"%(don,balance))
            LoginInfo[Username][1] = balance
            
        elif Option == "3": print("Current Balance: $%d"%balance)
        elif Option == "4":
            NP = input("Input new password(Enter Space to go back): ")
            NPC = ' '
            if NP == " ": continue
            while NP != NPC:
                NPC = input("Input new passward again: ")
            PIN = NP
            print("PIN successfully changed")
            LoginInfo[Username][0] = PIN
        elif Option == "5":
            don = int(input("How much money would you like to deposit?(Press 0 to go back): "))
            balance += don
            if don == 0: continue
            print("$%d has been deposited. Thank you\nCurrent Balance: $%d"%(don,balance))
        elif Option == "6":
            print("Bye," + Username + ". Hope to you see you again" )
            LoginScreen()
    
            
LoginScreen()

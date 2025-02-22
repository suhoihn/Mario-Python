import random
GameEnd = False
opt = []
Q = ["Which company created Mario?","Which company created Sonic?","Which company created PlayStation series?","Which company created Xbox?","What is the symbolic color of Link in the Legend of Zelda series?","When was Nintendo Switch Released?"]
A = ['nintendo','sega','sony','microsoft','green','2017']
Hint = ["This company is famous for Animal Crossing also","Hedgehog","Also famous for digital camera","This company is more famous for operating system","it is also symbolic color of Luigi","After 1 year of Trump's election"]
point = 0
players = []
playerscores = []
print("Welcome to Quiz! (Made by Suho Ihn)")
Nplayers = ""
DoNotReset = False
while True:
    try:Nplayers = int(input("How many people are there?: "));break
    except:print("Please enter proper integer value")
for i in range(Nplayers):
    name = input("Enter the name of each players(Player %d): "%(i+1))
    players.append(name)
while not GameEnd:
    for name in players:
        print("Your turn, " + name +"!")
        opt = []
        Progress = 0
        while Progress < len(Q):
            if not DoNotReset:
                QuestionN = random.randint(0,len(Q) - 1)
                if QuestionN in opt:
                    continue    
                opt.append(QuestionN)
            
            Ans = input(Q[QuestionN] + "(If you want hint, Write \"I am a noob\")"* (not DoNotReset))
            if Ans.upper() == "I am a noob".upper() and not DoNotReset:
                print(Hint[QuestionN])
                DoNotReset = True
                continue
            elif Ans.upper() == A[QuestionN].upper():
                print("nice. 1 point is added for you")
                point += 1
            else:
                print("too bad")
                if point > 0: point -= 1
            DoNotReset = False

            Progress += 1
        print("Your point is "+ str(point))
        playerscores.append(point)
    print("\n=====Game Over=====")
    for idx in range(len(playerscores)):
        print(players[idx] + "'s score: %d"%playerscores[idx])
    print(players[playerscores.index(max(playerscores))] + " scored the best and %d"%(max(playerscores)/len(Q)*100) + "% are correct!")
    again = input("Want to play again?(Y/N)")
    if again != "Y":
        GameEnd = True
        
    
        

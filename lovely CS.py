##for i in range(10):
##    for j in range(10):
##        print("%d x %d = %d"%(i+1,j+1,(i+1) * (j+1)))
##    print("\n")
##

import random
H = 0
T = 0
while H < 50 and T < 50:
    #input("press any key to flip a coin")
    coin = random.randint(0,1)
    if coin == 0: print("WOW! It's a tail!"); T += 1
    else: print("WOW! It's a head!"); H += 1
    
print("H: %d, T: %d"%(H,T))    

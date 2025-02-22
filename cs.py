##x = 50
##while not 20 <= x <= 40:
##    x = int(input("PLEASE INPUT A NUMER BETWEEN 20 AND 40: "))
##
##print("good job")
spts = []
for i in range(10):
    print("Input your 3 favorite sports! =)")
    for j in range(3):
        spts.append(input("Your %d option: "%(j+1)))
        

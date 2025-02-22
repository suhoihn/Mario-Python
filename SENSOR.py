import random
import time

HumTurnedOn = False
SensorInput = random.randint(0,100)
    
while True:
    SensorInput = random.randint(SensorInput - 5, SensorInput + 5)
    SensorInput = max(0, SensorInput)
    SensorInput = min(SensorInput, 100)
    
    print("Oh no! The humidity is " + str(SensorInput) + "%!")
    if SensorInput <= 20:
        if HumTurnedOn:
            print("Nah, it's already turned on!")
        else:
            print("Turn on the humidifier")
            HumTurnedOn = True
    elif SensorInput >= 70:
        if HumTurnedOn:
            print("Turn off the humidifier")
            HumTurnedOn = False
        else:
            print("Nah, it's already turned off!")
            
    else:
        print("Leave me alone")

    print("\n")

    time.sleep(0)
        

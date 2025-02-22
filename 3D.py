import pygame,sys
from math import *
pygame.init()
screen = pygame.display.set_mode((640,480))
X1,Y1,Z1,X2,Y2,Z2 = 0,0,0,0,0,0
RotX,RotY = 0,0
FOV = 74
CameraX,CameraY,CameraZ = 500,500,1
def SetPoint1(x1,y1,z1):
    global X1,Y1,Z1
    X1 = x1
    Y1 = y1
    Z1 = z1

def SetPoint2(x2,y2,z2):
    global X2,Y2,Z2
    X2 = x2
    Y2 = y2
    Z2 = z2

def Set2ndPoint(x1,y1):
    global X1,Y1
    X1 = x1
    Y1 = y1

def Set2ndPointAgain(x2,y2):
    global X2,Y2
    X2 = x2
    Y2 = y2
def DrawLine(x1,y1,z1,x2,y2,z2):
    global X1,Y1,Z1,X2,Y2,Z2,RotX,RotY
    RotX = radians(RotX)
    RotY = radians(RotY)
    SetPoint1(x1-CameraX,y1+CameraY,z1+CameraZ)
    SetPoint2(x2-CameraX,y2+CameraY,z2+CameraZ)
    SetPoint1(Z1*sin(RotY)+X1*cos(RotY),Y1,Z1*cos(RotY)-X1*sin(RotY))
    SetPoint2(Z2*sin(RotY)+X2*cos(RotY),Y2,Z2*cos(RotY)-X2*sin(RotY))
    SetPoint1(X1,Y1*cos(RotX)-Z1*sin(RotX),Y1*sin(RotX)+Z1*cos(RotX))
    SetPoint2(X2,Y2*cos(RotX)-Z2*sin(RotX),Y2*sin(RotX)+Z2*cos(RotX))
    Set2ndPoint(FOV*X1/Z1,FOV*Y1/Z1)
    Set2ndPointAgain(FOV*X2/Z2,FOV*Y2/Z2)
    pygame.draw.line(screen,(0,0,0),(X1,Y1),(X2,Y2))

def DrawCube():
    DrawLine(100,100,0,100,-100,0)
    DrawLine(100,100,-100,100,100,0)
    DrawLine(100,100,-100,100,-100,-100)
    DrawLine(100,-100,0,100,-100,-100)
    
    DrawLine(-100,-100,0,-100,-100,-100)
    DrawLine(-100,-100,100,100,-100,-100)
    DrawLine(-100,-100,0,100,-100,0)
    DrawLine(-100,-100,0,-100,100,0)
    
    DrawLine(-100,-100,-100,-100,100,-100)
    DrawLine(-100,100,-100,-100,100,-100)
    DrawLine(-100,100,-100,100,100,-100)
    DrawLine(-100,100,-100,-100,100,0)

while True:
    mouse = pygame.mouse.get_pos()
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    RotX = mouse[1]
    RotY = mouse[0]* -1
    try:
        DrawCube()
    except Exception as e:
        print(e)
    
    pygame.display.update()

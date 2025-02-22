import pygame,sys,random
from math import *
pygame.init()
screen=pygame.display.set_mode((640,480))
pixObj=pygame.PixelArray(screen)
def draw(pos,rad):
    a,b=pos
    for rasd in range(rad):
        ras=rad-rasd
        for i in range(360):
            angle=i
            x1=int(ras*sin(angle*pi/180))
            y1=int(ras*cos(angle*pi/180))
            try:pixObj[a+x1][b+y1]=(255,)*3#(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            except:pass
while True:
    screen.fill((0,0,0))
    mouse=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    draw((320,240),10)
    pygame.display.update()

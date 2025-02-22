#Walk in a cicrcle
import pygame,sys
from math import *
pygame.init()
screen=pygame.display.set_mode((640,480))

add=1
startX=300
startY=200
x=300
y=200
radius=100
angle=0
speed=2
length=1
CLOCK=pygame.time.Clock()
while True:
    #screen.fill((0,0,0))
        
    angle+=speed
    angle%=360
    x=startX+cos(angle*pi/180)*radius
    y=startY+sin(angle*pi/180)*radius*0.5 #타원
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.draw.rect(screen,(255,255,255),(x,y,10,10))
    pygame.display.update()
    CLOCK.tick(60)

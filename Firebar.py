#Firebar
import pygame,Globals
from math import *
Firebars = []
FirebarCenterImg = Globals.trans_img_size(pygame.image.load("Sprites/Blocks/FirebarCenter.png"),2)
FireImg = Globals.trans_img_size(pygame.image.load("Sprites/fireball.png"),2)
class firebar:
    def __init__(self,x,y,angle,length): 
        self.rect = FirebarCenterImg.get_rect()
        self.rect.topleft = (x,y)
        self.angle = angle
        self.length = length
        self.Fires = []
        #r = FireImg.get_rect()
        for i in range(self.length):
            self.Fires.append(FireImg.get_rect())
        Firebars.append(self)
    def Physics(self,mario):
        self.angle += 3
        s,c = sin(radians(self.angle)),cos(radians(self.angle))
        for n in range(len(self.Fires)):
            self.Fires[n].centerx = self.rect.centerx + 16 * n * c
            self.Fires[n].centery = self.rect.centery + 16 * n * s
            if self.Fires[n].colliderect(mario.rect):
                mario.Death()




def loop(screen,mario):
    for i in Firebars:
        if not mario.pause:
            i.Physics(mario)
        if Globals.IsRectOnScreen(i.rect,mario):
            screen.blit(FirebarCenterImg,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))
        for j in i.Fires:
            if Globals.IsRectOnScreen(j,mario):
                screen.blit(FireImg,(j.x - mario.scroll[0],j.y - mario.scroll[1]))

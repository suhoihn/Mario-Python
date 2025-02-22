import pygame,copy
from math import *
Platforms = []
class Platform:
    def __init__(self,lines,length):
        self.lines=lines
        self.length = length
        self.images=[]
        self.check=0
        self.speedx = 1
        self.speedy = 0
        self.yv=0
        self.tilt=0
        self.rect=pygame.Rect(0,0,50,20)
        self.type="Platform"
        Platforms.append(self)
        
        x,y = 0,0
        for i in range(0,self.length):
            if i == 0:
                self.images.append([pygame.transform.scale(pygame.image.load("Sprites/Platform/gold_platform_left.png"),(36,22)).convert_alpha(),(x,y)])
                x+=36
            elif i == self.length-1:
                self.images.append([pygame.transform.scale(pygame.image.load("Sprites/Platform/gold_platform_right.png"),(30,22)).convert_alpha(),(x,y)])
                x+=30
            else:
                self.images.append([pygame.transform.scale(pygame.image.load("Sprites/Platform/gold_platform_middle.png"),(30,22)).convert_alpha(),(x,y)])
                x+=30
        self.rect.width=x
        self.rect.height=22
        self.argument = "rect.centerx  >= self.targeted[0]"
        self.rect.center=lines[0][0]
        self.y=self.rect.y
        p1,p2 = lines[0]
        if p1[0] < p2[0]:
            self.targeted = p2
            self.mul = 1
        elif p1[0]  > p2[0]:
            self.targeted = p2
            self.mul = -1

    def f(self,x,d1,d2):
        y = (d2[1]-d1[1])/(d2[0]-d1[0])*(x-d1[0])+d1[1]
        return y
        
    def move(self,rect,p1,p2):
        if p1[0] < p2[0]:
            self.argument = "rect.centerx  >= self.targeted[0]"
            self.targeted = copy.deepcopy(p2)
                
        elif p1[0] > p2[0]:
            self.argument = "rect.centerx < self.targeted[0]"
            self.targeted = copy.deepcopy(p2)


        if eval(self.argument):#abs(self.f(rect.x,p2,p1) - p2[1] )<3:#abs(p2[0]-rect.centerx)<5 and abs(p2[1]-rect.centery)<5:
            self.check += 1
            if self.check == len(self.lines): return
            #rect.center = p2
            if p1[0] < p2[0]:
                rect.center = self.targeted
                #self.targeted = p2
                self.speedx = 2
                
            elif p1[0] > p2[0]:
                #print(rect.centerx, self.targeted[0],self.argument)

                rect.center = self.targeted
                self.speedx = -2
                
            
##            if p1[0] < p2[0]:
##       
##                rect.x += 1
##                
##            elif p1[0]  > p2[0]:
##       
##                rect.x -= 1
            
        else:
            if p1[0] < p2[0]:
                self.speedx = 2
            elif p1[0] > p2[0]:
                self.speedx = -2
            else:self.speedx = 0
            
            rect.centerx += self.speedx
            
            rect.centery = self.f(rect.centerx,p2,p1)
            #self.y = self.f(rect.x,p2,p1)
            #self.tilt=(p1[1]-p2[1])/(p1[0]-p2[0])*self.speedx
    def Physics(self,mario):
        self.speedy = self.rect.centery
        #self.speed += 0

        if self.check < len(self.lines):
            self.move(self.rect,*self.lines[self.check])
            self.yv = 0
        else:
        
            self.rect.x+=self.speedx
            self.yv += 0.4
            self.rect.y+=self.yv
            if self.yv > 15:
                self.yv =15
        self.speedy = self.rect.centery - self.speedy
     
class FallingPlatform:
    def __init__(self,X,Y,length,lim = (0.4,15)):#center
        self.images = []
        self.speedx = 0
        self.speedy = 0
        self.yv = 0
        self.length = length
        self.rect = pygame.Rect(0,0,50,22)
        self.type = "FallingPlatform"
        self.lim = lim#custom speed
        x,y = 0,0
        for i in range(0,self.length):
            if i == 0:
                self.images.append([pygame.transform.scale(pygame.image.load("Sprites/Platform/gold_platform_left.png"),(36,22)).convert_alpha(),(x,y)])
                x+=36
            elif i == self.length-1:
                self.images.append([pygame.transform.scale(pygame.image.load("Sprites/Platform/gold_platform_right.png"),(30,22)).convert_alpha(),(x,y)])
                x+=30
            else:
                self.images.append([pygame.transform.scale(pygame.image.load("Sprites/Platform/gold_platform_middle.png"),(30,22)).convert_alpha(),(x,y)])
                x+=30
        self.rect.width = x
        #self.rect.height=22

        self.rect.x, self.rect.y = X, Y
        self.falling = False
        Platforms.append(self)
    def Physics(self,mario):
        if self == mario.standingplatform:
            self.falling = True

        if self.falling:
            self.yv += self.lim[0]
            if self.yv > self.lim[1]:
                self.yv = self.lim[1]
            self.speedy = self.yv
            self.rect.y += self.yv
                
def loop(screen,mario):
    for i in Platforms:
        if i.type == "Platform": 
            for j in i.lines:
                pygame.draw.line(screen,(0,0,0),(j[0][0]-mario.scroll[0],j[0][1]-mario.scroll[1]),(j[1][0]-mario.scroll[0],j[1][1]-mario.scroll[1]),2)

        x,y = i.rect.x,i.rect.y
        for j in i.images:
            screen.blit(j[0],(j[1][0]+x-mario.scroll[0],y-mario.scroll[1]))
        if not mario.pause:
            i.Physics(mario)


import pygame,random,sys
from math import *
s1=random.randint(5,15)/10
s2=random.randint(5,15)/10
a=random.randint(0,640)
b=random.randint(0,640)
x=0
y=random.randint(0,300)
ypos=0
determining=[]
Render=[]
for i in range(0,640*100):
    if i%100==0:
        a+=1
        b+=abs(sin(radians(a)))
        y+=-tan(radians(45))#-0.1#sin(radians(a))*s1*cos(radians(b))*s2
        ypos=y
        determining.append(y+500)
        #y=480
        y=ypos
        Render.append(pygame.Rect(x,y+500,100,500))
        x+=1
class Character(object):
    def __init__(self):
        self.x=300
        self.y=0
        self.vel=0
        self.angle=90
        self.yv=0
        self.onslope=False
        self.rect=pygame.Rect(self.x,self.y,40,28)
        self.image=pygame.transform.scale(pygame.image.load("Sprites/Mario/A/small_m_still.png"),(28,40))
        self.scroll=0
    def move(self,yv):
        self.y+=yv
    def loop(self):
        global ypos,determining
        self.scroll += int((self.x-self.scroll-320)/2)
        self.rect=pygame.Rect(self.x,self.y,40,28)     
        self.yv+=0.5
        key=pygame.key.get_pressed()
        self.angle+=self.vel*3
        try:
            ypos=determining[round(self.x)]
        except:
            pass
        self.move(self.yv)
        self.onslope=False
        for i in Render:
            if self.rect.colliderect(i):
                self.onslope=True
                self.yv=0
                        
                if key[pygame.K_UP]:
                    self.yv=-10
                else:
                    self.y=ypos
        self.vel*=0.93
        self.x+=self.vel
                    
        if self.onslope:
            try:
                self.vel+=(determining[round(self.x)+1]-determining[round(self.x)])*0.75
            except:
                pass
        if key[pygame.K_LEFT]:
            self.vel-=1
        elif key[pygame.K_RIGHT]:
            self.vel+=1
                
##        if self.x<0:
##            self.x=0
##        if self.x>600:
##            self.x=600
        
        
mario=Character()          
screen=pygame.display.set_mode((640,480))
while True:
    screen.fill((0,0,128))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    for i in Render:
        pygame.draw.rect(screen,(0,255,128),(i.x-mario.scroll,i.y,i.width,500))
        #pygame.draw.rect(screen,(255,180,180),(i.x-mario.scroll,i.y+10,1,500))
    mario.loop()
    #screen.blit(pygame.transform.rotate(mario.image,mario.angle),(mario.x,mario.y-40))
    screen.blit(mario.image,(mario.x-mario.scroll,mario.y-30))
    pygame.display.update()
    
    
    

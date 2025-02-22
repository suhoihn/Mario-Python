#Slope test 3
import pygame,sys,random
import math

pygame.init()
slopes=[]
screen=pygame.display.set_mode((640,480))
class slope(object):
    def __init__(self,d1,d2):
        self.d1=d1
        self.d2=d2
        self.angle=math.atan2(d1[1]-d2[1],d1[0]-d2[0]) #Rad
        if (self.d2[1]-self.d1[1])/(self.d2[0]-self.d1[0])>0:
            self.heading='+'
        else:
            self.heading='-'
            
        slopes.append(self)
        
    def f(self,x):
        y = (self.d2[1]-self.d1[1])/(self.d2[0]-self.d1[0])*(x-self.d1[0])+self.d1[1]
        return y

    def update(self,d1,d2):
        self.angle=math.atan2(d1[1]-d2[1],d1[0]-d2[0])
        if (self.d2[1]-self.d1[1])/(self.d2[0]-self.d1[0])>0:
            self.heading='+'
        else:
            self.heading='-'
d=[300,0]
slope([300,200],[220,100])  
slope([800,100],[300,200])



player = pygame.Rect(200,0,50,50)
xv=0
yv=0
Onslope = False
SlippingDown=False
speed=[4,4]
allocated=None
CLOCK = pygame.time.Clock()
Nomoving=False
img=pygame.image.load("Sprites/Mario/small_m_still.png")
player.width=img.get_width()
player.height=img.get_height()

FallingRightAfterSlipping=False

def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
for i in slopes:
    print(math.degrees(i.angle))
#ought to apply FRICTION to slow the player down!
old=None
while True:
    
##    slopes[0].d1[1]+=0.5
##    slopes[1].d2[1]+=0.5
    print(speed[1])
    screen.fill((255,255,255))
    key = pygame.key.get_pressed()
    old=allocated
    for i in slopes:
        if player.midbottom[1] >= i.f(player.midbottom[0]) and min(i.d1[0],i.d2[0]) <= player.midbottom[0] <= max(i.d1[0],i.d2[0]): #플레이어의 오른쪽 아래 y좌표가 f(x) 그래프 안에 포함되어있는가? / 플레이어의 x좌표 값이 범위내에 있는가?
            if not player.centery >= i.f(player.centerx):
                Onslope=True
                allocated=i
        i.update(i.d1,i.d2)

    if old != allocated:
        for i in range(len(speed)): 
            speed[i]*=0.9
            if abs(speed[i])<1:
                SlippingDown=False
                
    yv += 0.5
    if key[pygame.K_UP] and Onslope:
        yv=-10
        Onslope=False
        SlippingDown=False
        
    if key[pygame.K_DOWN] and Onslope and not SlippingDown:
        SlippingDown = True
        speed=[0,0]

    if SlippingDown and Onslope:
        speed[0] += eval(allocated.heading+'1')*math.cos(abs(allocated.angle))/5
        speed[1] += eval(allocated.heading+'1')*math.cos(abs(allocated.angle))/5
       # print(speed)
    else:
        speed = [4,4]

    for i in range(len(speed)):
        if speed[i]>15:
            speed[i]=15
        elif speed[i]<-15:
            speed[i]=-15
            
    #print(SlippingDown and Onslope)
    if SlippingDown and not Onslope:
        player.x-=speed[0]

    FallingRightAfterSlipping = Onslope
    
    if Onslope:
        yv=0
        if not(min(allocated.d1[0],allocated.d2[0]) <= player.midbottom[0] <= max(allocated.d1[0],allocated.d2[0])):
            Onslope=False
        
        if not SlippingDown:
            if key[pygame.K_LEFT]:
                player.x -= speed[0]
                #player.y += speed[1]
            if key[pygame.K_RIGHT]:
                player.x += speed[0]
                #player.y -= speed[1]
            player.midbottom = (player.midbottom[0],allocated.f(player.midbottom[0]))
            
        else:
            player.midbottom = (player.midbottom[0]+speed[0],allocated.f(player.midbottom[0]))
            
    else:
        if key[pygame.K_LEFT]:
            player.x-=4
        if key[pygame.K_RIGHT]:
            player.x+=4

    if Onslope != FallingRightAfterSlipping:
        yv=speed[1]
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not Nomoving and not Onslope:
        player.y+=yv

    pygame.draw.rect(screen,(0,0,0),player)
    for i in slopes:
        pygame.draw.line(screen,(0,0,0),i.d1,i.d2)

    #screen.blit(img,player)
    pygame.display.update()
    CLOCK.tick(60)

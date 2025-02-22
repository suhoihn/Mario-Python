import pygame,sys,math
seesaws = []
class seesaw:
    def __init__(self,x,y,length):
        self.x = x
        self.y = y
        self.centerrect = pygame.Rect(0,y,20,20)
        self.centerrect.centerx = x
        self.length = length
        self.left = [x - self.length , y]
        self.right = [x + self.length , y]
        self.angle = 0
        self.rely = 0
        self.yspd = 0
        self.dy = 0
        self.f1x = 0
        self.f1y = 0
        self.f2x = 0
        self.f2y = 0

        self.image = pygame.transform.scale(pygame.image.load("Sprites/Blocks/POW.png"),(self.length * 2,10))
        
        self.marioison = False
        self.relx = 0 #실제 x좌표: i.x - i.length + relx
        seesaws.append(self)

    def dist(self,p1,p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    def Physics(self,mario):
        
        if True:
            self.relx = mario.rect.centerx - self.x + self.length#마리오 위치(x좌표), x좌표 차이
        else:
            self.relx = self.length
        
##        dy2 = 0.2 * (self.length - self.relx) / self.length
##        dy += dy2
        
        self.dy = 5 * (self.length - self.relx) / self.length#마리오가 멀리 있으면 빨리 휘게 함. 상수로 설정하면 마리오가 어디있든 같은 속도로 올라 가기만 함(같은 속도를 원하면 5 * self.relx가 필요함)
        #이후 식들은 직접 그림을 그려보면 이해하기 매우 편함
        if self.relx < self.x:
            self.f1x = self.x - self.left[0]
            self.f1y = self.left[1] - self.y
        else:
            self.f1x = self.right[0] - self.x
            self.f1y = self.y - self.right[1]
        

        self.f2y = self.f1y + self.dy
        try:
            self.f2x = math.sqrt((self.length ** 2) - (self.f2y ** 2))
        except: self.f2x = 1
        self.angle = math.atan2(self.f2y,self.f2x)
        if abs(math.degrees(self.angle)) <= 45 and self.marioison:
            self.left = (self.x - self.f2x,self.y + self.f2y)
            self.right = (self.x + self.f2x ,self.y - self.f2y)
        else:pass
            
        

        
        self.yspd = self.rely
        try: self.rely = -self.f2y / self.f2x * (self.x - self.length + self.relx - self.left[0]) + self.left[1]
        except: self.rely = 0
        self.yspd = self.rely - self.yspd
        

        
            
        
            

        

def loop(screen,mario):
    for i in seesaws:
        if not mario.GamePause:
            i.Physics(mario)
##        a = pygame.Rect(0,0,0,0)
##        a.center = i.centerrect.center
##        
##        #print((a.x - mario.scroll[0],a.y - mario.scroll[1])))
        #screen.blit(pygame.transform.rotate(i.image,math.degrees(i.angle)),(i.x - mario.scroll[0] - i.length,i.y - mario.scroll[1]))
        pygame.draw.polygon(screen,(255,255,255),((((i.centerrect.left + i.centerrect.right) / 2 - mario.scroll[0]),i.centerrect.top - mario.scroll[1]),(i.centerrect.left - mario.scroll[0],i.centerrect.bottom - mario.scroll[1]),(i.centerrect.right - mario.scroll[0],i.centerrect.bottom - mario.scroll[1])))
        pygame.draw.line(screen,(255,0,0),(i.left[0] - mario.scroll[0], i.left[1] - mario.scroll[1]),(i.right[0] - mario.scroll[0], i.right[1] - mario.scroll[1]),10)
        #pygame.draw.line(screen,(0,255,0),(i.x - i.length + i.relx - mario.scroll[0],0 - mario.scroll[1]),(i.x - i.length + i.relx - mario.scroll[0],480 - mario.scroll[1]),2)
        #pygame.draw.circle(screen,(0,0,255),(i.x - i.length + i.relx - mario.scroll[0],int(i.rely - mario.scroll[1])),10)

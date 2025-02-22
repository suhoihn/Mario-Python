import pygame,sys,math,Block,random
swings = []
rotatingplatforms = []
class rotatingplatform:
    def __init__(self,x,y,n,length = 150):
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Blocks/Bone.PNG"),(128,16)).convert_alpha()
        self.center = Block.QBlock(x+16,y+16,ContainmentType = "Coin")
        self.centerrect = self.center.rect
        self.timer = 0
        self.linelength = length
        self.platforms = []
        self.speedx = 0
        self.speedy = 0

        self.rect = pygame.Rect(0,0,0,0)#마리오가 현재 서있는 rect

        self.n = n
        for i in range(1,self.n+1):
            platform = pygame.Rect(0,0,128,16)
            platform.centerx = self.centerrect.centerx - math.cos(math.radians(360/self.n)) * self.linelength
            platform.centery = self.centerrect.centery + math.sin(math.radians(360/self.n)) * self.linelength
            self.platforms.append(platform)
        rotatingplatforms.append(self)
        

    def loop(self,mario):
        self.timer += 2
        for platform in self.platforms:
            og = platform.center
            if self.rect == platform:#platform in mario.hitlistsV:
                self.speedx = platform.centerx
                self.speedy = platform.centery
                self.rect = platform

            platform.centerx = self.centerrect.centerx - (math.cos(math.radians(self.timer) + (2 * math.pi / self.n) * (self.platforms.index(platform) + 1))) * self.linelength
            platform.centery = self.centerrect.centery + (math.sin(math.radians(self.timer) + (2 * math.pi / self.n) * (self.platforms.index(platform) + 1))) * self.linelength
            if self.rect == platform:#platform in mario.hitlistsV:
                self.speedx = platform.centerx - self.speedx
                self.speedy = platform.centery - self.speedy
        
class swing:
    def __init__(self,x,y,linelength):
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Blocks/Bone.PNG"),(128,16)).convert_alpha()
        self.center = Block.Block(x+16,y+16)
        self.centerrect = self.center.rect
        
        #self.centerrect.center = (x,y)
        self.timer = 0
        self.timer2 = 0
        self.timer3 = 0.05
        self.looping = True
        self.g = 0.1
        self.T = self.g
        self.linelength = linelength#350
        self.rect = pygame.Rect(0,0,128,16)
        self.rect.center = (x - self.linelength,y - self.linelength)
        #self.IsMarioOn = False
        swings.append(self)
    def distance(self,p1,p2):
        return math.sqrt(((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))

    def loop(self,mario):
        key = pygame.key.get_pressed()
        
        if abs(self.timer2) > 4:
            self.timer2 = 4 * abs(self.timer2)/self.timer2
        
        
        
        if mario.standingplatform == self:#self.rect in mario.hitlistsV and mario.rect.bottom < self.platform.bottom + abs(mario.yv):
            if self.rect.centerx < self.centerrect.centerx:
                self.timer3 = self.g - self.T * abs((self.rect.centery - self.centerrect.centery) / self.linelength)
            else:
                self.timer3 = -self.g + self.T * abs((self.rect.centery - self.centerrect.centery) / self.linelength)
            
        
            
            
        else:
            if self.timer2 > 0:
                self.timer2 -= 0.05
            if abs(self.timer2) < 1:
                self.timer2 = 0
            
            self.timer3 = 0
        
            
        
        self.timer2 += self.timer3
        self.timer += self.timer2
        self.speedx = self.rect.centerx
        self.speedy = self.rect.centery
        
        self.rect.centerx = self.centerrect.centerx - math.cos(math.radians(self.timer)) * self.linelength
        self.rect.centery = self.centerrect.centery + math.sin(math.radians(self.timer)) * self.linelength#(self.platform.centery - self.centerrect.centery) / self.distance((self.centerrect.center),(self.platform.center))# * self.linelength
        self.speedx = self.rect.centerx - self.speedx
        self.speedy = self.rect.centery - self.speedy

def loop(screen,mario):
    for i in swings:
        pygame.draw.line(screen,(255,0,0),(i.rect.centerx - mario.scroll[0],i.rect.centery - mario.scroll[1]),(i.centerrect.centerx - mario.scroll[0],i.centerrect.centery - mario.scroll[1]),5)
        screen.blit(i.image,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))
        if not mario.GamePause:
            i.loop(mario)
    for i in rotatingplatforms:
        for j in i.platforms:
            screen.blit(i.image,(j.x - mario.scroll[0],j.y - mario.scroll[1]))
        if not mario.GamePause:
            i.loop(mario)
        

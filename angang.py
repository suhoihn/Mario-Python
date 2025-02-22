import pygame,sys,math

screen = pygame.display.set_mode((640,480))
ground = []

class Player:
    def __init__(self,x,y):        
        self.rect = pygame.Rect(x,y,32,32)
        
        self.xv = 0
        self.yv = 0
        self.movement = [0,0]
        
        self.actualYspd = 0
        
        self.standingplatform = None
        
        self.collision = {"top":False,"bottom":False}
    
    
    def collision_check(self):
        self.collision = {"top":False,"bottom":False}

#-------X collision
            
        if self.standingplatform != None:
            self.movement[0] += self.standingplatform.vec[0]#If the platform moves horizontally, it moves with the same x speed.
          
        self.rect.x += math.ceil(self.movement[0])
        hit_list = []
        for i in ground:
            if self.rect.colliderect(i):
                hit_list.append(i)
                
        for i in hit_list:
            for j in range(abs(math.ceil(self.movement[0]))):
                if self.rect.colliderect(i.rect):
                    self.rect.x += abs(self.movement[0])/self.movement[0] * -1

#-------Y collision
                    
        self.actualYspd = 0 #This variable holds the speed of the platform that the player is on.
        
        if self.standingplatform != None:
            self.rect.y += self.standingplatform.vec[1]
            self.actualYspd = self.standingplatform.vec[1]
          
        self.rect.y += math.ceil(self.movement[1])
        hit_list = []   
        for i in ground:
            if self.rect.colliderect(i.rect):
                hit_list.append(i)

        self.standingplatform = None
        for i in platforms:
            if self.rect.colliderect(i.rect):
                self.standingplatform = i#Detects the moving platform to move along with it when player is on it.
            
        for i in hit_list:
            if self.movement[1] > 0:
                self.collision["bottom"] = True

            if self.movement[1] < 0:
                self.collision["top"] = True
                
            if i == self.standingplatform:#This is needed to stick the player to the platform  
                pushY = self.movement[1]
            else:
                pushY = self.movement[1] + self.actualYspd
                
            for j in range(abs(math.ceil(pushY))):
                if self.rect.colliderect(i.rect):
                    self.rect.y += abs(pushY)/pushY * -1


            self.yv = 0



        
    def loop(self):
        self.movement = [0,0]
        self.yv += 0.5
        
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.xv = 5
        elif key[pygame.K_LEFT]:
            self.xv = -5

        
        if abs(self.xv) < 1:
            self.xv = 0

        self.xv *= 0.7

        if self.yv > 15:
            self.yv = 15

     
        self.movement[0] += self.xv
        self.movement[1] += self.yv

        self.collision_check()
        if self.collision["top"]:
            self.yv = 0
        if self.collision["bottom"]:
            if key[pygame.K_UP]:
                self.yv = -15
        
        
        
player = Player(0,0)
platforms = []
class moving_platform:
    def __init__(self,x,y,w,h,vec):
        
        self.vec = vec #2D vector that stores the velocity of the platform
        
        self.rect = pygame.Rect(x,y,w,h)
        
        ground.append(self)
        platforms.append(self)

    def loop(self):
        self.rect.x += self.vec[0]
        self.rect.y += self.vec[1]

        #Platforms bounce off the screen
        if self.rect.right > 640 or self.rect.left < 0:
            self.vec[0] *= -1
        if self.rect.bottom > 480 or self.rect.top < 0:
            self.vec[1] *= -1


class platform:
    def __init__(self,x,y,w,h):
        self.rect = pygame.Rect(x,y,w,h)
        ground.append(self)
        

platform(0,180,100,30)
moving_platform(0,180,1000,30,[0,3])

CLOCK = pygame.time.Clock()
FPS = 60
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    for i in platforms:
        i.loop()
        
    for i in ground:
        pygame.draw.rect(screen,(255,0,0),i.rect)
    
    player.loop()
    pygame.draw.rect(screen,(0,0,255),player.rect)
    
    pygame.display.update()
    CLOCK.tick(FPS)

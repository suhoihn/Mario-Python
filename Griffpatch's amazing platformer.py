import pygame,sys,math,random
screen = pygame.display.set_mode((640,480))
MapImage = pygame.transform.scale(pygame.image.load("모양 1.png").convert_alpha(),(640,480))
Map = pygame.mask.from_surface(MapImage)

pygame.init()

pygame.mixer.music.load("../새로운 시작/BGM/06 - Level Theme 2.mp3")
#pygame.mixer.music.play(-1)

Platforms = []
def ColMap(mask,pos):
    collide = False
    if Map.overlap(mask,pos):
        collide = True

    for i in Platforms:
        if i.mask.overlap(mask,(pos[0] - i.rect.x, pos[1] - i.rect.y)):
            collide = True
        
    return collide

GRAVITY = 1
JUMP_FORCE = -15
ACCELERATION = 10#1.5
RESISTANCE = 0.8
class Player:
    def __init__(self,x,y):
        self.image = pygame.image.load("Sprites/Mario/small_m_still.png")
        self.rect = self.image.get_rect()
        self.surface = pygame.Surface(self.rect.size).convert_alpha()
        self.rect.x = x
        self.rect.y = y

        self.mask = pygame.mask.from_surface(self.surface)
        self.speedx = 0
        self.speedy = 0
        self.last_value = 0
        self.touching = False
        self.falling = 0 #체공시간

        self.PlatformSpd = [0,0]

    def Slip(self):
        self.rect.x += 1
        self.rect.y += 2
        
        self.Check_touching_solid()
        if not self.touching:
            self.falling = 9#Prevent player from jumping
            self.speedx += 1
            return
            
        self.rect.x -= 2

        self.Check_touching_solid()
        if not self.touching:
            self.falling = 9
            self.speedx -= 1
            return
        
        self.rect.x += 1
        self.rect.y -= 2
        
            
    def CollideX(self):
        self.rect.y -= 1
        self.Check_touching_solid()
        if self.touching:#still inside the ground  
            self.rect.y -= 1#move more to check if it's a wall(없으면 기울기 상관없이 올라감)
            self.Check_touching_solid()
            if self.touching:#still inside the ground
                self.rect.y += 2#gives up and acts as a wall
                self.rect.x = self.last_value
                self.speedx = 0
                return
        self.Slip()
                
    def CollideY(self):
        self.rect.y = self.last_value
        if self.speedy < 0:#if hit ceiling
            self.speedy = 0
            return
        if self.falling > 0:#Only when just landed
            self.falling = 0
            self.Slip()
        self.speedy *= 0.8
       
        
    def Move_in_stepsX(self,steps):
        for i in range(steps):
            self.last_value = self.rect.x
            self.rect.x += int(self.speedx / steps)
            self.Check_touching_solid()
            if self.touching:
                self.CollideX()

    def Move_in_stepsY(self,steps):
        self.falling += 1
        for i in range(steps):
            self.last_value = self.rect.y
            self.rect.y += int(self.speedy / steps)#this is 1
            self.Check_touching_solid()
            if self.touching:
                self.CollideY()
                
    def Check_touching_solid(self):
        if ColMap(self.mask, (self.rect.x,self.rect.y)):
            self.touching = True
        else:
            self.touching = False
    
    def Fix_Collision_in_Direction(self,direction):#Prevent being stuck
        #direction is in (x,y)
        distance = 1
        for i in range(64):
            self.Check_touching_solid()
            if not self.touching:
                break
            self.rect.x += direction[0] * distance#Move until not colliding
            self.rect.y += direction[1] * distance

            direction[0] *= -1 #Flip 180 degrees
            direction[1] *= -1
            
            distance += 1

    def Find_Closest_Space(self,x,y,MAX):
        print("?")
        distance = 1#radius of the circle
        direction = 0
        n = 16#how many checks
        for i in range(MAX):
            #direction = 0
            for j in range(n):
                self.rect.x,self.rect.y = x,y

                tempX = distance * math.sin(math.radians(direction))
                tempY = distance * math.cos(math.radians(direction))
                #print(tempX,tempY)
                self.rect.x += tempX
                self.rect.y -= tempY

                #print(tempX,tempY)
                
                self.Check_touching_solid()
                if not self.touching:
                    return

                direction += 360 / n
                
            distance += 1
        self.rect.x,self.rect.y = x,y

         
    def HandlePlatform(self):
        self.rect.x += self.PlatformSpd[0]
        self.rect.y += self.PlatformSpd[1]
        
        self.Check_touching_solid()
        if self.touching:
            #self.Fix_Collision_in_Direction([0,-1])
            self.Find_Closest_Space(self.rect.x,self.rect.y,16)
            if self.touching:
                print("GAME OVER")
    def loop(self):
        global FPS

        self.HandlePlatform()
        
        key = pygame.key.get_pressed()
        #Controls - Up and Down
        if key[pygame.K_UP]:
            if self.falling < 3:
                self.speedy = JUMP_FORCE
        self.speedy += GRAVITY
        
        #Controls - Left and Right
        if key[pygame.K_LEFT]:
            self.speedx = -ACCELERATION

        if key[pygame.K_RIGHT]:
            self.speedx = ACCELERATION
        self.speedx *= RESISTANCE
        

        #print(self.speedx,self.speedy)
    
        
        self.Move_in_stepsX(int(abs(self.speedx)))
        self.Move_in_stepsY(int(abs(self.speedy)))

        #DEBUG
        if key[pygame.K_SPACE]:
            FPS = 1
        else:
            FPS = 60

        print(self.falling)
        
        
            
class Platform:
    def __init__(self,x,y,Type = 1):
        self.rect = pygame.Rect(x,y,100,32)
        self.surface = pygame.Surface(self.rect.size).convert_alpha()

        self.surface = pygame.image.load("diamondy.png")
        self.OGS = pygame.image.load("diamondy.png")
        self.mask = pygame.mask.from_surface(self.surface)

        if Type == 1:
            self.spd = [0,-5]
        elif Type == 2:
            self.spd = [1,0]
            
        self.lastPos = (0,0)

        self.angle = 0

        self.timer = 10
        self.type = Type
        Platforms.append(self)

    def loop(self):
        self.check(self.rect.topleft)
        self.lastPos = self.rect.topleft

    def check(self,newPos):
        if newPos[1] - self.lastPos[1] < 0:#여기서 무조건 라스트 포지션을 기반으로 플레이어와 접촉 검사를 하므로 플랫폼이 아무리 빨라도 붙어있을 수 있음
            self.rect.y -= 1
        else:
            self.rect.y = self.lastPos[1] - 1
            
        if self.mask.overlap(player.mask,(player.rect.x - self.rect.x, player.rect.y - self.rect.y)):#self.rect.colliderect(player.rect):
            player.PlatformSpd = [newPos[0] - self.lastPos[0], newPos[1] - self.lastPos[1]]#player.OnPlatform
            #print(random.randint(1,100))
            
        self.rect.topleft = newPos

        
    def animate(self):
        self.rect.x += self.spd[0]
        self.rect.y += self.spd[1]
        if self.type == 1:
            if self.rect.y > 350 or self.rect.y < 100:# and self.timer == 0:
                self.spd[1] *= -1

            self.angle += 1
            if self.timer > 0:
                self.timer -=1
            #self.spd = [0,0]
##            self.surface = pygame.transform.rotate(self.OGS,self.angle)
##            self.mask = pygame.mask.from_surface(self.surface)
        elif self.type == 2:
            if self.rect.x > 200 or self.rect.x < 0:# and self.timer == 0:
                self.timer = 100
                self.spd[0] *= -1
                
            if self.timer > 0:
                self.timer -=1
                
        
##            self.angle += 5
##            #self.spd = [0,0]
##            self.surface = pygame.transform.rotate(self.OGS,self.angle)
##            self.mask = pygame.mask.from_surface(self.surface)

Platform(50,100,1)
#Platform(150,200,2)

player = Player(150,0)
CLOCK = pygame.time.Clock()
FPS = 60
while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    player.PlatformSpd = [0,0]
    for i in Platforms:
        #i.animate()
        i.loop()#이 순서가 꼭 지켜져야함! 안그러면 self.check()에서 플랫폼을 1칸 위로 옮겨도 플레이어에 닿지 않을수도 있음!
        i.animate()
        screen.blit(i.surface,(i.rect.x,i.rect.y))
        #pygame.draw.rect(screen,(0,255,0),i.rect)

    player.loop()

    screen.blit(MapImage,(0,0))
    pygame.draw.rect(screen,(0,0,0),player.rect)

    pygame.display.update()
    CLOCK.tick(FPS)

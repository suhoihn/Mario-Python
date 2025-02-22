import pygame, sys
screen = pygame.display.set_mode((640,480))
Level = pygame.transform.scale(pygame.image.load("모양 1.png"),(640,480))
LevelMask = pygame.mask.from_surface(Level)
def LevelCollide(mask,pos):
    if LevelMask.overlap(mask,pos):         
        return True
    return False
def scroll():
    pass
class Player:
    def __init__(self,x,y):
        self.image = pygame.image.load("Sprites/Mario/small_m_crouch.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.TouchingGround = 1
        self.scrollx = 0
        self.scrolly = 0
        self.xv = 0
        self.yv = 0
        self.sliding = False
        self.frame1x = 0
        self.frame1y = 0
        self.LastGround = 0
        self.SlideSpeed = 0
        self.lastX = 0
        self.lastY = 0
        self.leftfootH = 0
        self.rightfootH = 0
        self.xscrolled = 0
        self.yscrolled = 0
        self.CanJumpOnGround = False

        self.heading = 1

        self.mask = pygame.mask.from_surface(self.image)

        

    def scroll(self,n):
        pass
    def eventloop(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.TouchingGround == 1:
                    self.sliding = True
                    if self.leftfootH + self.rightfootH < 4:
                        if round(self.xv) == 0:
                            self.SlideSpeed = 0
                        else:
                            if self.xv > 0:
                                self.SlideSpeed = 1
                            else:
                                self.SlideSpeed = -1
                    if self.leftfootH + self.rightfootH < 4 and abs(self.SlideSpeed) <= 1:
                        print("슥")

            if event.key == pygame.K_UP:
                if not self.CanJumpOnGround:
                    self.CanJumpOnGround = True
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                if abs(self.leftfootH - self.rightfootH) < 2:
                    self.sliding = False
    def Physics(self):
        key = pygame.key.get_pressed()

        if self.leftfootH - self.rightfootH > 0:
            self.SlideSpeed *= -1

        if abs(self.leftfootH - self.rightfootH) < 2:
            self.SlideSpeed += -self.SlideSpeed / 10

        elif abs(self.leftfootH - self.rightfootH) > self.SlideSpeed:
            self.SlideSpeed += abs(self.leftfootH - self.rightfootH) / 10

        if self.SlideSpeed > 10:
            self.SlideSpeed = 10

        if self.leftfootH - self.rightfootH > 0:
            self.SlideSpeed *= -1



            
        
        self.frame1x = self.rect.x
        self.frame1y = self.rect.y
        if self.sliding and self.LastGround == 1:
            self.xv = self.SlideSpeed
        else:
            if key[pygame.K_LEFT]:
                self.xv += (-6 - self.xv) / 8
                self.heading = -1
                
            elif key[pygame.K_RIGHT]:
                self.xv += (6 - self.xv) / 8
                self.heading = 1
                
            else:
                if self.LastGround == 1:
                    self.xv += -self.xv / 8
                else:
                    self.xv += -self.xv / 32
            self.SlideSpeed = self.xv
            
        if key[pygame.K_UP]: #누르는 만큼 높이 조정
            self.yv += 1
        else:
            self.yv += 1.5
            
        if self.yv > 15:
            self.yv = 15

        self.rect.x += self.xv
        if round(self.xv * 100) / 100  != 0:
            self.lastX = round(self.xv * 100)
            
        if round(self.yv * 100) / 100  != 0:
            self.lastY = round(self.yv * 100)

        if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
            self.xmoveback()
            if abs(self.xv) > 0.1:
                self.xslope()
        if self.TouchingGround == 0 and self.yv > 0:
            if self.LastGround == 1:
                self.CheckForGround()

        self.rect.y += self.yv
        if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
            self.ymoveback()

        if self.TouchingGround == 1:
            self.GroundAngle()
        else:
            self.leftfootH = 0
            self.rightfootH = 0

        self.xscrolled = 0
        self.yscrolled = 0
        
        if self.rect.x > 320 + 25:
            self.scroll(1)
        if self.rect.x < 320 - 25:
            self.scroll(2)
        if self.rect.y < 240 - 50:
            self.scroll(3)
        if self.rect.y > 240 + 50:
            self.scroll(4)

        if self.scrolly == 0 and self.rect.y > 240 + 190:
            pass # Death Motion

        scroll() #전역 함수
        self.LastGround = self.TouchingGround
        #self.OverallSpeed = ((self.rect.x - self.frame1x - self.xscrolled) + (self.rect.y - self.frame1y - self.yscrolled)) / 2

        if self.TouchingGround == 1:
            if self.sliding:
                if self.leftfootH + self.rightfootH < 4 and abs(self.SlideSpeed) <= 1:
                    #Crouch Animation
                    if not key[pygame.K_DOWN]:
                        self.sliding = False
                else:
                    pass #Slide Animation

                if self.SlideSpeed != 0:
                    if self.SlideSpeed > 0:
                        pass # Heading = 1
                    else:
                        pass # Heading = -1
                else:
                    pass
            else:
                pass #Run Animation

        else:
            if self.yv < 0:
                pass #Jump Animation
            else:
                if self.sliding:
                    pass #Slide Animation
                else:
                    pass #Crouch Animation
    
                
    def xmoveback(self):
        if round(self.xv * 1000) / 100 != 0:
            oldx = self.rect.x
            oldy = self.rect.y
            slopemoves = 0
            for i in range(50):
                if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                    self.rect.y -= 1
                    slopemoves += 1
                else:
                    break

            self.rect.x = oldx
            self.rect.y = oldy

            if slopemoves >= 15:
                slopemoves = 0
                for i in range(50):
                    if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                        self.rect.x += abs(self.lastX) / self.lastX * -1 / 4
                        slopemoves += 1
                    else:
                        break
                if slopemoves == 50:                    
                    self.rect.x = oldx
                    self.rect.y = oldy
            else:
                self.rect.x += abs(self.xv) / self.xv / -3 * slopemoves

    def xslope(self):
        oldx = self.rect.x
        oldy = self.rect.y
        slopemoves = 0
        if not LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
            self.rect.y -= 3
            if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                self.rect.x += abs(self.xv) / self.xv
                if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                    for i in range(6):#여기 이렇게 하는거 맞나 
                        if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                            
                            self.rect.y += 1
                            slopemoves += 1
                        else:
                            break
                    if slopemoves == 6:
                        self.rect.x = oldx
                        self.rect.y = oldy
                else:
                    self.rect.x -= 3
            else:
                self.rect.x -= 3
                self.rect.y += 3
                if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                    self.rect.x += abs(self.xv) / self.xv                    
                    if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                        for i in range(6):#여기 이렇게 하는거 맞나 
                            if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                                self.rect.y -= 1
                                slopemoves += 1
                            else:
                                break
                        if slopemoves == 6:
                            self.rect.x = oldx
                            self.rect.y = oldy
                    else:
                        self.rect.x -= 3
                else:
                    self.rect.y -= 3
    def ymoveback(self):
        key = pygame.key.get_pressed()
        
        oldx = self.rect.x
        oldy = self.rect.y
        slopemoves = 0
        for i in range(100):
            if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                self.rect.y += abs(self.lastY) / self.lastY * -1# / 4
                slopemoves += 1
            else:
                break
                

        if slopemoves == 100:
            self.rect.x = oldx
            self.rect.y = oldy
        else:
            if self.yv < 0:
                self.TouchingGround = 2
                #self.CheckBlock()
            else:
                self.TouchingGround = 1

            if key[pygame.K_UP]:#and abs(self.lastY) / self.lastY == -1 and self.CanJumpOnGround:
                oldx = self.rect.x
                oldy = self.rect.y
                self.yv = -15
                #self.PlayerJump()
                self.rect.y -= 3
                self.CanJumpOnGround = False
                if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)): 
                    self.rect.x = oldx
                    self.rect.y = oldy
                else:
                    self.sliding = False
                        
    def GroundAngle(self):
        oldx = self.rect.x
        oldy = self.rect.y
        r = self.rect.right
        self.rect.width = 2
        uptimes = 0
        for i in range(12):
            if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                break
            else:
                self.rect.y += 1
                uptimes += 1
        self.leftfootH = uptimes
        if uptimes == 12:
            leftfootH = 0
        self.rect.x = oldx
        self.rect.y = oldy
        uptimes = 0
        self.rect.right = r
        for i in range(12):
            if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                break
            else:
                self.rect.y += 1
                uptimes += 1
            
        self.rightfootH = uptimes
        if uptimes == 12:
            rightfootH = 0
        self.rect.x = oldx
        self.rect.y = oldy
        self.rect.width = 28
        

    def CheckForGround(self):
        oldx = self.rect.x
        oldy = self.rect.y
        slopemoves = 0
        for i in range(10):
            if LevelCollide(self.mask,(self.rect.x - self.scrollx, self.rect.y - self.scrolly)):
                self.rect.y += 1
                slopemoves += 1
            else:
                break
        if slopemoves == 10:
            self.rect.x = oldx
            self.rect.y = oldy
        else:
            self.TouchingGround = 1
                
        
                        
        
                            
        


mario = Player(100,50)
CLOCK = pygame.time.Clock()
while True:
    screen.fill((255,) * 3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        mario.eventloop(event)
    mario.Physics()
    screen.blit(mario.image,(mario.rect.x,mario.rect.y))
    screen.blit(Level,(0,0))
    pygame.display.update()
    CLOCK.tick(60)
    

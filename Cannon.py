#Cannon
import pygame,random,Globals,Effects
Cannons = []
CannonBallImg = pygame.transform.scale(pygame.image.load("Sprites/Cannon/cannonball.png"),(36,32)).convert_alpha()
class cannon:
    class CannonBall:
        def __init__(self,heading,Cannon):
            self.yv = 0
            self.state = "Normal"
            self.Cannon = Cannon
            self.heading = heading

            self.IsinYoshiMouth = False
                
            #self.image = CannonBallImg
            self.rect = CannonBallImg.get_rect()
            self.rect.topleft = Cannon.rects[0].topleft
            Cannon.CannonBalls.append(self)
            
        def Physics(self,mario):
            for i in mario.Fireballs:
                if self.rect.colliderect(i.rect) and not i.blocked:
                    if self.state == "Normal":
                        if mario.MegamanMode:
                            i.blocked = True
                            pygame.mixer.Sound("Sounds/11 - Dink.wav").play()
                        else: 
                            Effects.Effect(self.rect.centerx,self.rect.centery,2,particles = False)
                            mario.Fireballs.remove(i)

            if self.IsinYoshiMouth:
                pass
            else:
                if -self.rect.width < self.rect.x - mario.scroll[0] < Globals.SW: #대포가 마리오 시선 안에 들어갔는지
                    self.rect.x += self.heading * 4
                    if self.rect.colliderect(mario.rect) and self.state != "Dead":
                        if mario.movement[1] > 0 and mario.rect.y+mario.rect.height/4<= self.rect.y and not mario.starman:
                            self.state="Dead"
                            pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()
                            mario.combo += 1
                            if mario.combo > 8:
                                mario.combo = 8
                                mario.life += 1
                            mario.jumpable=True
                            mario.jumping=False
                            mario.yv=-10
                        else:
                            mario.Death()
                        
                    if self.state == "Dead":
                        self.yv += 0.5
                    self.rect.y += self.yv
                else:
                    self.remove()

            if (mario.starman and self.rect.colliderect(mario.rect)) and self.state != "Dead":
                pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()
                mario.combo += 1
                if mario.combo > 8:
                    mario.combo = 8
                    mario.life += 1

                
                self.state = "Dead"
            
            
        def remove(self):
            self.Cannon.CannonBalls.remove(self)
    def __init__(self,x,y,length):
        self.x = x
        self.y = y
        self.timer = 0
        self.length = length
        self.rects = []
        self.rect = pygame.Rect(x,y,32,32 * length)
        self.CannonBalls = []
        for i in range(length):
            self.rects.append(pygame.Rect(self.x,self.y + 32 * i,32,32))
        Cannons.append(self)

    def Physics(self,mario):
        self.timer+=1
        if abs(mario.rect.centerx - (self.x + 16)) > 32 + 3:#대포가 마리오랑 가까울때만 발사
            if self.timer % 209 == 0:
                self.timer = random.randint(0,50)
                if mario.rect.centerx < self.x + 16:
                    self.CannonBall(-1,self)
                else:
                    self.CannonBall(1,self)
                pygame.mixer.Sound("Sounds/smash.wav").play()

TopImg = pygame.transform.scale(pygame.image.load("Sprites/Cannon/cannon1.png"),(32,32)).convert_alpha()
MiddleImg = pygame.transform.scale(pygame.image.load("Sprites/Cannon/cannon2.png"),(32,32)).convert_alpha()
BottomImg = pygame.transform.scale(pygame.image.load("Sprites/Cannon/cannon3.png"),(32,32)).convert_alpha()
def loop(screen,mario):
    for i in Cannons:
        if not mario.pause:
            if Globals.IsRectOnScreen(i.rects[0],mario):
                i.Physics(mario)
        for j in range(i.length):
            if Globals.IsRectOnScreen(i.rects[j],mario):
                if j == 0:
                    screen.blit(TopImg,(i.rects[j].x - mario.scroll[0],i.rects[j].y - mario.scroll[1]))
                elif j == 1:
                    screen.blit(MiddleImg,(i.rects[j].x - mario.scroll[0],i.rects[j].y - mario.scroll[1]))
                else:
                    screen.blit(BottomImg,(i.rects[j].x - mario.scroll[0],i.rects[j].y - mario.scroll[1]))

##        for j in range(len(i.images)):
##            if Globals.IsRectOnScreen(i.rects[j],mario):
##                screen.blit(i.images[j],(i.rects[j].x - mario.scroll[0],i.rects[j].y - mario.scroll[1]))
                        
        for k in i.CannonBalls:
            if not mario.pause:
                k.Physics(mario)
            screen.blit(pygame.transform.flip(CannonBallImg,k.heading == 1,False),(k.rect.x-mario.scroll[0],k.rect.y-mario.scroll[1]))

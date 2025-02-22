import pygame,Globals,Enemy,random,Effects
LakituImages = [Globals.trans_img_size(pygame.image.load("Sprites/Lakitu/Lakitu1.png"),2),
                Globals.trans_img_size(pygame.image.load("Sprites/Lakitu/Lakitu2.png"),2),
                Globals.trans_img_size(pygame.image.load("Sprites/Lakitu/Lakitu3.png"),2),
                Globals.trans_img_size(pygame.image.load("Sprites/Lakitu/Lakitu4.png"),2),
                Globals.trans_img_size(pygame.image.load("Sprites/Lakitu/Lakitu5.png"),2)]

CloudImages = [Globals.trans_img_size(pygame.image.load("Sprites/Lakitu/Cloud1.png"),2),
               Globals.trans_img_size(pygame.image.load("Sprites/Lakitu/Cloud2.png"),2),
               Globals.trans_img_size(pygame.image.load("Sprites/Lakitu/Cloud3.png"),2),
               Globals.trans_img_size(pygame.image.load("Sprites/Lakitu/Cloud4.png"),2),
    ]
Clouds = []
class Cloud:
    def __init__(self,x,y,lakitu = None):
        self.image = CloudImages[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.lakitu = lakitu#None 이면 안 타고 있다는 소리
        self.riding = False
        Clouds.append(self)
        #Whos riding 이런거 만들어서 통일시킬까?
    def loop(self,mario):
        self.image = CloudImages[(Globals.GlobalTimer // 5) % 4]
        if self.riding:
            self.rect.centerx = mario.rect.centerx
            self.rect.centery = mario.rect.centery + 23

        if self.lakitu == None:
            if not self.riding and mario.rect.colliderect(self.rect) and mario.yv > 0 and not mario.RidingCloud:
                self.riding = True
                mario.RidingCloud = True
                mario.TheActualCloud = self
        else:
            self.rect.centerx = self.lakitu.rect.centerx
            self.rect.centery = self.lakitu.rect.centery + 18
Lakitus = []
class Lakitu:
    def __init__(self,x,y):
        self.image = LakituImages[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.xv = 0
        self.ThrowTimer = 0
        self.Cloud = Cloud(*self.rect.center,self)
        self.throw = False
        self.Dead = False
        self.yv = 0
        self.acc = random.uniform(0.15,0.3)
        Lakitus.append(self)

    def loop(self,mario):
        if self.Dead:
            self.yv += Globals.GRAVITY
            self.rect.y += self.yv
            if not Globals.IsRectOnScreen(self.rect,mario): Lakitus.remove(self)
        else:
            self.rect.x += self.xv
            if self.rect.centerx < mario.rect.centerx:
                self.xv += self.acc
            else:
                self.xv -= self.acc

            self.xv = min(max(self.xv,-7),7)

            if self.throw:
                if self.ThrowTimer < 10 * 3:
                    self.image = LakituImages[(self.ThrowTimer // 10) % 3 + 1]#1,2,3
                elif self.ThrowTimer == 30:
                    self.image = LakituImages[4]
                    Enemy.KoopaTroopa(*self.rect.center,Type = "Spiny",winged = False,Thrown = True)

                elif self.ThrowTimer == 60:
                    self.image = LakituImages[0]
                    self.ThrowTimer = 0
                    self.throw = False

            else:
                if self.ThrowTimer == 120:
                    self.ThrowTimer = 0
                    self.throw = True
            self.ThrowTimer += 1
            
            if self.rect.colliderect(mario.rect):
                if mario.movement[1] > 0 and mario.rect.bottom < self.rect.bottom:
                    mario.jumpable = True
                    mario.jumping = False
                    if mario.SpinJump:
                        pygame.mixer.Sound("Sounds/stomp2.wav").play()
                        mario.yv=-3
                        Lakitus.remove(self)
                        Effects.Effect(mario.rect.centerx,mario.rect.bottom,2,particles = True,TI = 2)
                    else:
                        self.Dead = True
                        self.Cloud.lakitu = None
                        mario.yv = -12
                        
                        #이걸 mario안에 함수로 만들자
                        pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()
                        mario.combo += 1
                        if mario.combo > 8:
                            mario.life += 1
                            mario.combo = 8
                else:
                    mario.Death()


        

        
        



def loop(screen,mario):
    for i in Lakitus:
        if not mario.pause:
            i.loop(mario)
        screen.blit(i.image,(i.rect.x - mario.scroll[0], i.rect.y - mario.scroll[1]))

    for i in Clouds:
        if not mario.pause:
            i.loop(mario)
        screen.blit(i.image,(i.rect.x - mario.scroll[0], i.rect.y - mario.scroll[1]))


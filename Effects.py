import pygame,Globals
from math import *
Effects = []
#MotionTimer를 global 변수로 만드는건 어떠신지요

KickImg = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_kick.png"),(32,32))
KickImgFlipped = pygame.transform.flip(pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_kick.png"),(32,32)),True,False)
SpJumpImg = []
for i in range(1,5):
    SpJumpImg.append(Globals.trans_img_size(pygame.image.load("Sprites/Effect/ef_spjump{}.png".format(i)),2))
    
SpJumpParticle = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_spjump_particle.png"),(16,16))

InvincibleParticles = []
for i in range(1,4):
    InvincibleParticles.append(Globals.trans_img_size(pygame.image.load("Sprites/Effect/ef_invincible{}.png".format(i)),2))

SkidParticles = []
for i in range(1,4):
    SkidParticles.append(Globals.trans_img_size(pygame.image.load("Sprites/Effect/ef_skid{}.png".format(i)),2))

CoinParticles = []
for i in range(1,12):
    CoinParticles.append(Globals.trans_img_size(pygame.image.load("Sprites/Effect/ef_coin{}.png".format(i)),0.5))

DebrisParticles = []
for i in range(1,7):
    DebrisParticles.append(Globals.trans_img_size(pygame.image.load("Sprites/Effect/ef_debris{}.png".format(i)),2))

class Effect:
    def __init__(self,x,y,Type,**args):
        self.type = Type
        if Type == 1:
            self.image = KickImg
        elif Type == 2:
            self.image = SpJumpImg[0]

            try:self.particles = args["particles"]
            except KeyError:self.particles = True
            try:self.TI = args["TI"]#Time Interval
            except KeyError:self.TI = 4
            
        elif Type == 3:
            self.image = SpJumpParticle
            self.direction = args["direction"]
            self.pos = [x,y]
        elif Type == 4:
            self.image = InvincibleParticles[0]

        elif Type == 5:
            self.image = SkidParticles[0]
    
        elif Type == 6:
            self.image = CoinParticles[0]
        elif Type == 7:
            self.image = DebrisParticles[0]
            self.xv = 3 * args["heading"]
            self.yv = -10
            
        self.MotionTimer = 0
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        Effects.append(self)

    def loop(self,mario):
        if self.type == 1:
            if self.MotionTimer == 0 or self.MotionTimer == 4: self.image = KickImg
            elif self.MotionTimer == 2 or self.MotionTimer == 6: self.image = KickImgFlipped

            if self.MotionTimer == 8:
                Effects.remove(self)
        elif self.type == 2:
            #이거 잘하면 한줄로 바꿀수 있다
            if self.MotionTimer == 0:
                self.image = SpJumpImg[0]
                if self.particles:
                    for i in range(4): Effect(self.rect.centerx + 16 * (2 * (i == 0 or i == 3) - 1), self.rect.centery + 16 * (2 * (i == 2 or i == 3) - 1),3,direction = 45 + i * 90)
                    
            elif self.MotionTimer == self.TI: self.image = SpJumpImg[1]
            elif self.MotionTimer == self.TI * 2: self.image = SpJumpImg[2]
            elif self.MotionTimer == self.TI * 3: self.image = SpJumpImg[3]
            elif self.MotionTimer == self.TI * 4: Effects.remove(self)
            
        elif self.type == 3:
            if self.MotionTimer == 8:
                Effects.remove(self)
            self.pos[0] += cos(radians(self.direction)) * 2
            self.pos[1] -= sin(radians(self.direction)) * 2

            self.rect.center = self.pos
        elif self.type == 4:
            if self.MotionTimer == 0:
                self.image = InvincibleParticles[0]
            elif self.MotionTimer == 2:
                self.image = InvincibleParticles[1]
            elif self.MotionTimer == 4:
                self.image = InvincibleParticles[2]
            elif self.MotionTimer == 6:
                Effects.remove(self)

        elif self.type == 5:
            if self.MotionTimer == 0:
                self.image = SkidParticles[0]
            elif self.MotionTimer == 4:
                self.image = SkidParticles[1]
            elif self.MotionTimer == 8:
                self.image = SkidParticles[2]
            elif self.MotionTimer == 12:
                Effects.remove(self)

        elif self.type == 6:
            #self.rect.center = self.FixedCenter
##            if self.MotionTimer == 0:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin1.png"),(8,8))
##            elif self.MotionTimer == 2:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin2.png"),(13,18))
##            elif self.MotionTimer == 4:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin3.png"),(18,18))
##            elif self.MotionTimer == 6:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin4.png"),(18,18))
##            elif self.MotionTimer == 8:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin5.png"),(18,27))
##            elif self.MotionTimer == 10:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin6.png"),(15,27))
##            elif self.MotionTimer == 12:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin7.png"),(15,24))
##            elif self.MotionTimer == 14:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin8.png"),(9,24))
##            elif self.MotionTimer == 16:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin9.png"),(8,12))
##            elif self.MotionTimer == 18:
##                self.image = pygame.transform.scale(pygame.image.load("Sprites/Effect/ef_coin10.png"),(2,2))
            if self.MotionTimer == 21:
                Effects.remove(self)
                

            self.image = CoinParticles[(self.MotionTimer // 2) % 11]
            #self.image = pygame.image.load("Sprites/Effect/ef_coin" +str(((self.MotionTimer // 2) % 10) + 1) + ".png")

##            if self.MotionTimer > 20:
##                Effects.remove(self)
        elif self.type == 7:
            self.rect.x += self.xv
            self.rect.y += self.yv
            self.yv += 1
            self.image = DebrisParticles[(self.MotionTimer // 2) % 6]
            if self.rect.top - mario.scroll[1] > 485:
                Effects.remove(self)

        self.MotionTimer += 1
            
        
        
def loop(screen,mario):
    for i in Effects:
        i.loop(mario)
        screen.blit(i.image,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))

import pygame,Block,Effects,Globals
Coins = []
RMemory = []

CoinImages =[]
for i in range(4):
    CoinImages.append(pygame.transform.scale(pygame.image.load("Sprites/Coin/coin"+str(i+1)+".png"),(16,32)).convert_alpha())

class coin:
    def __init__(self,x,y,yv = 0,center = (None,None),RegisteredBlock = None):
        self.rect = CoinImages[0].get_rect()
        if center == (None,None):
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.center = center
        
        self.yv = yv
        self.Pdependent = False
        if self.yv != 0:
            self.moving = True
        else:
            self.moving = False
            if RegisteredBlock == None:
                self.ActualBlock = Block.BreakableBlock(self.rect.x - self.rect.width / 2, self.rect.y, "ActiveWhenP")
            else:
                self.RegisteredBlock = RegisteredBlock
                self.Pdependent = True

        Coins.append(self)
    def remove(self):
        Coins.remove(self)
    def Physics(self,mario):            
        if self.moving:
            self.yv += 0.5
            if self.yv > 2:
                pygame.mixer.Sound("Sounds/coin.wav").play()
                mario.coin += 1
                Effects.Effect(*self.rect.center,6)
                Coins.remove(self)
            self.rect.y += self.yv
        else:
            if self.Pdependent:
                if mario.Pactivated:
                    if self.rect.colliderect(mario.rect):
                        Effects.Effect(*self.rect.center,6)
                        mario.coin += 1
                        pygame.mixer.Sound("Sounds/coin.wav").play()
                        Coins.remove(self)
                        self.RegisteredBlock.type = None
            else:
                if self.ActualBlock.type == None:
                    Coins.remove(self)

                if self.rect.colliderect(mario.rect):
                    Effects.Effect(*self.rect.center,6)
                    mario.coin += 1
                    pygame.mixer.Sound("Sounds/coin.wav").play()
                    Coins.remove(self)
                    self.ActualBlock.type = None


        
def loop(screen,mario):
    for i in Coins:
        if Globals.IsRectOnScreen(i.rect,mario):
            if i.moving or (i.Pdependent and mario.Pactivated) or (not i.Pdependent and not mario.Pactivated):
                if not mario.pause:
                    i.Physics(mario)
                #if not mario.Pactivated:
                screen.blit(CoinImages[(Globals.GlobalTimer // 5) % 4],(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
        
        else:
            Coins.remove(i)
            RMemory.append(i)
    for i in RMemory:
        if -i.rect.width <= i.rect.x - mario.scroll[0] <= 640 and -i.rect.height <= i.rect.y - mario.scroll[1] <= 480:
            RMemory.remove(i)
            Coins.append(i)
    #print(len(Coins),len(RMemory))

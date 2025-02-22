#Block
import pygame,Mushroom,Enemy,Vine,Globals,Coin,Effects
import math
Blocks = []
#투명블록 만들잨ㅋㅋ-> 만듦
temp_img = pygame.image.load("Sprites/Blocks/BreakableBlock1.png").convert_alpha()

BreakableBlockImgs = []
for i in range(1,4 + 1):
    BreakableBlockImgs.append(pygame.image.load("Sprites/Blocks/BreakableBlock{}.png".format(i)).convert_alpha())
UselessBlockImage = pygame.transform.scale(pygame.image.load("Sprites/Blocks/Wall_1.png"),(32,32)).convert_alpha()


def Spawn(Box,ContainmentType,mario):
    if ContainmentType == "Mushroom":
        Mushroom.Mushroom(Box)
    elif ContainmentType == "1up":
        Mushroom.Mushroom(Box,"1up")
    elif ContainmentType == "Feather":
        Mushroom.Feather(Box)
    elif ContainmentType == "FireFlower":
        Mushroom.FireFlower(Box)
    elif ContainmentType == "Star":
        Mushroom.Star(Box)
    elif ContainmentType == "MegamanPowerup":
        Mushroom.MegamanPowerup(Box)

    elif ContainmentType == "Coin":
        Coin.coin(0,0,center = Box.rect.center,yv = -8)
        
    elif ContainmentType == "FeatherR":#R: Relative
        if mario.state == "big": Mushroom.Feather(Box)
        elif mario.state == "small": Mushroom.Mushroom(Box)

            
    elif ContainmentType == "FireFlowerR":
        if mario.state == "big": Mushroom.FireFlower(Box)
        elif mario.state == "small": Mushroom.Mushroom(Box)

    if ContainmentType == "Vine":
        Vine.Head(Box)

class BreakableBlock:
    def __init__(self,x,y,Type = "BreakableBlock",ContainmentType = None):
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Blocks/BreakableBlock1.png"),(32,32)).convert_alpha()
        self.type = Type
        #self.oy = y#OriginalY
        self.dy = y#DisplayY
        self.yv = 0
        self.state = "normal"
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.idx = 0
        self.hit = False
        self.activate = False#For powerups
        self.ActivatedByShell = False

        self.ContainmentType = ContainmentType
        if ContainmentType == "Coin":
            self.CoinCounter = 1
        if ContainmentType == "10Coin":
            self.CoinCounter = 10
            self.ContainmentType = "Coin"

        #p가 눌리면 그 자리에 코인이 생성되도록 바꾸자
        #인자로 self를 넘겨서 remove할 수 있게
        if ContainmentType == None:
            if self.type != "ActiveWhenP":
                self.ManagingCoin = Coin.coin(0,0,center = self.rect.center,RegisteredBlock = self)



        Blocks.append(self)
    def Physics(self,mario):#self.rect in mario.hitlistsV
        if (self.rect in mario.hitlistsV or self.ActivatedByShell and not self.activate) and not self.hit:
            if mario.collision_types['top'] or self.ActivatedByShell:
                self.hit = True
                if mario.rect.centerx > self.rect.centerx:
                    self.hitFrom = 1
                else:
                    self.hitFrom = -1

                if self.ContainmentType != None:
                    self.yv = -3* (not InfiniteBlockMode)
                    if self.state == "normal":
                        self.dy -= 1* (not InfiniteBlockMode)
                        pygame.mixer.Sound("Sounds/smb_bump.wav").play()
                self.ActivatedByShell = False


            elif mario.collision_types['bottom']:
                if mario.state == "big" and mario.SpinJump and self.ContainmentType == None:
                    mario.yv = -5
                    mario.collision_types['bottom'] = False
                    pygame.mixer.Sound("Sounds/smw_break_block.wav").play()
                    if self.type == "ActiveWhenP":
                        self.type = None
                    else:
                        self.ManagingCoin.remove()

                    Effects.Effect(*self.rect.topright,7,heading = 1)
                    Effects.Effect(*self.rect.bottomright,7,heading = 1)
                    Effects.Effect(*self.rect.topleft,7,heading = -1)
                    Effects.Effect(*self.rect.bottomleft,7,heading = -1)
                    Blocks.remove(self)
                
            
        if self.state == "useless":
            self.hit = False
            self.image = UselessBlockImage
        elif self.hit:
            if self.ContainmentType == None:
                if self.idx >= 128: #이때부터 마리오에 닿았는지 검사 시작  
                    if self.rect.colliderect(mario.rect):#닿았을 때
                        self.idx += 1 #쉬지 않고 계속 빙빙 돌다가
                        if self.idx == 128 + 18:#원래대로 돌아오는 idx가 되면 
                            self.idx = 128 #루프가 되도록 초기화
                    elif self.idx >= 128 + 18:#마리오에 닿지 않고 idx가 80이 되면 도는거 정지
                        self.hit = False
                    else:#마리오에 닿지 않고 idx가 128 ~ 146일 때 idx 1씩 증가(이거 없으면 마리오가 닿을 때만 돎)
                        self.idx += 1
                else:
                    self.idx += 1

                oldpos = self.rect.centery
                if self.idx % 18 == 0:#너무 빠르고 이 라인들을 조금 더 간결하게 바꾸자
                    self.image = BreakableBlockImgs[0]
                elif self.idx % 18 == 3:
                    self.image = BreakableBlockImgs[1]
                elif self.idx % 18 == 6:
                    self.image = BreakableBlockImgs[2]
                elif self.idx % 18 == 9:
                    self.image = BreakableBlockImgs[3]
                elif self.idx % 18 == 12:
                    self.image = BreakableBlockImgs[2]
                elif self.idx % 18 == 15:
                    self.image = BreakableBlockImgs[1]
                self.rect.height = self.image.get_height()
                self.rect.centery = oldpos
            else:
                if self.dy < self.rect.y:
                    self.dy += self.yv
                    self.yv += 0.5
                else:
                    self.yv = 0
                    self.dy = self.rect.y
                    self.activate = True
                    self.hit = False
                    

                
            
            
        else:
            self.idx = 0
            oldpos = self.rect.centery
            self.image = BreakableBlockImgs[0]
            self.rect.height = self.image.get_height()
            self.rect.centery = oldpos

CloudImage = pygame.image.load("Sprites/Blocks/Cloud.png").convert_alpha()
class Cloud:
    def __init__(self,x,y):
        #self.image = CloudImage
        self.rect = CloudImage.get_rect()
        self.rect.x, self.rect.y = x, y
        self.type = "Cloud"
        Blocks.append(self)

BlockImage = pygame.transform.scale(pygame.image.load("Sprites/Blocks/ground_cement_brick.png"),(32,32)).convert_alpha() #16 16     
class Block:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.type = "cerment_brick"
        #self.image = BlockImage
        self.rect = BlockImage.get_rect()
        self.rect.topleft = (x,y)
        Blocks.append(self)

QBlockImages = []
for i in range(1,5):
    QBlockImages.append(pygame.transform.scale(pygame.image.load("Sprites/Blocks/questionBlock"+str(i)+".png"),(32,32)).convert_alpha())

InfiniteBlockMode = not True
class QBlock:
    def __init__(self,x,y,Invisible = False, ContainmentType = "Vine"):
        #Qblock 위로 튕기는거 이미지만 적용!
        self.x = x
        self.y = y
        self.Invisible = Invisible
        self.yv=0
        self.type="QBlock"
        self.state="Normal"
        self.width=32
        self.height=32
        self.activate=False
        self.hit = False
        self.ActivatedByShell = False

        self.rect = pygame.Rect(x,y,self.width,self.height)

        self.ContainmentType = ContainmentType
        if ContainmentType == "Coin":
            self.CoinCounter = 1
        if ContainmentType == "10Coin":
            self.CoinCounter = 10
            self.ContainmentType = "Coin"

        self.holded = False
        self.isInMario = False
        self.hitFrom = 0#-1: left, 1: right
        Blocks.append(self)
        
    def reload(self):
        Blocks.append(self)
        
    def Physics(self,mario):
        self.rect.width = 32
        if self.isInMario:
            if mario.rect.colliderect(self.rect):
                self.rect.width = 0
        
        for i in Enemy.KoopaTroopas:
            if not i.holded and i.rect.colliderect(self.rect):
                if i.yv < 0 and i.collision_types['top']:
                    self.activate=True
                    i.yv = 0
        key = pygame.key.get_pressed()
##        if (self.rect in mario.hitlistsH):
##            if key[pygame.K_s] and not mario.holding:# and False:#False없애면 블록을 들 수 있음
##                self.rect.width = 0
##                mario.holding = True
##                self.holded = True

        if self.holded:
            self.rect.width = 32
            
            mario.Holded_Object_Loop(self)
            self.y = self.rect.y
            self.rect.width = 0
            if not key[pygame.K_s]:
                self.rect.width = 0
                self.holded = False
                self.isInMario = True
                mario.holding = False
            
        if (self.rect in mario.hitlistsV and mario.collision_types['top'] and not self.activate and self.state == "Normal" or self.ActivatedByShell) and not self.hit:
            pygame.mixer.Sound("Sounds/smb_bump.wav").play()
            self.yv = -3 * (not InfiniteBlockMode)
            self.y -= 1 * (not InfiniteBlockMode)
            self.hit = True
            if mario.rect.centerx > self.rect.centerx:
                self.hitFrom = 1
            else:
                self.hitFrom = -1
            self.Invisible = False
            self.ActivatedByShell = False
            
        if self.hit:
            if self.y < self.rect.y:
                self.y += self.yv
                self.yv += 0.5
            else:
                self.yv = 0
                self.y = self.rect.y
                self.hit = False
                self.activate = True

OnOffState = "OFF"
OnOffSwitchImg = {"OFF1":pygame.image.load("Sprites/Blocks/OnOffBlock/OffSwitch1.png").convert_alpha(),
                  "OFF2":pygame.image.load("Sprites/Blocks/OnOffBlock/OffSwitch2.png").convert_alpha(),
                  "ON1":pygame.image.load("Sprites/Blocks/OnOffBlock/OnSwitch1.png").convert_alpha(),
                  "ON2":pygame.image.load("Sprites/Blocks/OnOffBlock/OnSwitch2.png").convert_alpha()}

class OnOffSwitch:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.yv=0
        self.type = "OnOffSwitch"
        self.state = "Normal"
        self.rect = pygame.Rect(x,y,32,32)
        self.timer = 0
        self.ActivatedByShell = False

        self.image = OnOffSwitchImg["OFF1"]
        
        Blocks.append(self)
    def Physics(self,mario):
        global OnOffState
        if (self.rect in mario.hitlistsV and mario.collision_types['top'] or self.ActivatedByShell):
            pygame.mixer.Sound("Sounds/switch.wav").play()
            if OnOffState == "OFF":
                OnOffState = "ON"
            elif OnOffState == "ON":
                OnOffState = "OFF"
        self.ActivatedByShell = False


OnOffBlockImg =[pygame.image.load("Sprites/Blocks/OnOffBlock/OnBlockTriggered.png").convert_alpha(),
               pygame.image.load("Sprites/Blocks/OnOffBlock/OnBlockUnTriggered.png").convert_alpha(),
               pygame.image.load("Sprites/Blocks/OnOffBlock/OffBlockTriggered.png").convert_alpha(),
               pygame.image.load("Sprites/Blocks/OnOffBlock/OffBlockUnTriggered.png").convert_alpha()]

class OnOffBlock:
    def __init__(self,x,y,state):
        self.image = OnOffBlockImg[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.state = state
        self.type = "OnOffBlock"
        Blocks.append(self)

    def Physics(self):
        global OnOffState
        
        a = int(self.state == "OFF")#0 ~ 1
        b = int(self.state != OnOffState)#0 ~ 1
        #만약 Onblock Untriggered를 원하면 a = 0, b = 1이 되므로 2a + b = 1, self.images[1]의 값이 나오게 됨(모든 경우에 관해 모두 작동함)

        self.image = OnOffBlockImg[a * 2 + b]
        
pygame.font.init()
def text_objects(text,size):
    textSurface=pygame.font.Font("Super-Mario-World.ttf", size).render(text,True,(255,255,255))
    return textSurface,textSurface.get_rect()

TextBlockImage = pygame.image.load("Sprites/Blocks/TextBlock.png").convert_alpha()
        
class TextBlock:
    def __init__(self,x,y,texts):
        self.texts = texts#list of texts
        self.type = "TextBlock"
        self.Surface = pygame.Surface((0,0))
                   
        self.rect = TextBlockImage.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x, self.y = 320,160
        self.CloseTimer = 0#3.14 / 2
        self.activated = False
        self.decrease = False
        
        Blocks.append(self)

    def Physics(self,mario):
        if self.rect in mario.hitlistsV and mario.collision_types['top']:
            self.activated = True
        if self.activated and not self.decrease:
            a = self.Surface.get_width()
            b = self.Surface.get_height()

            if self.CloseTimer < 3.14 / 2: #1/2pi
                self.CloseTimer += 0.1
            if self.CloseTimer > 3.14 / 2:
                self.CloseTimer = 3.14 / 2
                mario.GamePause = True
                mario.pause = True
                mario.WaitForB = True
                mario.TargetText = self
            self.Surface = pygame.Surface((int(384 * math.sin(self.CloseTimer)), int(192 * math.sin(self.CloseTimer))))
            for idx,text in enumerate(self.texts):
                TS,TR = text_objects(text,16)
                TR.x, TR.y = 5,32 * idx + 8
                self.Surface.blit(TS,TR) 
            self.x += (a - self.Surface.get_width()) / 2
            self.y += (b - self.Surface.get_height()) / 2
        elif self.decrease:
            a = self.Surface.get_width()
            b = self.Surface.get_height()
            
            if self.CloseTimer > 0:
                self.CloseTimer -= 0.1
            if self.CloseTimer < 0:
                self.CloseTimer = 0
                self.decrease = False
            self.Surface = pygame.Surface((int(384 * math.sin(self.CloseTimer)), int(192 * math.sin(self.CloseTimer))))
            for idx,text in enumerate(self.texts):
                TS,TR = text_objects(text,16)
                TR.x, TR.y = 5,32 * idx + 8
                self.Surface.blit(TS,TR) 
            self.x += (a - self.Surface.get_width()) / 2
            self.y += (b - self.Surface.get_height()) / 2

#QBlock 이미지 밖으로 빼내서 저장하자
#무언가를 spawn할 때 그냥 그 즉시 스폰하자. 미리 대기 시켜 놓으면 메모리 낭비임
idx=0
def IsRectOnscreen(rect,mario):
    return -rect.width < rect.x - mario.scroll[0] < Globals.SW and -rect.height < rect.y - mario.scroll[1] < Globals.SH
def loop(screen,mario):
    global idx
    if not mario.pause: #pause하면 모양이 바뀌면 안됨
        idx += 1
    k = ((Globals.GlobalTimer % 40) < 20) + 1
    for i in Blocks:
        if -i.rect.width - 32 * 10 <= i.rect.x-mario.scroll[0] <= 640 + 32 * 10 or True:
            if i.type == "cerment_brick":
                if IsRectOnscreen(i.rect,mario):
                    screen.blit(BlockImage,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))
                
            elif i.type == "ActiveWhenP":
                if mario.Pactivated:
                    i.Physics(mario)
                    if IsRectOnscreen(i.rect,mario):
                        screen.blit(i.image,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))
            elif i.type == "QBlock":
                i.Physics(mario)
                if i.activate and i.state != "useless":
                    if i.ContainmentType == "Coin":
                        if i.CoinCounter != 0:
                            i.CoinCounter -= 1 * (not InfiniteBlockMode)
                            i.activate = False
                            if i.CoinCounter == 0:
                                i.state = "useless"
                            Spawn(i,i.ContainmentType,mario)
                    else:
                        Spawn(i,i.ContainmentType,mario)
                        if not InfiniteBlockMode:
                            i.state = "useless" 
                        i.activate = False
                if not i.Invisible:
                    if IsRectOnscreen(i.rect,mario):
                        if i.state == "Normal":
                            screen.blit(QBlockImages[(idx // 5) % 4],(i.rect.x - mario.scroll[0],i.y - mario.scroll[1]))
                        else:
                            screen.blit(UselessBlockImage,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))


            elif i.type == "BreakableBlock":
                if i.ContainmentType != None or not mario.Pactivated:
                    i.Physics(mario)

                if i.activate and i.state != "useless":

                    if i.ContainmentType == "Coin":
                        if i.CoinCounter != 0:
                            i.CoinCounter -= 1 * (not InfiniteBlockMode)
                            i.activate = False
                            if i.CoinCounter == 0:
                                i.state = "useless"
                            Spawn(i,i.ContainmentType,mario)
                    else:
                        Spawn(i,i.ContainmentType,mario)
                        if not InfiniteBlockMode:
                            i.state = "useless" 
                        i.activate = False
                        
                if IsRectOnscreen(i.rect,mario):
                    if i.ContainmentType == None:
                        if not mario.Pactivated:
                            screen.blit(i.image,(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
                    else:
                        screen.blit(i.image,(i.rect.x-mario.scroll[0],i.dy-mario.scroll[1]))

            elif i.type == "OnOffSwitch":
                i.Physics(mario)
                if IsRectOnscreen(i.rect,mario):
                    screen.blit(OnOffSwitchImg[OnOffState + str(k)],(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
            elif i.type == "OnOffBlock":
                i.Physics()
                a = 2 * (i.state != OnOffState)
                if IsRectOnscreen(i.rect,mario):
                    screen.blit(i.image,(i.rect.x-mario.scroll[0] + a,i.rect.y-mario.scroll[1] + a))

            elif i.type == "Cloud":
                if IsRectOnscreen(i.rect,mario):
                    screen.blit(CloudImage,(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))

            elif i.type == "TextBlock":
                i.Physics(mario)
                screen.blit(i.Surface,(i.x,i.y))#-mario.scroll[0] ,i.y-mario.scroll[1]))
                if IsRectOnscreen(i.rect,mario):
                    screen.blit(TextBlockImage,(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
            else: 
                Blocks.remove(i)


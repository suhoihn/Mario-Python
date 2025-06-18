import pygame,sys,os,copy,random
from pygame.locals import *
#PYTHON 꿀팁
#float.is_integer() (ex. 1.0.is_integer() -> True)
#isinstance(value,type) (ex. isinstance("a",str) -> True)
#

SW,SH = 640, 480

os.environ["SDL_VIDEO_CENTERED"] = "1"
#만약에 도는 블록에 움직이는 버섯이 끼는 상황이 발생할 수 있음

flag = pygame.HWSURFACE | pygame.DOUBLEBUF# | pygame.FULLSCREEN | pygame.SCALED

screen2=pygame.display.set_mode((SW,SH),flag,16)
const = 1
screen = pygame.Surface((int(SW/const),int(SH/const)))#.convert_alpha()

#뒤집힌 슬로프 collision_types 확인
#RMemory를 Global에 넣을까?
const = 1#/1.5
#pygame.mixer.pre_init(44100, 32, 2, 1024)
pygame.init()

PLAYTRIPLEJUMPSOUND = False

from Globals import SW,SH

import Globals
import ROM

ROM.LoadLevel(Globals.Lvidx)
import Coin,Goal,math,cape,Spike,Spring,와리가리,seesaw
import BackGround,Ground,Enemy,Thwomp,Pipe,Cannon,Block,Mushroom,Platform,Things,Spiny,Yoshi,Vine,Effects,Galumba,Firebar,Lakitu

import importlib

import tracemalloc
#Mario Holded Objects 라 해서 함수로 던지기 뭐시기 하기
#Mario Holded Object라고 해서 파이프 들어가도 유지할 수 있게 하자
#(혹시 가능하면 다시 돌아왔을 때 리스폰 안되게 하는것도 생각해보자)

#별 먹었을때 pspeed가 유지가 안됨 -> 고치자 -> 고쳤다

#아니 쉘 던질 때 모션이나 소리좀 만들자
#디스플레이 리스트 만들어서 하는 것도 괜찮은 듯 -> 뭐야 이거 예전에도 생각했던거네 이거 나중에 그리는거 복잡하게 하지 말고 이걸로 통일화 시켜버리자

###  꿀팁s  ###
#만약 마리오가 movement[0],[1]만큼 움직여도 껴 있는 경우, 벽 취급을 중단해서 마리오가 빠져나올 수 있게 해야 한단 마리오
#마리오가 빠른 속도(15)로 떨어지면 물체를 통과할 수 도 있다. 그럴 때는 일단 yv만큼 욺겨서 통과 판정을 받을 때, for i in range(abs(int(yv)))를 사용해서 정확한 위치를 찾아야 한단 루이지
marios = []


global tm
#마리오가 플랫폼에 걸치면 이상해짐 -> 고치자
deathimage = pygame.transform.scale(pygame.image.load("deathX.png"),(30,35)).convert_alpha()

tm=0

def blit_alpha(target, source, location, opacity):
    if opacity == 255:
        target.blit(source,location)
    else:
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
print("Objective : Collect 100 lives or clear this game")
#"Globals.BGM/새로운 녹음 17ss.MP3"
CLOCK = pygame.time.Clock()
pygame.mixer.music.load(Globals.BGM)
#pygame.mixer.music.play(-1)


faster= 1
Temp=0
idx=0
Target = 1
again = 0
ScreenPos = (0,0)
old = None
stime = 0


# === CONSTANTS ==== #
MMWalkSpd = 4 * faster

JUMPPOWER = 17.5
ACC = 0.15# * 10
MaxPSpd = 6.5 * faster
#12 in older versions(cannot clear "The Doom of P-Switch")
#10 in newer version(more managable speed)
MaxRunSpd = 5.5 * faster
#10 in older version
#8 in newer version
WalkingSpd = 2.5 * faster
easteregg = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h]#ADADVVSS -> LRLRZZYY


###  FATAL BUGs ####
#pswitch 안으로 가서 인접한 스위치에 닿으면 그냥 밟아짐 -> fixed
#pswitch 밟고 파이프 들어가면 뭔가 겁나 이상함 -> OK -> NOT OK AGAIN!!!!
#pswitch위에 억지로 고정시키면 가끔 벽/땅 사이로 낀다
#pswitch가 머리 위로 2개 박히면 하나가 알아서 눌린다 -> fixed
#seesaw에서 이상한 버그 많이 생긴다
#LvTrans가 있는 파이프에 물건을 들고 가면 없어지는데 이걸 어케 해결할거지?

##with open("deaths.txt","r+") as f:
##    DeathSpots = eval(f.readline())
##    f.close()
##print(len(DeathSpots))

ShakeVar = 0
beftarget = 0
target_y = 0
FPS = 0

sp_clearedLevels = 0#For spring fair


ExplosionParticles = []
ExplosionImage = (
    Globals.trans_img_size(pygame.image.load("Sprites/Explosion/sprExplosion_0.png"),1),
    Globals.trans_img_size(pygame.image.load("Sprites/Explosion/sprExplosion_1.png"),1),
    Globals.trans_img_size(pygame.image.load("Sprites/Explosion/sprExplosion_2.png"),1),
    Globals.trans_img_size(pygame.image.load("Sprites/Explosion/sprExplosion_3.png"),1),
    Globals.trans_img_size(pygame.image.load("Sprites/Explosion/sprExplosion_4.png"),1))
from timeit import default_timer as timer

startTime = timer()

class ExplosionParticle:
    def __init__(self,pos,angle,speed):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.rect = ExplosionImage[0].get_rect()
        self.rect.center = self.pos
        ExplosionParticles.append(self)

    def loop(self,mario):
        self.pos[0] += math.cos(math.radians(self.angle)) * self.speed
        self.pos[1] -= math.sin(math.radians(self.angle)) * self.speed
        if not Globals.IsRectOnScreen(self.rect,mario):
            ExplosionParticles.remove(self)
        self.rect.center = self.pos
        
def firemario(surf,mario):
    m = surf.copy()
    if mario.player == "t":
        for i in range(m.get_height()):
           for j in range(m.get_width()):
                if m.get_at((j,i)) == (140,10,80):
                    m.set_at((j,i),(99,17,0))
                    
                elif m.get_at((j,i)) == (255,255,255):
                    m.set_at((j,i),(255,150,238))
                    
                elif m.get_at((j,i)) == (230,20,110):
                    m.set_at((j,i),(191,34,0))
                    
                elif m.get_at((j,i)) == (255,100,180):
                    m.set_at((j,i),(255,62,20))
                    
                elif m.get_at((j,i)) == (230,200,255):
                    m.set_at((j,i),(255,99,202))
                

        
    elif mario.player == "m":
##                    for i in range(m.get_height()):
##                for j in range(m.get_width()):

        if mario.Mario1:
            for i in range(m.get_height()):
                for j in range(m.get_width()):
                    c = m.get_at((j,i))
                    
                    if c == (181,49,32):
                        m.set_at((j,i),(247,216,165))
                    if c == (107,109,0):
                        m.set_at((j,i),(181,49,32))

        elif mario.Mario3:
            for i in range(m.get_height()):
                for j in range(m.get_width()):
                    if m.get_at((j,i)) == (248,56,0):
                        m.set_at((j,i),(232,157,52))
                    if m.get_at((j,i)) == (0,0,0):
                        m.set_at((j,i),(178,50,38))
        else:
            for i in range(m.get_height()):
                for j in range(m.get_width()):
                    if m.get_at((j,i)) == (80,0,0):
                        m.set_at((j,i),(71,71,71))
                        
                    elif m.get_at((j,i)) == (248,64,112):
                        m.set_at((j,i),(247,247,247))
                        
                    elif m.get_at((j,i)) == (176,40,96):
                        m.set_at((j,i),(216,160,56))
                        
                    elif m.get_at((j,i)) == (248,112,104):
                        m.set_at((j,i),(247,118,25))
                        
                    elif m.get_at((j,i)) == (32,48,136):
                        m.set_at((j,i),(0,0,64))
                        
                    elif m.get_at((j,i)) == (64,128,152):
                        m.set_at((j,i),(184,0,0))
                        
                    elif m.get_at((j,i)) == (128,216,200):
                        m.set_at((j,i),(247,0,0))
        
    return m

ColorTable = {
    "Normal":[(0,232,216),(0,112,236)],
    "Fire":[(240,188,60),(216,40,0)],
    "Mario":[(248,64,112),(128,216,200)][::-1],
    "Toadette":[(248,248,248),(255,100,180)],
    "Mysterious":[(64,64,64),(0,0,0)]}

def MM_ColorChange(surf,colorlist):
    m = surf.copy()
    for i in range(m.get_height()):
        for j in range(m.get_width()):
            if m.get_at((j,i)) == (0,232,216):#연블루
                m.set_at((j,i),colorlist[0])
            if m.get_at((j,i)) == (0,112,236):#진블루
                m.set_at((j,i),colorlist[1])

                
    return m

def RM_ColorChange(surf,colorlist):
    temp = surf.copy()
    
    white,red = colorlist
    
    darkWhite = pygame.Color(white)
    darkWhite.hsva = (darkWhite.hsva[0],darkWhite.hsva[1],max(darkWhite.hsva[2] - 16,0))


    darkRed = pygame.Color(red)
    darkRed.hsva = (darkRed.hsva[0],darkRed.hsva[1],max(darkRed.hsva[2] - 16,0))

    darkWhite = darkWhite[0:3]
    darkRed = darkRed[0:3]

    for h in range(temp.get_height()):
        for w in range(temp.get_width()):
            if temp.get_at((w,h)) == (210,34,99):
                temp.set_at((w,h),red)

            elif temp.get_at((w,h)) == (255,255,255):
                temp.set_at((w,h),white)

##            elif temp.get_at((w,h)) == (0,0,0):
##                temp.set_at((w,h),mm.teduri)
                
            elif temp.get_at((w,h)) == (189,189,231):
                temp.set_at((w,h),darkWhite)

            elif temp.get_at((w,h)) == (155,30,76):
                temp.set_at((w,h),darkRed)
    return temp

ff = os.listdir("Sprites/Megaman")
def Stamp_MM(colorlist):
    MM = {}
    for i in ff:
        raw_img = Globals.trans_img_size(pygame.image.load("Sprites/Megaman/" + i),2)
        MM[i] = MM_ColorChange(raw_img,colorlist)
    return MM

# ff2 = os.listdir("../../Mega Man on pygame/cirno/TinyReimu/")
# def Stamp_RM(colorlist):
#     RM = {}
#     for i in ff2:
#         raw_img = Globals.trans_img_size(pygame.image.load("../../Mega Man on pygame/cirno/TinyReimu/" + i),1)
#         RM[i] = RM_ColorChange(raw_img,colorlist)
#     return RM


MEGAMANS = {}
for name in ColorTable:
    MEGAMANS[name] = Stamp_MM(ColorTable[name])
    

# REIMUS = {}
# for name in ColorTable:
#     REIMUS[name] = Stamp_RM(ColorTable[name])

#print(REIMUS)
class Mario:
    class Fireball:
        def __init__(self,mario,pos = (0,0),heading = None,MM = False):
            self.FireImages = [
                 pygame.transform.flip(Globals.trans_img_size(pygame.image.load("Sprites/Megaman/fire1.png"),2),mario.heading == 1,False),
                 pygame.transform.flip(Globals.trans_img_size(pygame.image.load("Sprites/Megaman/fire2.png"),2),mario.heading == 1,False),
                 pygame.transform.flip(Globals.trans_img_size(pygame.image.load("Sprites/Megaman/fire3.png"),2),mario.heading == 1,False)
                ]

            self.Fire = mario.MMFire
            if MM:
                if mario.MMFire:
                    self.image = self.FireImages[0]
                else:
                    self.image = Globals.trans_img_size(pygame.image.load("Sprites/Megaman/bullet.png"),1)
            else:
                self.image = Globals.trans_img_size(pygame.transform.scale(pygame.image.load("Sprites/Mario/fireball.png"), (12,14)),1)#.convert_alpha()

            self.rect = self.image.get_rect()
            self.blocked = False#For MM
            
            if pos != (0,0):
                self.rect.x, self.rect.y = pos
            else:
                self.rect.centerx,self.rect.centery = mario.rect.centerx + 20 * mario.heading,mario.rect.centery + 3
            if heading != None:
                self.speed = 12 * heading
            else:
                self.speed = 12 * mario.oldheading

            self.heading = mario.heading
            self.yv = 0
            self.Onslope = False
            self.Onslope2 = False
            self.collision_types= {'top':False,'bottom':False,'right':False,'left':False}
            mario.Fireballs.append(self)

        def collision_test(self,rect,tiles):
            return Globals.collision_test(rect,tiles)
        def move(self,rect,movement,tiles,slopes):
            collision_types = {'top':False,'bottom':False,'right':False,'left':False}
            for i in range(4):
                if self.Onslope:# or collision_types['bottom']:
                    rect.y += 0
            self.Onslope = False
            for ramp in slopes:
                hitbox = ramp.rect
                if rect.colliderect(hitbox):
                    rel_x = rect.x - hitbox.x

                    if ramp.heading == "NE":
                        pos_height = rel_x + rect.width 
                    elif ramp.heading == "NW":
                        pos_height = 32 - rel_x 
                    elif ramp.heading == "ENE1" or ramp.heading == "ENE2":
                        pos_height = 0.5 * (rel_x + rect.width) + 16
                    elif ramp.heading == "WNW1" or ramp.heading == "WNW2":
                        pos_height = 0.5 * (32 - rel_x) + 16
                    else:
                        pos_height = 69
                    # add constraints
                    pos_height = min(pos_height, 64)
                    pos_height = max(pos_height, 0)
                    target_y = hitbox.y + 64 - pos_height
                    
                    if rect.bottom >= target_y:
                        
                        rect.bottom = target_y

                        collision_types['bottom'] = True
                        self.Onslope = True
                        self.Onslope2 = True
                        
            if not self.Onslope and self.Onslope2:
                self.Onslope2 = False
                #rect.y -= 20
            rect.x+=movement[0]
            hit_list = self.collision_test(rect,tiles)
            for tile in hit_list:
                if movement[0] > 0:
                    rect.right = tile.left
                    collision_types['right'] = True
                elif movement[0] < 0:
                    rect.left = tile.right
                    collision_types['left'] = True
            rect.y += movement[1]
            hit_list = self.collision_test(rect,tiles)
            for tile in hit_list:
                if movement[1] > 0:
                    rect.bottom = tile.top
                    collision_types['bottom'] = True
                elif movement[1] < 0:
                    rect.top = tile.bottom
                    collision_types['top'] = True
            return rect, collision_types
            
        def Physics(self,Grounds,Slopes,mario):
            if mario.MegamanMode:
                if self.Fire:
                    self.image = self.FireImages[(Globals.GlobalTimer // 5) % 3]
                
                if self.blocked:
                    self.rect.x -= self.heading * 8
                    self.rect.y -= 8
                else:
                    self.rect.x += self.heading * 12
            else:
                self.yv += Globals.GRAVITY
                self.rect,self.collision_types = self.move(self.rect,[self.speed,self.yv],Grounds+[i.rect for i in Things.Pswitchs if not i.holded and not i.eaten],Slopes)#+[i.rect for i in Things.Pswitchs if not i.holded]
                if self.collision_types['bottom'] or self.Onslope:
                    self.yv = -10
                    self.Onslope = False
                if self.collision_types['top']:
                    self.yv = 0
                if self.collision_types['left'] or self.collision_types['right']:
                    Effects.Effect(self.rect.centerx,self.rect.centery,2,particles = False)
                    mario.Fireballs.remove(self)
                    return
        
            if self.rect.x - mario.scroll[0] < 0 or self.rect.x - mario.scroll[0] > 640:
                mario.Fireballs.remove(self)


            
    def ScreenShake(self,length,intensity):
        global ShakeVar,ScreenPos
        if ShakeVar == 0 and length != -1: #시작
            self.ScreenShaking = [True,length,intensity]
            pygame.mixer.Sound("Sounds/smash.wav").play()
        if ShakeVar < length:
            ShakeVar += 1
            ScreenPos = (random.randrange(-intensity,intensity),random.randrange(-intensity,intensity))
        else:
            ShakeVar = 0
            ScreenPos = (0,0)
            self.ScreenShaking = [False,-1,0]
        
    def __init__(self,x,y,player,main = False):
        self.Holded_Obj = None
        
        self.PrevUnderwater = False
        self.Underwater = False

        self.GamePause = False

        self.MMFire = not False

        self.standingplatform = None
        
        self.SpinCount = 0
        self.dive = False
        self.ScrollLimit = Globals.ScrollLimit
        self.jumpcombo = 0
        self.again = 0
        self.angle = 0
        self.RelativeHeight = False
        self.mission = False
        self.Pmeter = 0
        self.JumpTimer = 0
        self.Prun = False

        self.ScreenShaking = [False,-1,0]

        self.onplatform = False

        self.Nodisplay = False

        self.TargetText = None

        self.onspd = 0
        self.gotoffground = False

        self.main = main
        self.Ayv = 0

        self.WaitAfterDeath = 0
        
        self.oldheading = 0#self.heading이 0이 되기 바로 직전 heading

        self.AutoScroll = Globals.AutoScroll#이런건 Globals에 보내버리자
        

        self.CapeAttack = False

        self.rangeX = [0,0]
        self.rangeY = [0,0]

        self.AirSpinTimer = 0        
        
        self.GotInRealGoal = True

        self.fire = False
        self.FireTimer = 0
        self.Fireballs = []
        
        self.WallJumpable = False
        self.WallJump = False

        self.AbleToLimitSpd = False
        self.transforming = False

        self.climbing = False

        self.LayorTop = False
        self.Onslope2 = False

        self.WaitForB = False
        
        self.x = x
        self.y = y
        self.yv = 0
        self.realend = False
        self.jumping = False
        self.walktoend = False
        self.cannotmove = False
        self.blurness = 1

        self.onseesaw = False

        self.PowerChange = False

        self.starman = False
        self.StarTimer = 0
        if self.Underwater:
            self.yvLimit = 4
        else:
            self.yvLimit = 12
        self.ExtraScroll = 0

        self.RunJumping = False #달리면서 뛰면 아무것도 못하게 하기 위한 변수 
        
        self.cape = False
        
        self.TurnAround = False

        self.RidingYoshi = False
        self.Yoshi = None
        self.attack = False
        self.DisplayAddPos = [0,0]

        
        self.Onslope = False
        self.SlippingDown = False
        
        self.Pactivated = False
        self.Ptimer = 0
        self.Pwarning = False

        self.DeathTimer = 0
        self.CapeTimer = 0
        self.ClimbTimer = 0

        self.stuck = False
        self.jumpable = False

        self.swim = False
        
        self.Gameclear=False

        self.coin = 0

        self.PipeEnterType = "horizontal"#vertical

        self.RidingCloud = False
        
        self.slide = False
        self.InvincibleTimer = 0
        self.hitlistsH = []
        self.hitlistsV = []
        self.Turning = False
        self.running = False
        self.holding = False
        self.sitting = False
        self.LookingUp = False
        self.BlackScreen = False
        self.scroll = [x-320,y]
        self.state = "small"
        self.heading = 1
        self.speed = 0
        self.death = False

        self.beforeslope = False
        self.jumpingout = False
        self.TurnDirection = self.heading

        self.flying = False
        self.rising = False
        self.AbleToBoost = False
        self.ExtraBoost = False

        self.TheActualCloud = None#타고 있는 구름
        

        self.LookingBack = False #스핀 할 때 뒤 돌아보는 거

        self.pause = False
        
        self.combo = 1
        self.life = 30

        self.opacity = 255 # 255: 불투명 / 0: 투명

        self.CurrentSlopeAngle = 0
        
        self.calm = False

        self.DeathMotion = False
        
        self.player = 'm'
        self.playername = 'Mario'

        self.howchanging = None
        self.DeadInstantly = False

        self.ShellSpin = True
        self.AbleToEscapeFromWater = False

        self.FireColorChange = False#불 디스플레이 여부
        self.CapeDisplay = False#망토 디스플레이 여부
        
        self.image = pygame.image.load("Sprites/"+self.playername+"/"+self.state+"_"+self.player+"_"+"still.png").convert_alpha()

        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
        
        self.width = 28
        self.height = 40
        self.MoveTimer = 0
        self.SpinJump = False

        self.times = 1
        self.images = {}
        self.Mario1 = not True
        self.Mario3 = not True
        
        chara = ["Luigi","Mario","Toadette"]#,"Retro","Mario3"]
        if self.Mario1: chara.append("Retro")
        if self.Mario3: chara.append("Mario3")

        self.OriginalImages ={}
        self.FireImages = {}

        for i in chara:
            self.player = i[0].lower()
            if i == "Retro":
                self.player = "m"
            self.playername = i
            
            file_list = os.listdir("./Sprites/"+self.playername)
            
            for j in file_list:
                img = pygame.image.load("Sprites/"+self.playername+"/"+j).convert_alpha()
                if i in ["Toadette","Retro","Mario3"]:
                    img = pygame.transform.scale(img,(img.get_width() * 2, img.get_height() * 2))
            
                self.OriginalImages[j] = img
                self.FireImages[j] = firemario(img,self)
                    
        self.images = self.OriginalImages
        
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.mask = pygame.mask.from_surface(pygame.Surface(self.rect.size).convert_alpha())
        self.player = player[0].lower()#'m'
        self.playername = player#'Mario'
        self.movement = [0,0]
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.PowerChangeReserved = False#이게 True면 한 프레임 뒤에 PowerChanged가 활성화됨

        self.lastx = 0
        self.lasty = 0
        self.PowerChangeTimer = 0
        self.PlatformSpd = [0,0]
        
        #====Megaman Related=====#
        self.MegamanMode = False
        self.SlideTimer = 0
        self.Slide = False
        self.DamageTimer = 0
        self.ShootTimer = 0
        self.MMImageName = ""
        
        marios.append(self)

    def Holded_Object_Loop(self,obj,offsetX = 0):#throw, 마리오 canhold이런거 만들
        key = pygame.key.get_pressed()
        self.Holded_Obj = obj
        if self.SpinJump:
            if self.heading == 1:
                obj.rect.centerx = self.rect.right
            elif mario.heading == -1:
                obj.rect.centerx = self.rect.left
            else:
                obj.rect.centerx = self.rect.centerx
        else:
            if mario.heading == 0:
                obj.rect.centerx = self.rect.centerx #그냥 x로 하면 한 쪽으로 치우침
            else:
                obj.rect.centerx = self.rect.centerx + (24 + offsetX) * self.heading 
            
        if mario.sitting:
            obj.rect.bottom = self.rect.bottom
        else:
            obj.rect.bottom = self.rect.bottom - 7 * (self.state == "big")

        #Throwing behavior
        if not mario.running:
            if mario.LookingUp:
                obj.yv = -20
                obj.heading = 1
                try:obj.speed = abs(mario.speed) * mario.heading * 0.5
                except NameError: pass
            #기타 behavior script
            try:
                
                obj.ThrownBehavior(self,key[pygame.K_DOWN])
            except:pass
            
            mario.holding = False
            obj.holded = False

    def LevelCollide(self,surface,pos):#얘랑 아래 있는 애랑 합치자
        #ground, other tile(e.g. blocks), and slope는 각각 따로 계산!
        
        collide = False
        for i in slopes:
            if i.overlap(surface,(self.rect.x-i.rect.x,self.rect.y-i.rect.y)): #offset 설정(빼기)
                collide = True
                
        return collide

    def collision_test(self,rect,tiles):
        return self.Ground_collision_check(rect,tiles)

    def Ground_collision_check(self,rect,tiles = []):
        return Globals.collision_test(rect,tiles)
    
    #Object들은 위로 고정을 먼저 하는 것이 아니라 옆으로 고정을 먼저 한다(movement[1] 부터 검사)
##    def slope1(self,rect,slopes,movement):
##        return rect
##    
##        oldpos = rect.center
##        for i in range(16):
##            check = False
##            for s in slopes:
##                if not s.ceiling and s.mask.overlap(self.mask,(-s.rect.x + rect.x, -s.rect.y + rect.y)):#not ceiling이 없으면 lv3 에서 역가시 모양 땅에서 공중부양 할 수 있음. 나중에 문제 생기면 바꾸자                  
##                    check = True
##            
##            if not check:
##                break
##            
##            rect.y -= 1
##        
##        if i == 15:
##            rect.center = oldpos
##        return rect
    def slope2(self,rect,tiles,movement,collision_types):
        oldpos = rect.center
        if self.collision_types['bottom'] or self.beforeslope:
            for i in range(16):
                if movement[1] > 0:
                    check = self.SlopeCollision(rect)
##                    for ramp in slopes:
##                        if self.SlopeCollision(rect):
##                            check = True
                    if self.collision_test(rect,tiles) != []:
                        check = True
                        
                    if check:
                        break
                    
                    rect.y += 1
            if i == 15:
                rect.center = oldpos
            
        return rect
    def SlopeCollision(self,rect):
        NULL, SLOPES = Globals.test_collision_test(rect,[])# != Slopes
        for rampdata in SLOPES:
            ramptype,pos = rampdata
            ramp = Ground.SlopeData[ramptype]
            self.CurrentSlopeAngle = Ground.SlopeAngleData[ramptype]
            if ramp.overlap(self.mask,(-pos[0] + rect.x, -pos[1] + rect.y)):
                return True
        return False

    def SpecialXMove(self,rect,movement,tiles,collision_types):
        for i in range(math.ceil(abs(movement[0]))):#For ONLY slopes
            self.lastx = copy.deepcopy(rect.x)
            rect.x += abs(movement[0])/movement[0]
##            for i in range(3):
##                if self.SlopeCollision(rect):
##                    rect.y -= 1
##                else:
##                    break
            if self.SlopeCollision(rect):
                rect.y -= 1
                if self.SlopeCollision(rect):
                    rect.y -= 1
                    if self.SlopeCollision(rect):
                        rect.y -= 1
                        if self.SlopeCollision(rect):
                            rect.y += 3
                            rect.x = self.lastx
                            if movement[0] > 0:
                                collision_types['right'] = True
                            elif movement[0] < 0:
                                collision_types['left'] = True
                            break
                
        return rect,collision_types
    def SpecialYMove(self,rect,movement,collision_types):
        for i in range(math.ceil(abs(movement[1]))):#For ONLY slopes
            if self.SlopeCollision(rect):#ramp.mask.overlap(self.mask,(-ramp.rect.x + rect.x, -ramp.rect.y + rect.y)):
                rect.y += abs(movement[1])/movement[1] * -1
                #if not ramp.ceiling:
                self.Onslope = True
                
                if movement[1] > 0:
                    collision_types['bottom'] = True
                elif movement[1] < 0:
                    collision_types['top'] = True
            
                
        
        return rect,collision_types

    def Find_Closest_Space(self,rect,x,y,MAX,tiles):
        #print("WORKING")
        distance = 1#radius of the circle
        direction = 0
        n = 16#how many checks
        for i in range(MAX):
            for j in range(n):
                self.rect.x,self.rect.y = x,y

                tempX = distance * math.sin(math.radians(direction))
                tempY = distance * math.cos(math.radians(direction))

                self.rect.x += tempX
                self.rect.y -= tempY

                
                if not self.Ground_collision_check(rect,tiles):#SHOULD CONTAIN SLOPE!
                    return

                direction += 360 / n
                
            distance += 1
        self.rect.x,self.rect.y = x,y

    def move(self,rect,movement,tiles,slopes,colObjs):#,PureGround):
        global beftarget,target_y
        #rect.x %= len(Ground.game_map[0]) * 32
        prevtile = copy.deepcopy(tiles)
        for i in Enemy.KoopaTroopas:
            if i.winged and i.type == "BuzzyBeetle" and i.solid:# and movement[1] > 0:# and rect.bottom <= i.rect.top:#마리오와 충돌했을 때 모든 것을 처리
                tiles.append(i.rect)
                

        self.beforeslope = self.Onslope
        self.Onslope = False
        
        self.mask = pygame.mask.from_surface(pygame.Surface(self.rect.size).convert_alpha())

        returnlist = []
        last_collision_types = copy.deepcopy(self.collision_types)
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        prehit_list = self.collision_test(rect,tiles)


        #movement[0] += self.PlatformSpd[0]
        #movement[1] += self.PlatformSpd[1]
        for i in range(abs(math.ceil(self.PlatformSpd[0]))):
            self.lastx = rect.x
            rect.x += abs(self.PlatformSpd[0]) / self.PlatformSpd[0]
            if self.Ground_collision_check(rect,prevtile):
                rect.x = self.lastx
                break
##
        for i in range(abs(math.ceil(self.PlatformSpd[1]))):
            self.lasty = rect.y
            rect.y += abs(self.PlatformSpd[1]) / self.PlatformSpd[1]
            if self.Ground_collision_check(rect,prevtile):
                rect.y = self.lasty
                break
##        for i in Enemy.KoopaTroopas:
##            if i.winged and i.type == "BuzzyBeetle":# and movement[1] > 0:# and rect.bottom <= i.rect.top:#마리오와 충돌했을 때 모든 것을 처리
##                if i.rect.colliderect(rect):print("?")

##        rect.x += self.PlatformSpd[0]
##        rect.y += self.PlatformSpd[1]
        
        #any other way to implement moving platform without the script under?

##        if self.Ground_collision_check(rect,tiles) and not self.death:
##            self.Find_Closest_Space(rect,rect.x,rect.y,16,tiles)
##            if self.Ground_collision_check(rect,tiles):
##                self.Death()

        if self.onplatform:
            movement[0] += self.standingplatform.speedx

                
        #rect.x += movement[0]
##        if not self.death:
##            rect = self.slope1(rect,slopes,movement)
        
        if self.Onslope:
            collision_types['bottom'] = True

        if not self.death:
            rect,collision_types = self.SpecialXMove(rect,movement,None,collision_types)
       
        hmm = False
        
        for i in Block.Blocks:
            if i.type == "QBlock":
                if i.Invisible:
                    tiles.append(i.rect)
        
        hit_list = self.collision_test(rect,[])
        hit_obj_list = [i for i in colObjs if rect.colliderect(i.rect)]
        #print(prehit_list,hit_obj_list)
        if not self.death:
            for obj in hit_obj_list:
                NotActiveLH = False # whether it should not push horizontally
                
                if isinstance(obj,와리가리.swing) or isinstance(obj,Platform.Platform) or isinstance(obj,와리가리.rotatingplatform) or isinstance(obj,Block.Cloud):
                    NotActiveLH = True
                elif isinstance(obj,Block.QBlock):
                    if obj.Invisible:
                        hmm = True
                elif isinstance(obj,Things.Pswitch):
                    if obj.rect in prehit_list or obj.holded:
                        NotActiveLH = True

                elif isinstance(obj,Spring.Spring):
                    if obj.rect in prehit_list or obj.holded:
                        NotActiveLH = True
                                            

                if not hmm and not NotActiveLH:
                    tile = obj.rect
                    if movement[0] > 0:
                        if rect.right - tile.left <= 12 and self.rect.bottom != tile.top and not self.Onslope:
                            collision_types['left'] = True
                    elif movement[0] < 0:
                        if tile.right - rect.left <= 12 and self.rect.bottom != tile.top and not self.Onslope:
                            collision_types['right'] = True
                            
                    for i in range(math.ceil(abs(movement[0]))): #밀어내 버리기
                        if rect.colliderect(tile):
                            rect.x += abs(movement[0])/movement[0]*-1

            
            for tile in hit_list: # 여긴 이제 Ground rect밖에 없음
                if movement[0] > 0:
                    if rect.right - tile.left <= 12 and self.rect.bottom != tile.top and not self.Onslope:
                        collision_types['left'] = True
                elif movement[0] < 0:
                    if tile.right - rect.left <= 12 and self.rect.bottom != tile.top and not self.Onslope:
                        collision_types['right'] = True
                        
                for i in range(math.ceil(abs(movement[0]))): #밀어내 버리기
                    if rect.colliderect(tile):
                        rect.x += abs(movement[0])/movement[0]*-1
                
            
            #returnlist.append(hit_list) --> 이러면 쓸대없는 Ground의 rect까지 전달됨
            returnlist.append([obj.rect for obj in hit_obj_list])
            
            if self.Onslope:
                movement[1] = self.Ayv

        
        prehit_list = self.collision_test(rect,tiles)
        
        if self.onseesaw:
            for i in seesaw.seesaws:
                if i.marioison:
                    movement[1] -= i.yspd

        
        if self.onplatform:
            movement[1] += self.standingplatform.speedy
            movement[1] -= rect.bottom + movement[1] - self.standingplatform.rect.top

            ######ORIGINAL#######

##            movement[1] -= rect.bottom - self.standingplatform.rect.top + self.standingplatform.speedy
##            movement[1] += self.standingplatform.speedy + (0 if self.standingplatform.speedy > 0 else -1)# + (rect.bottom + self.standingplatform.speedy - self.standingplatform.rect.top)




        rect.y += math.ceil(movement[1]) #소수점으로 하면 생기는 문제: rect는 소수점 단위로 움직일 수 없다. 그리고  math.ceil(올림)이 없으면 마리오가 계속 떨어졌다 말았다가 한다. #마리오가 움직이는 것은 정수화 하기 위해 천장함수 사용.
        if not self.death:
            rect = self.slope2(rect,tiles,movement,collision_types)
    
##            for ramp in slopes:
##                if ramp.mask.overlap(self.mask,(-ramp.rect.x + rect.x, -ramp.rect.y + rect.y)):
##                    rect,collision_types = self.SpecialYMove(rect,movement,ramp,collision_types)
            rect,collision_types = self.SpecialYMove(rect,movement,collision_types)

        hit_list = self.collision_test(rect,tiles)
        for tile in hit_list:
            for i in Spring.Springs:
                if tile == i.rect and tile in prehit_list:
                    hit_list.remove(tile)
                    
            for m in Things.Pswitchs:
                if tile == m.rect and tile in prehit_list and not m.activated:#마리오가 스위치에 꼇는지 확인(꼈으면 아래에서 고정하는 스크립트가 안 돌아감)
                   hit_list.remove(tile)
        
        returnlist.append(hit_list) #returnlist에는 추가하는 이유: pswitch가 밟혔는지 확인하기 위함
        
    
        #그래서 pswitch가 발동되는 조건은 마리오가 끼지 않고 collision_types['bottom']이 true일 때임

    

        NonActive = False
        NonActive2 = False
        doit = False
        exception = False
        ExitThisWholeLoop = False
        
        
        
        if not self.death:
            soundplayed = False

            for tile in hit_list:
                for i in Block.Blocks:
                    if tile == i.rect:
                        if i.type == "QBlock" and i.Invisible:  
                            NonActive = True
                        elif i.type == "Cloud":
                            NonActive = True
                            
                            if tile.top + 16 > rect.bottom > tile.top:# and movement[1] > 0:
                                NonActive = False
                                
                                rect.bottom = tile.top
                            NonActive2 = True
                                                    
                        
                        
                if self.Onslope:#이 안에 구문은 언제적건데 작동은 하긴 하니?
                    if not NonActive :
                        if self.Ayv > 0:
                            collision_types['bottom'] = True
                                
                    if self.Ayv < 0:
                        for i in range(100):
                            if rect.colliderect(tile):
                                rect.x += 1#abs(self.Ayv) / self.Ayv
                                rect.y += 1
                            else:
                                self.speed = 0
                        collision_types['top'] = True
                else:
                    if not NonActive :
                        
                        okiedokie = False
                        if movement[1] > 0:
                            collision_types['bottom'] = True
                    if not NonActive2:
                        if movement[1] < 0:#투명블록을 때릴 수 있게
                            #pswitch는 조금 다른 방식으로 작동할 수 있게 pswitch한테 이 구문 실행불가 설정하셈
                            if not hmm or (hmm and rect.top > tile.bottom):
                                collision_types['top'] = True
                                rect.top = tile.bottom
                    for i in range(math.ceil(abs(movement[1]))): #밀어내 버리기
                        if rect.colliderect(tile) and not (NonActive or NonActive2):
                            if NonActive:
                                if movement[1] < 0:
                                        rect.y+=abs(movement[1])/movement[1]*-1
                            elif NonActive2:
                                if movement[1] > 0:
                                        rect.y+=abs(movement[1])/movement[1]*-1
                            else:
                                rect.y+=abs(movement[1])/movement[1]*-1
##                    if tile.colliderect(rect):
##                        X = [tile.right - rect.left, rect.right - tile.left]
##                        Y = [tile.bottom - rect.top, rect.bottom - tile.top]
##                        #print(X+Y)
##                        if min(X) > min(Y):#y축으로 밀어야 되는 상황
##                            for i in range(abs(min(Y))): #밀어내 버리기
##                                if min(Y) == Y[0]:
##                                    rect.y += 1
##                                else:
##                                    rect.y -= 1
##
##
##                        elif min(X) < min(Y):
##                            for i in range(abs(min(X))): #밀어내 버리기
##                                if min(X) == X[0]:
##                                    rect.x += 1
##                                else:
##                                    rect.x -= 1
##
##                        else:#둘 다 같은 경우
##                            for i in range(abs(min(Y))): #밀어내 버리기
##                                if min(Y) == Y[0]:
##                                    rect.y += 1
##                                else:
##                                    rect.y -= 1
##
##
##                            for i in range(abs(min(X))): #밀어내 버리기
##                                if min(X) == X[0]:
##                                    rect.x += 1
##                                else:
##                                    rect.x -= 1

        else:
            returnlist = [[],[]]
        
        for p in Things.Pswitchs:#pswitch가 머리에 박혔을 때
            if p.rect.colliderect(rect):
                oldpos = rect.center
                rect.y += p.yv
                if p.yv > 0 and p.rect.bottom < rect.centery:
                    #collision_types['top'] = True
                    p.yv = -8
                    p.speed = -3 * (-2 * (rect.centerx < p.rect.centerx) + 1)
                rect.center = oldpos 
            
##        f = 0
##        if not self.death and not self.onplatform:
##            for i in range(20):
##                if self.Onslope or collision_types['bottom']:
##                    #break
##                    rect.y += 1
##                    f += 1
##                
##                    
##                
##                
##            reservation = self.Onslope
##            self.Onslope = False
##            
##
##        
##                
##            jotcarnet = True
##            
##                    
##            #pygame.draw.rect(screen,(0,255,0),(self.rect.x - self.scroll[0],self.rect.y - self.scroll[1], self.width,self.height))
##            for ramp in slopes:
##                hitbox = ramp.rect
##                if rect.colliderect(hitbox): # check if player collided with the bounding box for the ramp
##                    # get player's position relative to the ramp on the x axis
##                    rel_x = rect.x - hitbox.x
##                    
##                    # get height at player's position based on type of ramp
##                
##                    if ramp.heading == "NE":
##                        pos_height = rel_x + rect.width
##                        Type = "Ground"
##                    elif ramp.heading == "NW":
##                        pos_height = 32 - rel_x
##                        Type = "Ground"
##                    elif ramp.heading == "ENE1" or ramp.heading == "ENE2":
##                        pos_height = 0.5 * (rel_x + rect.width) + 16
##                        Type = "Ground"
##                    elif ramp.heading == "WNW1" or ramp.heading == "WNW2":
##                        pos_height = 0.5 * (32 - rel_x) + 16
##                        Type = "Ground"
##
##                    if ramp.heading == "SE":
##                        pos_height = -rel_x
##                        Type = "Ceiling"
##                    elif ramp.heading == "SW":
##                        pos_height = rel_x
##                        Type = "Ceiling"
##                    
##                    # add constraints
##                    pos_height = min(pos_height, 32)
##                    pos_height = max(pos_height, 0)
##                    
##                    target_y = hitbox.y + 32 - pos_height
##                    nope = False
####                    if not reservation:
####                        if rect.bottom - movement[1] < target_y + 12 or movement[1] < 0:
####                           nope = True
##                    if rect.bottom > target_y and not nope and Type == "Ground":# or (not self.Onslope and not self.jumping): # check if the player collided with the actual ramp
##                        # adjust player height
##                        
##                        #rect.bottom = target_y
##                        for i in range(math.ceil(abs(rect.bottom-target_y))):
##                            if rect.bottom > target_y:
##                                rect.bottom += abs(rect.bottom-target_y) / (rect.bottom-target_y) * -1
##                        jotcarnet = False
##                        collision_types['bottom'] = True
##                        self.sloperect = hitbox
##                        self.Onslope = True
##                        self.Onslope2 = True
##                        self.CurrentSlopeAngle = ramp.angle
##                        self.Ayv = math.cos(math.radians(ramp.angle))
##                
##                    if self.SlippingDown:
##                        self.speed += -math.sin(math.radians(ramp.angle)) * 1
##
##                    if rect.top < target_y and Type == "Ceiling":
##                        for i in range(math.ceil(abs(target_y - rect.top))):
##                            if rect.top < target_y:
##                                rect.bottom -= abs(target_y - rect.top) / (target_y - rect.top) * -1
##                        collision_types['top'] = True
##                        
##                        
##                else:
##                    pass#if not reservation and hitbox == self.sloperect and not self.jumping:#slope -> flat ground 이동하자마자 한 번 반복
##                       
##                            
##                    #*** 차후 문제가 생길시 아래 onslope2를 활용한 알고리즘으로 ㄱㄱ ***#
##              
##            if not self.Onslope and self.Onslope2:#slope -> flat ground 이동하자마자 한 번 반복(사실 여기로 하는 것도 OK임)
##                self.Onslope2 = False
##                if not self.jumping:
##                    rect.y += 2
##                    for j in Grounds:
##                        if rect.colliderect(j):#근처 땅으로 강제 이동
##                            collision_types['bottom'] = True
##                            rect.bottom = j.top + 20#+20 이유는 이미 rect가 20(=f)만큼 이동해 있기 때문
##               
##            if jotcarnet:
##                rect.y -= f
        if self.Onslope:
            collision_types['bottom'] = True

        if not last_collision_types['bottom'] and collision_types["bottom"] and self.MegamanMode:
            pygame.mixer.Sound("Sounds/06 - MegamanLand.wav").play()
            soundplayed = True
##            self.ScreenShake(10,abs(int(movement[1])))
##            Effects.Effect(rect.centerx,rect.bottom,2)

        return rect, collision_types,returnlist[0],returnlist[1]

        
    def Run(self):
        key = pygame.key.get_pressed()
        if self.Turning:
            if Globals.GlobalTimer % 3 == 0:
                Effects.Effect(self.rect.centerx,self.rect.bottom,5)
        if not self.calm and not self.pause:
            if self.RidingCloud:
                if key[pygame.K_RIGHT]: self.speed += ACC
                elif key[pygame.K_LEFT]: self.speed -= ACC
                else:
                    if self.speed > 0: self.speed -= ACC / 3
                    else: self.speed += ACC / 3

                if key[pygame.K_z]: self.yv -= ACC
                elif key[pygame.K_DOWN]: self.yv += ACC
                else:
                    if self.yv > 0: self.yv -= ACC / 3
                    else: self.yv += ACC / 3

                self.speed = max(min(self.speed,WalkingSpd),-WalkingSpd * 1.5)
                self.yv = max(min(self.yv,WalkingSpd),-WalkingSpd * 1.5)

                if abs(self.speed) < ACC: self.speed = 0
                if abs(self.yv) < ACC: self.yv = 0
            elif self.MegamanMode:
                if self.ShootTimer > 0:
                    self.ShootTimer -= 1

                if self.DamageTimer > 0:
                    self.DamageTimer -=1

                if self.SlideTimer > 0:
                    self.SlideTimer -= 1
                if self.SlideTimer == 0 or not self.collision_types["bottom"]:
                    self.Slide = False
                    self.SlideTimer = 0


                if self.DamageTimer > 96:
                    self.speed = self.heading * -2
                else:
                    if key[pygame.K_RIGHT]:
                        if self.Slide:
                            if (key[pygame.K_RIGHT] and self.speed < 0) or (key[pygame.K_LEFT] and self.speed > 0):
                                self.Slide = False
                                self.SlideTimer = 0

                        else:
                            self.speed = MMWalkSpd
                            self.heading = 1
                    elif key[pygame.K_LEFT]:
                        if self.Slide:
                            if (key[pygame.K_RIGHT] and self.speed < 0) or (key[pygame.K_LEFT] and self.speed > 0):
                                self.Slide = False
                                self.SlideTimer = 0

                        else:
                            self.speed = -MMWalkSpd
                            self.heading = -1
                    else:
                        if not self.Slide:
                            self.speed = 0
                            
                    if self.Slide:
                        self.speed = 7 * self.heading
            
            else:
                self.running = key[pygame.K_s]
                    
                if self.Prun:
                    self.RunJumping = True
                    if self.collision_types['bottom']:
                        if not self.running or (abs(self.speed) != MaxPSpd + 1 * self.starman and self.mission):
                            if Globals.GlobalTimer % 24 == 0 and self.Pmeter > 0:
                                self.Pmeter -= 1
                    else:
                        pass
    ##                    if self.JumpTimer == 0:
    ##                        self.Pmeter = 0
                    
                else:
                    self.RunJumping = False
                    if self.running and abs(self.speed) >= MaxRunSpd and self.collision_types['bottom']:
                        if self.Pmeter < 6 and Globals.GlobalTimer % 8 == 0:#6
                            self.Pmeter += 1
                    else:
                        if Globals.GlobalTimer % 24 == 0 and self.Pmeter > 0:
                            self.Pmeter -= 1

                    
                
                        
                if self.Pmeter == 6:
                    self.Prun = True
                else:
                    self.Prun = False
                    self.mission = False
                k = 1 + 2 * Globals.SnowTheme#0.1같을 때 뭔가 이상함
                if not self.dive:
                    if self.Underwater:
                        if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
                            if self.speed == 0:
                                if key[pygame.K_LEFT]:
                                    self.speed = -1
                                elif key[pygame.K_RIGHT]:
                                    self.speed = 1
                        if not self.sitting:
                            if key[pygame.K_LEFT]:
                                self.speed -= 0.1 + (0.1 * self.holding)
                            elif key[pygame.K_RIGHT]:
                                self.speed += 0.1 + (0.1 * self.holding)
                                
                        if self.collision_types['bottom'] or self.Onslope:# and self.jumping: #아무것도 안 누르고 하늘에 있는데 느려지는게 말이 됨? / 등껍질을 밟거나 스핀할때 속도를 줄일 수 있어야함(아직 확실하지 않음)
                            if not (key[pygame.K_LEFT] or key[pygame.K_RIGHT]) or self.sitting: #아무 키도 안 누르거나 앉아 있고 땅에 있을 때
                                if self.speed > 0:
                                    self.speed -= 0.4
                                if self.speed < 0:
                                    self.speed += 0.4
                        
                    else: 
                        k /= 1 + 0.4 * self.Prun
                        if not self.flying and not self.SlippingDown: 
                            if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
                                if self.speed == 0:
                                    if key[pygame.K_LEFT]:
                                        self.speed = -0.5
                                    elif key[pygame.K_RIGHT]:
                                        self.speed = 0.5
                            if self.sitting:
                                self.Turning = False
                                if not self.collision_types['bottom']:#앉아 있고 공중에서만 가속 가능, Turning을 지정해 줄 필요가 없음(어차피 이미지 고정)
                                    if key[pygame.K_LEFT]:
                                        if self.speed > 0:
                                            self.speed -= ACC #0.25
                                        else:
                                            self.speed -= ACC
                                        
                                    elif key[pygame.K_RIGHT]:
                                        if self.speed < 0:
                                            self.speed += ACC#0.25
                                        else:
                                            self.speed += ACC
                            else:
                                if key[pygame.K_LEFT]:
                                    if self.collision_types['bottom'] and self.speed > 0: #급격한 속도변화는 땅에서만 가능
                                        self.speed -= 0.4 / k
                                        self.Turning = True
                                    else:#not on ground or speed < 0
                                        if self.collision_types['bottom']: self.speed -= ACC / k
                                        else: self.speed -= ACC
                                        
                                        self.Turning = False
                                    
                                elif key[pygame.K_RIGHT]:
                                    if self.collision_types['bottom'] and self.speed < 0:
                                        self.speed += 0.4 / k
                                        self.Turning = True
                                    else:
                                        if self.collision_types['bottom']: self.speed += ACC / k
                                        else: self.speed += ACC
                                        
                                        self.Turning = False
                                else:
                                    self.Turning = False

                if self.collision_types['bottom']:# and self.jumping: #아무것도 안 누르고 하늘에 있는데 느려지는게 말이 됨? / 등껍질을 밟거나 스핀할때 속도를 줄일 수 있어야함(아직 확실하지 않음)
                    if (not (key[pygame.K_LEFT] or key[pygame.K_RIGHT])) or self.sitting or (self.SlippingDown and not (self.Onslope or self.onseesaw)) or self.dive: #아무 키도 안 누르거나 앉아 있고 땅에 있을 때
                        if self.speed > 0:
                            self.speed -= 0.3 / k
                        if self.speed < 0:
                            self.speed += 0.3 / k

                                
                if not self.running and not self.SlippingDown and not self.dive: #속도는 빠른데 self.running이 아닌 경우 강제 감속 / 걷고 있는데 속도를 5로 유지하는 것도 여기서
                    if abs(self.speed) > WalkingSpd + 1:
                        if self.speed > 0:
                            self.speed -= 0.3
                        if self.speed < 0:
                            self.speed += 0.3
                    else:
                        if self.speed > WalkingSpd:
                            self.speed = WalkingSpd
                        if self.speed < -WalkingSpd:
                            self.speed = -WalkingSpd

                
            if self.Onslope and self.SlippingDown:
                self.speed += -math.sin(math.radians(self.CurrentSlopeAngle))
                if not self.AbleToLimitSpd and abs(self.speed) > 1:
                    self.AbleToLimitSpd = True
            if not self.MegamanMode and not self.RidingCloud:
                if abs(self.speed) < 0.5:
                    if self.SlippingDown:
                        if self.AbleToLimitSpd:# and not self.SlippingDown:
                            self.speed = 0
                    else:
                        self.speed = 0

            if self.Underwater:
                if self.collision_types['bottom']:
                    if self.speed > 2 :
                        self.speed = 2 
                    if self.speed < -2:
                        self.speed = -2
                else:
                    if self.speed > 3 + (2 * self.holding):
                        self.speed = 3 + (2 * self.holding)
                    if self.speed < -3 - (2 * self.holding):
                        self.speed = -3 - (2 * self.holding)
                
            elif not self.MegamanMode:
                if self.running or self.SlippingDown:
                    if self.Prun:    
                        if self.speed > MaxPSpd + 1 * self.starman:
                            self.speed = MaxPSpd + 1 * self.starman
                            self.mission = True
                        if self.speed < -MaxPSpd - 1 * self.starman:
                            self.speed = -MaxPSpd - 1 * self.starman
                            self.mission = True
                    else: 
                        if self.speed > MaxRunSpd + 1 * self.starman:
                            self.speed = MaxRunSpd + 1 * self.starman
                        if self.speed < -MaxRunSpd - 1 * self.starman:
                            self.speed = -MaxRunSpd - 1 * self.starman
                elif self.dive:
                    if self.speed > MaxRunSpd + 1 * self.starman:
                        self.speed = MaxRunSpd + 1 * self.starman
                    if self.speed < -MaxRunSpd - 1 * self.starman:
                        self.speed = -MaxRunSpd - 1 * self.starman
    def MegamanMotion(self):
        global MMWalkSpd

        if self.MMFire:
            MEGAMAN = MEGAMANS["Fire"]
            REIMU = REIMUS["Fire"]
        else:
            MEGAMAN = MEGAMANS["Normal"]
            REIMU = REIMUS["Normal"]
        MMWalkSpd = 4

        if self.PowerChange:
            self.pause = True
            self.PowerChangeTimer += 1
            if self.PowerChangeTimer % 6 == 0:
                self.MMFire = False
            elif self.PowerChangeTimer % 6 == 3:
                self.MMFire = True
                
            if self.PowerChangeTimer >= 48:
                self.PowerChangeTimer = 0
                self.pause = False
                self.PowerChange = False
                self.MMFire = True
           
        elif self.SpinJump:
            if self.MoveTimer % 8 == 0:
                self.MMImageName = "Spin1.png"
            if self.MoveTimer % 8 == 2:
                self.MMImageName = "Spin2.png"
            if self.MoveTimer % 8 == 4:
                self.MMImageName = "Spin3.png"
            if self.MoveTimer % 8 == 6:
                self.MMImageName = "Spin4.png"
            self.MoveTimer += 1
            
        elif self.collision_types["bottom"]:
            if self.speed == 0:
                self.MoveTimer = 0
                if self.ShootTimer == 0:
                    if (Globals.GlobalTimer // 8) % 16 == 0:
                        self.MMImageName = "Still2.png"
                    else:
                        self.MMImageName = "Still.png"
                else:
                    self.MMImageName = "Shoot.png"
                    
            else:
                if self.Slide:
                    self.MMImageName = "Slide.png"
                else:
                    if self.MoveTimer < 4:
                        self.MMImageName = "Walk1.png"
                        MMWalkSpd = 1
                    else:
                        if self.ShootTimer == 0:
                            if self.MoveTimer % 24 == 0:
                                self.MMImageName = "Walk1.png"
                            if self.MoveTimer % 24 == 6:
                                self.MMImageName = "Walk2.png"
                            if self.MoveTimer % 24 == 12:
                                self.MMImageName = "Walk3.png"
                            if self.MoveTimer % 24 == 18:
                                self.MMImageName = "Walk2.png"
                        else:
                            if self.MoveTimer % 24 == 0:
                                self.MMImageName = "Walk_shoot1.png"
                            if self.MoveTimer % 24 == 6:
                                self.MMImageName = "Walk_shoot2.png"
                            if self.MoveTimer % 24 == 12:
                                self.MMImageName = "Walk_shoot3.png"
                            if self.MoveTimer % 24 == 18:
                                self.MMImageName = "Walk_shoot2.png"


                if not self.PowerChange: self.MoveTimer += 1
        else:
            if self.ShootTimer == 0:
                self.MMImageName = "Jump.png"
            else:
                self.MMImageName = "Jump_shoot.png"

        if self.DamageTimer > 96:
            self.MMImageName = "Damage.png"


        #self.image = MEGAMAN[self.MMImageName]
        #print("tinyReimu_" + self.MMImageName.lower())
        self.image = REIMU["TinyReimu_" + self.MMImageName.lower()]
    def MoveMotion(self):
        if self.fire and self.FireColorChange:            
            self.images = self.FireImages
        else:
            self.images = self.OriginalImages


        if self.Gameclear:
            self.Turning=False
        global idx,Temp,Refill,Target,again

        self.MoveTimer += 1

        if not self.PowerChange and not self.climbing:
            if not self.cannotmove and not self.attack and not self.flying:
                if not self.SpinJump and not self.TurnAround and self.AirSpinTimer > 12 and not self.climbing and not self.dive:#SELF.SITTING
                    if key[pygame.K_LEFT]:
                        self.heading = -1
                        
                    elif key[pygame.K_RIGHT]: #동시에 눌리면 난리나므로 elif 사용
                        self.heading = 1

                    if self.ShellSpin:
                        self.heading = 0
                            
                
            if self.RidingYoshi:
                oldpos = self.rect.bottom
                if (self.collision_types['bottom'] or self.Onslope) and not self.calm:
                    if not self.Yoshi.turning and not self.attack: 
                        if key[pygame.K_DOWN]:
                            self.sitting = True
                            self.rect.height = 32
                        else:
                            self.rect.height = 55
                            self.sitting = False
                
                    
                else:     
                    if self.Underwater:
                        self.sitting = False
                        
                self.rect.bottom = oldpos
                

                self.SpinJump=True

                if Temp:
                    idx+=1
                    if idx < 12:
                        self.Yoshi.turning = True
                        self.ImageName = self.state+"_"+self.player+"_"+"yoshi_turn.png"
                        self.RelativeHeight = True
                        if idx <= 6:
                            self.heading = Target * -1
                        else:
                            self.heading = Target
                        
                    else:
                        idx = 0
                        Temp = False
                        self.Yoshi.turning = False
                    self.DisplayAddPos[0] -= self.heading * 2#이 두 코드가 정확히 여기 위치해야 돌 때 이상하지 않음 
                    self.DisplayAddPos[1] -= 23

                elif self.attack:
                    if self.collision_types['bottom']:
                        self.DisplayAddPos = [0,-15 + self.sitting * 5]
                    else:
                        self.DisplayAddPos = [0,-20]
                    if self.MoveTimer == 0:
                        self.ImageName = self.state+"_"+self.player+"_"+"yoshi_attack1.png"
                    elif self.MoveTimer == 8:
                        self.ImageName = self.state+"_"+self.player+"_"+"yoshi_attack2.png"
                    elif self.MoveTimer > 20:
                        self.ImageName = self.state+"_"+self.player+"_"+"yoshi_idle.png"
     
                elif self.sitting:
                    self.ImageName = self.state+"_"+self.player+"_"+"hold_crouch.png"
                    self.RelativeHeight = True
                    self.DisplayAddPos = [0,-10]

                else:
                    self.ImageName = self.state+"_"+self.player+"_"+"yoshi_idle.png"
                    self.DisplayAddPos[0] -= self.heading * 2
                    if self.calm:
                        self.DisplayAddPos[1] -= 20#정확하지 않음
                    else:
                        self.DisplayAddPos[1] -= 20


                    if self.state == "small":
                        self.height = 40
                    else:
                        self.height = 55
                    
        
                if self.calm:
                    if self.PipeEnterType == "horizontal":
                        self.ImageName = self.state+"_"+self.player+"_"+"yoshi_idle.png"
                        self.DisplayAddPos[1] = -5
                    else:
                        self.ImageName = self.state+"_"+self.player+"_"+"yoshi_turn.png"
                        self.DisplayAddPos[1] = -23

            else:
                if self.holding and not self.SpinJump:
                    if Temp and not self.calm: 
                        if not self.sitting and self.AirSpinTimer > 12:#앉아 있을 때는 돌 수 없음
                            idx+=1
                            if idx < 8:
                                self.heading = 0
                                self.LookingBack = False
                                self.ShellSpin = True

                            else:
                                self.ShellSpin = False
                                Temp = False
                                self.heading = Target
                            
                    else:
                        self.ShellSpin = False
                        idx=0
                        

                        if self.collision_types['bottom']:
                            if abs(self.speed) > 0:
                                if self.state == "small":
                                    if self.MoveTimer % 6 == 0:
                                        self.ImageName = self.state+"_"+self.player+"_"+"hold1.png"
                                    elif self.MoveTimer % 6 == 3:
                                        self.ImageName = self.state+"_"+self.player+"_"+"hold2.png"
                                else:
                                    if self.MoveTimer % 6 == 0:
                                        self.ImageName = self.state+"_"+self.player+"_"+"hold1.png"
                                    elif self.MoveTimer % 6 == 2:
                                        self.ImageName = self.state+"_"+self.player+"_"+"hold2.png"
                                    elif self.MoveTimer % 6 == 4:
                                        self.ImageName = self.state+"_"+self.player+"_"+"hold3.png"
                            else:
                                self.ImageName = self.state+"_"+self.player+"_"+"hold1.png"

                                
                            
                                
                        else:
                            
                            if self.Underwater:
                                if self.MoveTimer % 12 == 0:
                                    self.ImageName = self.state+"_"+self.player+"_"+"hold_swim1.png"
                                    
                                elif self.MoveTimer % 12 == 4:
                                    self.ImageName = self.state+"_"+self.player+"_"+"hold_swim2.png"
                                elif self.MoveTimer % 12 == 8:
                                    self.ImageName = self.state+"_"+self.player+"_"+"hold_swim3.png"
##                                else:
##                                    self.image=self.images[self.state+"_"+self.player+"_"+"swim1.png"]
                            else:
                                if not self.sitting:
                                    if self.state == "small":
                                        self.ImageName = self.state+"_"+self.player+"_"+"hold2.png"
                                    else:
                                        self.ImageName = self.state+"_"+self.player+"_"+"hold3.png"
                            
                else:
                    self.ShellSpin = False
                    if self.RidingCloud:
                        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                    elif self.collision_types['bottom']:
                        if not self.TurnAround and not self.flying:
                            if abs(self.speed)>0:
                                if self.Turning and not Globals.SnowTheme:
                                    self.ImageName = self.state+"_"+self.player+"_"+"quickturn.png"

                                else:
                                    if abs(self.speed) == MaxPSpd + 1 * self.starman and not self.Mario1:
                                        if self.MoveTimer % 4 == 0:
                                            self.ImageName = self.state+"_"+self.player+"_"+"run1.png"
                                        elif self.MoveTimer % 4 == 2:
                                            self.ImageName = self.state+"_"+self.player+"_"+"run2.png"
                                    elif self.speed != 0:     
                                        if self.state == "small":
                                            speedmeter = 0
                                            if 0 <= abs(self.speed) < 6:
                                                speedmeter = 8
                                            elif 6 <= abs(self.speed) < 9:
                                                speedmeter = 6
                                            elif 9 <= abs(self.speed) < 12:
                                                speedmeter = 4
                                            else:  # 12 <= abs(self.speed) < 15:
                                                speedmeter = 2
                                            if Globals.SnowTheme:
                                                speedmeter = 4#최소 3 아니면 이상해짐

                                            if self.MoveTimer % speedmeter == 0:
                                                self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                                            elif self.MoveTimer % speedmeter == int(speedmeter / 2):
                                                self.ImageName = self.state+"_"+self.player+"_"+"walk.png"
                                            
                                        else:
                                            speedmeter = 0
                                            if 0 <= abs(self.speed) < 6:
                                                speedmeter = 12
                                            elif 6 <= abs(self.speed) < 9:
                                                speedmeter = 9
                                            elif 9 <= abs(self.speed) < 12:
                                                speedmeter = 6
                                            else:# 8 <= abs(self.speed) < 15:
                                                speedmeter = 3
                                            if Globals.SnowTheme:
                                                speedmeter = 6#최소 3 아니면 이상해짐
                                                
                                            if self.MoveTimer % speedmeter  == 0:
                                                self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                                            elif self.MoveTimer % speedmeter  == int(speedmeter / 3):
                                                self.ImageName = self.state+"_"+self.player+"_"+"walk.png"
                                            elif self.MoveTimer % speedmeter  == int(speedmeter / 3 * 2):
                                                self.ImageName = self.state+"_"+self.player+"_"+"walk2.png"

                                            if self.Mario3:#마리오 3
                                                scale = 4
                                                speedmeter = scale * 4
                                                if self.MoveTimer % speedmeter == 0:
                                                    self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                                                elif self.MoveTimer % speedmeter  == scale:
                                                    self.ImageName = self.state+"_"+self.player+"_"+"walk.png"
                                                elif self.MoveTimer % speedmeter  == scale * 2:
                                                    self.ImageName = self.state+"_"+self.player+"_"+"walk2.png"
                                                elif self.MoveTimer % speedmeter  == scale * 3:
                                                    self.ImageName = self.state+"_"+self.player+"_"+"walk.png"


                                        if self.Mario1:#마리오 1
                                            speedmeter = 12
                                            if self.MoveTimer % speedmeter == 0:
                                                self.ImageName = self.state+"_"+self.player+"_"+"walk.png"
                                            elif self.MoveTimer % speedmeter  == int(speedmeter / 3):
                                                self.ImageName = self.state+"_"+self.player+"_"+"walk2.png"
                                            elif self.MoveTimer % speedmeter  == int(speedmeter / 3 * 2):
                                                self.ImageName = self.state+"_"+self.player+"_"+"walk3.png"


                                        
                                    else:
                                        if not self.sitting :
                                            self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                                            

                            else:
                                self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                                
                            
                            
                                
                                    
                        
                        
                    else:
                        if not self.SpinJump:
                            if self.RunJumping:
                                pass
##                                if self.cape and self.yv>0 and self.rising:
##                                    self.rising = False
##                                    self.flying = True
                            else:
                                if self.Underwater:
                                    if self.swim:
                                        if self.MoveTimer % 18 == 0:
                                            self.ImageName = self.state+"_"+self.player+"_"+"swim1.png"
                                            if self.MoveTimer > 0:
                                                self.swim = False
                                                self.MoveTimer = -1
                                        elif self.MoveTimer % 18 == 6:
                                            self.ImageName = self.state+"_"+self.player+"_"+"swim2.png"
                                        elif self.MoveTimer % 18 == 12:
                                            self.ImageName = self.state+"_"+self.player+"_"+"swim3.png"
                                    else:
                                        self.ImageName = self.state+"_"+self.player+"_"+"swim1.png"

                                        
                                else:
                                    if not self.TurnAround:
                                        if self.yv < 0:
                                            self.ImageName = self.state+"_"+self.player+"_"+"jump.png"
                                        elif self.yv > 0:
                                            if not self.Mario1:
                                                 self.ImageName = self.state+"_"+self.player+"_"+"fall.png"
                                       
                
                

                if not self.TurnAround and not self.SpinJump and not self.sitting and not self.holding:
                    if self.RunJumping and not self.flying:#공중에서 모양 변환이 안되게, 망토도 마찬가지       
                        if (self.cape and self.yv < 0) or not self.collision_types['bottom'] and not self.Mario1:
                            self.ImageName = self.state+"_"+self.player+"_"+"run_jump.png"
                            
                               
                            

                if key[pygame.K_z] and not self.cannotmove and not self.Mario1 and not self.Mario3:
                    if not self.sitting and not self.jumping and self.collision_types['bottom']:
                        if self.speed == 0: #speed가 0일때만 모습을 바꾼다(위를 바라보는건 언제든지)
                            if self.holding:
                                self.ImageName = self.state+"_"+self.player+"_"+"up_hold.png"
                            else:
                                self.ImageName = self.state+"_"+self.player+"_"+"up.png"
                    self.LookingUp=True
                else:
                    self.LookingUp=False

                if self.collision_types['bottom']:
                    #self.RunJumping = False
                    if self.SlippingDown:
                        self.sitting = False
                    else:
                        if not self.calm:
                            if key[pygame.K_DOWN]:
                                if not ((self.Mario1 or self.Mario3) and (self.state == "small" or self.holding)):
                                    self.sitting = True
                                
                            else:
                                self.sitting = False
                        
                else:
                    if self.Underwater:
                        self.sitting = False


                if not self.cannotmove and self.sitting:
                    if self.holding:
                        self.ImageName = self.state+"_"+self.player+"_"+"hold_crouch.png"
                    else:
                        self.ImageName = self.state+"_"+self.player+"_"+"crouch.png"
                        
        if self.cape and self.yv > 0 and self.rising:
            self.rising = False
            if not self.holding and not self.RidingYoshi and not self.SpinJump:
                self.flying = True
            
            
        oldInfo = (self.rect.bottom,self.rect.height)
        if not self.RidingYoshi and not self.flying:      
            if self.sitting:
                self.RelativeHeight = True
                if self.state == "small":
                    self.rect.height=int(28 * self.times)#st6,bt12,sm4,bm12 -> + 5 * self.holding
                    self.height=int((28 + 5 * self.holding)* self.times)
                else:
                    self.rect.height=int(30 * self.times)
                    self.height=int((30 + 5 * self.holding)* self.times)
            else:
                if self.state == "small":
                    self.rect.height=int(32 * self.times)
                    self.height=int(40 * self.times)
                    #self.width = int(28 * self.times)
                    #self.rect.width = int(28 * self.times)

            
                else:
                    #self.width = int(28* self.times)
                    #self.rect.width = int(28* self.times)
                    self.rect.height=int(55* self.times)
                    self.height=int(55* self.times)

             
        if self.rect.height != oldInfo[1]:
            self.rect.bottom = oldInfo[0]
        
        if not self.PowerChange:
                if self.flying:
                    #self.rect.height=int(34* self.times)
                    self.width=int(34* self.times)
                    
                else:pass
##                    self.rect.width=28
##                    self.width=28

                
                
                if self.CapeAttack:
                    k = 4
                elif self.AirSpinTimer > 12:
                    k = 4
                else:
                    k = 12
                
                    
                if self.TurnAround:
                
                    if self.again < 2:
                        if self.MoveTimer % k == 0: #0 <= self.MoveTimer %k <= int(k/4*1) - 1:
                            self.ImageName = self.state+"_"+self.player+"_"+"spin1.png"
                            self.heading = 0
                            self.LookingBack = False
                            
                        elif self.MoveTimer % k == int(k/4*1): #int(k/4*1) <= self.MoveTimer %k <= int(k/4*2) - 1:
                            self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                            self.heading = -self.TurnDirection
                            if self.fire and self.SpinCount % 4 == 0:
                                self.FireFireball()
                            
                        elif self.MoveTimer % k == int(k/4*2): #int(k/4*2) <= self.MoveTimer %k <= int(k/4*3) - 1:
                            
                            self.ImageName = self.state+"_"+self.player+"_"+"spin2.png"
                            self.heading = 0
                            self.LookingBack = True
                        elif self.MoveTimer % k == int(k/4*3): #int(k/4*3) <= self.MoveTimer %k <= int(k/4*4) - 1:
                            
                            self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                            self.heading = self.TurnDirection
                            if self.fire and self.SpinCount % 4 == 2:
                                self.FireFireball()

                            if self.SpinJump:
                                self.SpinCount += 1
                            else:
                                self.again +=1
                            
                    else:
                        self.TurnAround = False
                        self.again = 0
                        self.SpinCount = 0
                        if self.CapeAttack:
                            self.CapeAttack = False
                
                    
        if not self.PowerChange:

            if self.flying:
                if self.yv > 0:
                    self.CapeTimer += 1
                if ((self.heading == 1 and key[pygame.K_RIGHT]) or (self.heading == -1 and key[pygame.K_LEFT])):
                    if self.CapeTimer >= 23:
                        self.CapeTimer = 23
                else:
                    if self.CapeTimer >= 12:
                        self.CapeTimer = 12
            else:
                self.CapeTimer = 0
                self.AbleToBoost = False
                self.ExtraBoost = False

            
            if self.flying:# and not self.AbleToBoost:  
                self.yvLimit = 12
                if self.CapeTimer == 0 or self.CapeTimer == 1:
                    self.ImageName = self.player+"_"+"cape1.png"
                    
                elif self.CapeTimer == 6:
                    
                    self.ImageName = self.player+"_"+"cape2.png"
                    
                elif self.CapeTimer == 12:
                    self.ImageName = self.player+"_"+"cape3.png"
                    self.AbleToBoost = True
                    self.ExtraBoost = False
                    
                elif self.CapeTimer == 17:
                    self.ImageName = self.player+"_"+"cape4.png"
                    
                elif self.CapeTimer == 20:
                    self.ImageName = self.player+"_"+"cape5.png"
                     
                elif self.CapeTimer == 23:
                    self.ImageName = self.player+"_"+"cape6.png"
                    self.ExtraBoost = True
            if self.CapeTimer > 12:
                self.speed += 0.5 * self.heading

                

            if self.flying and self.collision_types['bottom']:
                if self.speed == 0:
                    self.flying = False
                    self.AbleToBoost = False
                    self.ExtraBoost = False

                if self.ExtraBoost:
                    self.ScreenShake(30,10)
                    self.flying = False


            FallOff = True
            for i in Vine.Vines:
                if self.rect.colliderect(i.rect):
                    if key[pygame.K_z]:
                        if not self.RidingYoshi and not self.holding and not self.climbing:
                            self.climbing = True
                            self.SpinJump = False
                            self.heading = 0
                            
                            self.LookingBack = True
                    if self.climbing:
                        FallOff = False
                                
            if self.climbing and FallOff:
                self.climbing = False
                self.heading = self.oldheading


            if self.climbing: #보완좀...
                self.heading = 0
                if key[pygame.K_LEFT]:
                    self.speed = -2
                elif key[pygame.K_RIGHT]:
                    self.speed = 2
                else:
                    self.speed = 0
                    
                if key[pygame.K_z]:
                    self.yv = -3#movement[1] -= 3
                elif key[pygame.K_DOWN]:
                    self.yv = 3#movement[1] += 3
                    self.sitting = False
                else:
                    self.yv = 0
                if key[pygame.K_z] or key[pygame.K_DOWN]:
                    self.ClimbTimer += 1

                    
                if self.ClimbTimer % 10 == 0:
                    self.ImageName = self.state+"_"+self.player+"_"+"climb1.png"
                if self.ClimbTimer % 10 == 5:
                    self.ImageName = self.state+"_"+self.player+"_"+"climb2.png"

        if self.PowerChangeReserved:
            self.PowerChange = True
            self.PowerChangeReserved = False
            
        if self.PowerChange:
            self.RelativeHeight = True
            if self.howchanging == "Down":
                if self.MoveTimer == 0:
                    
                    self.pause = True
                    self.LayorTop = True

                if self.fire:
                    if ((self.MoveTimer % 32) // 4) % 2 == 0:#0,4,8,12... -> 0,1,2,3 -> 0,1,0,1
                        self.FireColorChange = True
                    else:
                        self.FireColorChange = False

                    if self.MoveTimer == 32:
                        self.transforming = False
                        self.FireColorChange = True
                        self.pause = False
                        self.fire = False
                        self.PowerChange = False
                        self.LayorTop = False
                        self.Nodisplay = False
                elif self.cape:
                    if ((self.MoveTimer % 32) // 4) % 2 == 0:#0,4,8,12... -> 0,1,2,3 -> 0,1,0,1
                        self.CapeDisplay = True#이걸 self가 아니라 cape에 넣어도 될듯?
                    else:
                        self.CapeDisplay = False

                    if self.MoveTimer == 32:
                        self.transforming = False
                        self.FireColorChange = True
                        self.pause = False
                        self.cape = False
                        self.CapeDisplay = False#나중에 다시 망토를 얻었을 경우를 위해
                        self.PowerChange = False
                        self.LayorTop = False
                        self.Nodisplay = False
                        if self.Underwater:
                            self.yvLimit = 4
                        else:
                            self.yvLimit = 12

                else:
                    if self.MoveTimer % 32 == 0:
                        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                        self.pause = True
                        self.LayorTop = True
                        self.transforming = False
                    elif self.MoveTimer % 32 == 4:
                        self.ImageName = self.player+"_"+"powerdown.png"
                        self.transforming = True
                    elif self.MoveTimer % 32 == 8:
                        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                        self.transforming = False
                    elif self.MoveTimer % 32 == 12:
                        self.ImageName = self.player+"_"+"powerdown.png"
                        self.transforming = True
                    elif self.MoveTimer % 32 == 16:
                        self.state = "small"
                        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                        self.transforming = False
                    elif self.MoveTimer % 32 == 20:
                        self.ImageName = self.player+"_"+"powerdown.png"
                        self.transforming = True
                    elif self.MoveTimer % 32 == 24:
                        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                        self.transforming = False
                    elif self.MoveTimer % 32 == 28:
                        self.ImageName = self.player+"_"+"powerdown.png"
                        self.transforming = False
                        self.pause = False
                        self.PowerChange = False
                        self.LayorTop = False


            elif self.howchanging == "Grow":
                if self.MoveTimer == 0 and self.cape:
                    Effects.Effect(self.rect.centerx,self.rect.centery,2,particles = False,TI = 8)
                    self.Nodisplay = True
                    self.CapeDisplay = True

                if self.MoveTimer == 0:
                    self.pause = True
                    self.LayorTop = True

                if self.fire:
                    if ((self.MoveTimer % 32) // 4) % 2 == 0:#0,4,8,12... -> 0,1,2,3 -> 0,1,0,1
                        self.FireColorChange = True
                    else:
                        self.FireColorChange = False

                    if self.MoveTimer == 32:
                        self.transforming = False
                        self.FireColorChange = True
                        self.pause = False
                        self.fire = True
                        self.PowerChange = False
                        self.LayorTop = False
                        self.Nodisplay = False
                else:
                    if self.MoveTimer % 32 == 0:
                        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                        self.pause = True
                        self.LayorTop = True
                        self.transforming = False
                    elif self.MoveTimer % 32 == 4:
                        self.ImageName = self.player+"_"+"powerdown.png"
                        self.transforming = True
                    elif self.MoveTimer % 32 == 8:
                        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                        self.transforming = False
                    elif self.MoveTimer % 32 == 12:
                        self.ImageName = self.player+"_"+"powerdown.png"
                        self.transforming = True
                    elif self.MoveTimer % 32 == 16:
                        self.state = "big"
                        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                        self.transforming = False
                    elif self.MoveTimer % 32 == 20:
                        self.ImageName = self.player+"_"+"powerdown.png"
                        self.transforming = True
                    elif self.MoveTimer % 32 == 24:
                        self.ImageName = self.state+"_"+self.player+"_"+"still.png"
                        self.transforming = False
                    elif self.MoveTimer % 32 == 28:
                        self.ImageName = self.player+"_"+"powerdown.png"
                        self.transforming = False
                        self.pause = False
                        self.PowerChange = False
                        self.LayorTop = False
                        self.Nodisplay = False
            self.times = 1
        
        if self.SlippingDown:
            self.ImageName = self.state+"_"+self.player+"_"+"slide.png"

        if self.fire:
            if self.FireTimer > 0:
                self.FireTimer -= 1
                if not self.SpinJump:
                    if self.collision_types['bottom']: self.ImageName = self.player+"_"+"fire.png"
                    else: self.ImageName = self.state+"_" + self.player + "_" + "swim1.png"

                
        if self.dive:                        
            self.ImageName = self.state+"_" + self.player + "_" + "swim1.png"

        if self.heading == 0 and not self.climbing:
            if self.LookingBack:
                self.ImageName = self.state + "_" + self.player + "_" + "spin2.png"
            else:
                self.ImageName = self.state + "_" + self.player + "_" + "spin1.png"
        
        self.image = self.images[self.ImageName]
        if key[pygame.K_q]:
            self.Death(Instantly = True)
                

    #마리오 파이프 들어갈 때 모습 똑바로(찌그러지지 않게)

    def Death(self,Instantly = False):
        if (self.starman and not Instantly) or self.calm:
            return
##        if not Instantly:
##            return

        if not Instantly and self.Gameclear:
            return

        self.DeadInstantly = Instantly #이 함수에서 Instantly 삭제 (중복되므로)
        if Instantly:
            self.pause = True
            pygame.mixer.music.stop()
            self.heading=1
            self.calm=False
            self.DeathMotion = True
            self.death=True
            self.speed=0
            
        else:
            if self.InvincibleTimer == 0 and not (self.death and not self.DeathMotion):
                if self.RidingYoshi:
                    self.RidingYoshi = False
                    self.yv = -10
                    self.SpinJump = False
                    self.Yoshi.runaway = True
                    self.Yoshi.MarioRiding = False
                    pygame.mixer.Sound("Sounds/smw_yoshi_runs_away.wav").play()
                    self.InvincibleTimer = 100

                elif self.cape:
                    if self.flying:
                        pygame.mixer.Sound("Sounds/smw_hit_while_flying.wav").play()
                        self.InvincibleTimer = 100
                        self.flying = False
                    else:
                        self.MoveTimer = -1
                        pygame.mixer.Sound("Sounds/smw_powerdown.wav").play()
                        self.PowerChange = True
                        self.howchanging = "Down"
                        self.InvincibleTimer = 100
                    
                elif self.fire:
                    self.MoveTimer = -1
                    pygame.mixer.Sound("Sounds/smw_powerdown.wav").play()
                    self.PowerChange = True
                    self.howchanging = "Down"
                    self.InvincibleTimer = 100
                elif self.MegamanMode:
                    self.MegamanMode = False
                    self.MMFire = False
                    pygame.mixer.Sound("Sounds/Ded.wav").play()
                    for i in range(8):
                        ExplosionParticle(self.rect.center,360 / 8 * i,5)
                        ExplosionParticle(self.rect.center,360 / 8 * i,8)
                    self.InvincibleTimer = 100
                    
                elif self.state == "big":
                    #print("ouch")
                    self.MoveTimer = -1
                    pygame.mixer.Sound("Sounds/smw_powerdown.wav").play()
                    self.PowerChange = True
                    self.howchanging = "Down"
                    self.InvincibleTimer = 100
                    
                else:
                    pygame.mixer.music.stop()
                    self.DeathMotion = True
                    self.pause = True
                    self.heading=1
                    self.calm = True
                    self.death = True
                    self.speed=0
                    

    def Deathmotion(self):
        #(0,1),(1,-1) / (self.heading, mario.heading)
        if self.DeadInstantly:
            if self.DeathTimer == 0:
                pygame.mixer.Sound("Sounds/deathEffect.WAV").play()
            if self.DeathTimer > 30:
                self.DeathMotion = False
                pygame.mixer.Sound("Sounds/death.wav").play()

        else:
            if self.DeathTimer == 0:
                pygame.mixer.Sound("Sounds/deathEffect.WAV").play()
                self.image = self.images[self.player+"_death.png"]
            if self.DeathTimer > 50:
                self.calm = False
                self.DeathMotion = False
                pygame.mixer.Sound("Sounds/death.wav").play()
                self.yv = -15
                
                
        

    def text_objects(self,text,size,color = (0,0,0)):
        textSurface=pygame.font.Font('PressStart2P-vaV7.ttf', size).render(text,True,color)#pygame.font.Font('Super-Mario-World.ttf',size)
        return textSurface,textSurface.get_rect()
                
    def playPsong(self):
        if not self.starman and not self.Gameclear:
            pygame.mixer.music.stop()
        if not self.Pactivated:
            self.Pactivated = True
        self.Pwarning = False
        pygame.mixer.Sound("Sounds/switch.wav").play()
        if not mario.starman and not self.Gameclear:
            pygame.mixer.music.load("BGM/P-Switch - Super Mario World.mp3")
            pygame.mixer.music.play(-1)

        self.Ptimer = pygame.time.get_ticks()
           
    def Physics(self):
        global FPS,stime,startTime
        
        self.RelativeHeight = False        

        if self.yv > 0:
            self.jumpable=False
        if not self.heading == 0:
            self.oldheading = self.heading
        
        self.ScreenShake(*self.ScreenShaking[1:3])   

        
        if self.InvincibleTimer > 0 and not self.pause:
            self.InvincibleTimer-=1
            if 66 < self.InvincibleTimer < 100:
                self.opacity = 64 + ((Globals.GlobalTimer // 6) % 2) * 191
            elif 33 < self.InvincibleTimer < 66:
                self.opacity = 64 + ((Globals.GlobalTimer // 3) % 2) * 191
            elif self.InvincibleTimer < 33:
                self.opacity = 64 + ((Globals.GlobalTimer // 1) % 2) * 191

        else:
            self.opacity = 255
            
        self.DisplayAddPos = [0,0]
        self.movement=[0,0]

        if self.starman:
            if pygame.time.get_ticks() - self.StarTimer >= 17000:
                self.starman = False
                self.Pwarning = False

        if self.JumpTimer > 0:
            self.JumpTimer -= 1
       
        if self.life > 999:
            self.BlackScreen = True

##        if self.Underwater and self.yv < 0:
##            if not self.jumpingout:
##                self.rect.y -= self.yv
##                for i in range(abs(int(self.yv))):
##                    self.rect.y -= 1
##                    for w in Waters:
##                        #print(int(self.rect.centery),int(w.rect.top))
##                        if int(self.rect.centery) == int(w.rect.centery) and w.IsSurface:
##                            self.yv = 0
##                            self.rect.centery = w.rect.centery
##                            break
##        self.Underwater = False
##        for w in Waters:
##            if self.rect.colliderect(w.rect):
##                if not self.jumpingout:self.Underwater = True
##
##        if not self.Underwater and self.yv > 0: self.jumpingout = False
                
        if key[pygame.K_DOWN]:
            if self.Underwater and self.holding:
                self.yv = 3
        #====RAPID FIRE CHEAT MODE=====
        if key[pygame.K_s] and False:
            if Globals.GlobalTimer % 2 == 0 and (self.fire or self.MegamanMode) and not self.SpinJump and not self.sitting and not self.SlippingDown and not self.pause:
                self.FireFireball()

        if key[pygame.K_SPACE]:
            FPS = 1
        elif key[pygame.K_CAPSLOCK]:
            FPS = 0
        else:
            FPS = 60

        if key[pygame.K_u]:#꼬맹이 마리오
            self.state = "small"
            self.fire = False
            self.cape = False
        if key[pygame.K_i]:#슈퍼 마리오
            self.state = "big"
            self.fire = False
            self.cape = False
        if key[pygame.K_o]:#망토 마리오만
            self.fire = False
            self.cape = True
            self.CapeDisplay = True
        if key[pygame.K_p]:#파이어 마리오만
            self.fire = True
            self.FireColorChange = True
            self.cape = False

        
        if key[pygame.K_LSHIFT]:
            self.rect.x -= 1
        if key[pygame.K_RSHIFT]:
            self.rect.x += 1
        #걍 Warning 으로 바꾸자
        if (self.Pactivated and 1950 <= 16000 - (pygame.time.get_ticks() - self.Ptimer) <= 2050) or (self.starman and 1950 <= 17000 - (pygame.time.get_ticks() - self.StarTimer) <= 2050) :
            #if not self.Pwarning:
            pygame.mixer.Sound("Sounds/smw_switch_timer_ending.wav").play()
                #self.Pwarning = True
                
        if self.Pactivated and pygame.time.get_ticks() - self.Ptimer >= 16000:
            self.Pactivated = False
            self.Pwarning = False
            if not mario.starman and not mario.Gameclear and not mario.death:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(Globals.BGM)
                pygame.mixer.music.play(-1)
            
        if self.speed == 0:
            if not self.Onslope:
                self.SlippingDown = False
            self.AbleToLimitSpd = False
        if self.Onslope and not self.RidingYoshi and not Globals.WaterTheme and not mario.holding:
            if key[pygame.K_DOWN] and not self.MegamanMode:
                self.sitting = False
                self.SlippingDown = True
                
        
        if self.collision_types['bottom']:
            if self.SpinJump:
                self.TurnAround = False
            if self.heading == 0 and not self.calm:##공중에서 돌 때 heading이 0이면 1이 되므로 어색해짐
                self.heading = 1
            self.SpinJump=False
            if not self.starman and not self.SlippingDown:
                self.combo = 1

        if self.combo > 8:
            self.combo = 8
            self.life += 1

        if not self.holding:
            self.Holded_Obj = None

        if not self.death and not self.pause:
            ScrollSpd = 1
            if not self.realend:
                if self.main:
                    self.scroll[0] += ((self.rect.centerx-self.scroll[0]- SW / 2 / 1 + self.ExtraScroll)/ScrollSpd) * (not self.AutoScroll) + Globals.AutoScrollVector[0] * self.AutoScroll
                    self.scroll[1] += ((self.rect.bottom-self.scroll[1] - SH)/5)# * (not self.AutoScroll) + Globals.AutoScrollVector[1] * self.AutoScroll# * (not self.AutoScroll)+ Globals.AutoScrollVector[1] * self.AutoScroll#300 * SH / 485 /1)/5 #bottom 으로 해야 앉을 때 스크롤이 안됨
                else:
                    self.scroll[0] += ((self.rect.centerx-self.scroll[0]- SW / 2 / 1 + self.ExtraScroll)/ScrollSpd) * (not self.AutoScroll) + Globals.AutoScrollVector[0] * self.AutoScroll
                    self.scroll[1] += ((self.rect.bottom-self.scroll[1] - SH * (2/3)) /ScrollSpd)# * (not self.AutoScroll) + Globals.AutoScrollVector[1] * self.AutoScroll#  * (not self.AutoScroll) + Globals.AutoScrollVector[1] * self.AutoScroll #300 * SH / 485 /1)/5 #bottom 으로 해야 앉을 때 스크롤이 안됨 / 300

                    
                if CRAZY:
                    self.scroll[0] += (self.rect.x-self.scroll[0]-random.randint(270,370) + self.ExtraScroll)/ScrollSpd
                    self.scroll[1] += (self.rect.bottom-self.scroll[1]-random.randint(270,370))/ScrollSpd #bottom 으로 해야 앉을 때 스크롤이 안됨

                if False:#진동 스크롤 
                    self.scroll[0] += (self.rect.x-self.scroll[0]-320-math.cos(Globals.GlobalTimer*0.03) * 100 + self.ExtraScroll)/ScrollSpd
                    #self.scroll[1] += (self.rect.bottom-self.scroll[1]- SH * (2/3) - math.sin(Globals.GlobalTimer*0.1) * 100)/5 #bottom 으로 해야 앉을 때 스크롤이 안됨

##            if self.scroll[1] >= 85:#485 -> 85
##                self.scroll[1] = 85
            #self.ScrollLimit = [[None,None],[None,None]]
            if self.ScrollLimit[0][0] == None:#나중에 각 맵에 기본 세팅에서 None대신 0으로 다 바꾸자!
                self.ScrollLimit[0][0] = 0
            if self.ScrollLimit[0][0] != None and self.scroll[0] <= self.ScrollLimit[0][0]:
                self.scroll[0] = self.ScrollLimit[0][0]
            elif self.ScrollLimit[0][1] != None and self.scroll[0] >= self.ScrollLimit[0][1]:
                self.scroll[0] = self.ScrollLimit[0][1]
            if self.ScrollLimit[1][0] != None and self.scroll[1] <= self.ScrollLimit[1][0]:
                self.scroll[1] = self.ScrollLimit[1][0]
            elif self.ScrollLimit[1][1] != None and self.scroll[1] >= self.ScrollLimit[1][1]:
                self.scroll[1] = self.ScrollLimit[1][1]
            
            if (self.collision_types['left'] or self.collision_types['right']):
                if (self.collision_types['right'] and key[pygame.K_LEFT]) or (self.collision_types['left'] and key[pygame.K_RIGHT]) or self.TurnAround:
                    self.speed = 1 * self.heading # For Wall Jumps -> 속도가 0이 되면 collision_types가 계속 바뀜, 따라서 계속 그 방향으로 가서 벽에 붙는 것이 인식이 되도록 속도 유지(벽 점프를 하려면 벽에 붙어야 하기 때문)
                else:
                    self.speed = 0
            
            if not self.pause: #정지시에는 마리오도 정지
                self.movement[0] += self.speed
                    

            

                        

        if key[pygame.K_l]:
            print(self.rect.x //32,self.rect.bottom//32)
        
        if abs(self.speed) == MaxPSpd + 1 * self.starman and pygame.time.get_ticks() - stime > 1900 and self.Pmeter == 6:
            stime = pygame.time.get_ticks()
            #pygame.mixer.Sound("Sounds/smb3_pmeter.wav").play()
        
        if not self.calm and not self.climbing and not self.pause and not self.RidingCloud or self.death:
            if self.ExtraBoost:#이 모양일 때는 빨리 떨어짐
                self.yv += 2
            elif self.Underwater:
                if self.holding:
                    self.yv -= 0.2
                else:
                    self.yv += 0.2
            else:
                if self.onplatform:
                    self.yv = 1
                else:
                    self.yv += Globals.GRAVITY#근데 이게 1보다 작으면 platform등에 고정이 제대로 안된다 -> 고치자

##        if self.Underwater and self.yv < 0:
##            if not self.jumpingout:
##                self.rect.y -= math.ceil(self.yv)
##                for i in range(abs(math.ceil(self.yv))):
##                    self.rect.y -= 1
##                    for w in Waters:
##                        #print(int(self.rect.centery),int(w.rect.top))
##                        if self.rect.colliderect(w.rect) and int(w.rect.top) < int(self.rect.centery) < int(w.rect.centery) and w.IsSurface:
##                            self.yv = 0
##                            self.rect.centery = w.rect.centery
##                            break
        if not self.death:
            self.PrevUnderwater = copy.deepcopy(self.Underwater)
            self.Underwater = False
            if Globals.WaterTheme:
                self.Underwater = True

##            for w in Waters:
##                if self.rect.colliderect(w.rect):
##                    if not self.jumpingout:
##                        if w.IsSurface:
##                            if self.rect.centery > w.rect.top:
##                                self.Underwater = True
##                                break
##                        else:
##                            self.Underwater = True
##                            break

            else:
                surf,norm = Globals.water_collision_test(self.rect)
                if not self.jumpingout:
                    for w in surf:
                        if self.rect.centery > w.top:
                            self.Underwater = True
                            break
                                
                    for w in norm:
                        if not self.jumpingout:
                            self.Underwater = True
                            break

            if not self.PrevUnderwater and self.Underwater:#방금 막 물에 들어갔을 때
                if self.yv > 0 and not self.collision_types["bottom"]:
                    self.yv = 0

                

        c = copy.deepcopy(self.rect.y)
        ck = False
        if self.Underwater and not self.jumpingout and self.yv < 0:#self.OnWaterTop 뭐 이런거라도 만들자
            for i in range(abs(int((self.yv)))):
                self.rect.y -= 1
                surf,norm = Globals.water_collision_test(self.rect)
                for w in surf:
                    if self.rect.centery == w.top:
                        self.yv = 0                   
                        self.rect.centery = w.top + 1
                        ck = True
                        break
                if ck:
                    break
                
        if not ck:
            self.rect.y = c

        #m    k
        #down down -> only can bounce if m > k
        #down up   -> can bounce
        #up   down -> cannot bounce
        #up   up   -> only can bounce if m < k
        if not self.Underwater and self.yv > 0 and self.jumpingout: self.jumpingout = False

        if not self.calm:
            if self.collision_types['top']:
                if not (self.cape and self.rising and self.SpinJump):
                    self.yv = 0
                

        if self.RidingCloud:
            self.movement[1] = self.yv
        else:
            if not self.pause or self.death:
                if self.yv < -15:
                    self.movement[1] = -15 #yv는 감소하지만 점프 높이는 15를 넘기지 않게(For cape)
                else:
                    self.movement[1] += self.yv

        self.onplatform = False
        self.onseesaw = False
        
        if not self.calm and not self.death:
            
            for i in seesaw.seesaws:
                okiedokie = False
                oldpos = mario.rect.center
               
                self.rect.y += i.yspd
##                for j in range(abs(int(self.yv))):
##                    self.rect.y -= 1
##                              
##                    if i.left[0] < self.rect.centerx  < i.right[0] and i.rely - 5 < self.rect.bottom < i.rely + 5 and self.yv > 0:
##
##                        self.onseesaw = True
##                mario.rect.center = oldpos   
                for j in range(abs(int(self.yv))):
                    self.rect.y += 1
                              
                    if i.left[0] < self.rect.centerx  < i.right[0] and i.rely - 5 < self.rect.bottom < i.rely + 20 + abs(self.yv) and self.yv > -3:
                        okiedokie = True
                        
                            
                mario.rect.center = oldpos
                i.marioison = False
                if okiedokie:
                    if self.SlippingDown:
                        
                        self.speed += -math.sin(i.angle) * 1
                    self.movement[1] += i.yspd
                    self.onseesaw = True
                    i.marioison = True
                    self.yv = 0
                    self.collision_types['bottom'] = True
                    self.rect.bottom = i.rely - 5
                                        
            if self.onseesaw:
                if key[pygame.K_DOWN] and not self.MegamanMode:
                    self.SlippingDown = True
                    if self.speed == 0:
                        self.speed = mario.heading * 2
                    if abs(self.speed) < 2:
                        self.speed = abs(self.speed) / self.speed * 2
                        
##            for i in 와리가리.rotatingplatforms:
##                for j in i.platforms:
##                    okiedokie = False
##                    oldcenter = self.rect.center
##                    self.rect.y += i.speedy
##                    for k in range(abs(int(self.yv))):
##                        self.rect.y += 1
##                        if self.rect.colliderect(j) and self.yv > 0 and self.rect.bottom < j.bottom + abs(self.yv):
##                            okiedokie = True
##                           
##                            break
##                    #self.rect.y -= i.speedy
##                    self.rect.center = oldcenter
##                    if okiedokie:# and abs(self.rect.bottom - j.top) < 16:
##                        
##                        
##                        
##
##                        self.rect.bottom = j.top
####                        if not self.collision_types['bottom']:
####                            
####                            self.rect.y -= abs(i.speedy)#abs(self.yv) - 1
##                        self.onplatform = True
##                        #self.yv = 0
##                        
##                        self.collision_types['bottom'] = True
##                        
##                        self.movement[0] += i.speed
            for j in 와리가리.rotatingplatforms:
                for i in j.platforms:
                    oldcenter = self.rect.center
                    self.rect.y += j.speedy
                    for k in range(abs(math.ceil(self.yv))):                      
                        self.rect.y += 1
                        if self.rect.colliderect(i):
                             if self.yv > 0 and i.top <= self.rect.bottom < i.top + 10:
                                self.onplatform = True
                                j.rect = i
                                self.standingplatform = j                                
                                break
                                
                    self.rect.center = oldcenter
                
                    if not self.onplatform:
                        Grounds.remove(i)

            for i in Platform.Platforms + 와리가리.swings:
                oldcenter = self.rect.center
 
                self.rect.y += i.speedy
                for j in range(abs(math.ceil(self.yv))):                      
                    self.rect.y += 1
                    if self.rect.colliderect(i.rect):
                        if self.yv > 0 and i.rect.top <= self.rect.bottom < i.rect.top + 10:
                                self.onplatform = True
                                self.standingplatform = i
                        
                                #self.movement[1] = -(i.rect.top - self.rect.bottom)
                                
                                break
                                
                self.rect.center = oldcenter
                
                if not self.onplatform:
                    Grounds.remove(i.rect)
                        #self.rect.bottom = i.rect.top

                        #self.movement[1] += (i.rect.top - self.rect.bottom)
                    


##                    self.onplatform = True
##                    #oldcenter = self.rect.center
##                    #oldspeed = self.movement[1]
##                    #self.rect.y += i.speedy
####                    while self.rect.colliderect(i.rect):
####                        if i.speedy != 0:
####                            self.rect.y += abs(i.speedy)/i.speedy
####                        else:break
##                    okiedokie = True
##                    #self.movement[1] -= self.yv - 1#self.rect.bottom + i.rect.top
##                    
##                    
##                    #self.rect.center = oldcenter
##                    #self.movement[1] -= oldspeed
##                    if okiedokie:
##                        #print(i.speedy)
##                        self.onplatform = True
##                        
##                        #self.movement[1] = i.speedy
##
##                        self.rect.bottom = i.rect.top
##                        self.Onslope = False
##                        #self.yv = 0
##                        
##                        self.collision_types['bottom'] = True
##                        
##
##
##
##                        
        if self.onseesaw:
            self.collision_types['bottom'] = True 
        if self.calm:
            self.hitlistsV, self.hitlistsH = [], []
            self.yv = 0
            self.collision_types['bottom'] = True 
            self.cannotmove = True
            self.climbing = False
            self.Turning = False
            self.LookingBack = False
            if not self.death:#죽었을때도 calm = True 이기 때문
                if self.PipeEnterType == "vertical":
                    self.speed = 0
                    
                    if self.RidingYoshi:
                        self.image = self.images[self.state+"_"+self.player+"_"+"yoshi_turn.png"]
                    else:
                        self.heading = 0
                    self.MoveMotion()
                
                else:
                    prev = copy.deepcopy(self.speed)
                    self.speed = 6 * self.heading #가짜 움직임으로 마치 걷는 것처럼
                    self.MoveMotion()
                    self.speed = prev
                
                
        else:
            self.stuck = False          

            #oldh = self.rect.height
    
            if self.RidingYoshi:
                pass# and not self.sitting and not self.attack:
                #self.rect.height = self.Yoshi.rect.height #높이가 요시랑 똑같으면 앉아있는 것처럼 보임(요시가 마리오를 따라다님)
                #요시처럼 탈 것에 타면 마리오의 높이를 그 탈것의 높이와 같게하라
                #요시가 방향을 틀 때는 마리오를 중심으로 돌아라(그래야 자연스러움)
                #self.rect.y -= self.rect.height - oldh

            bef = self.collision_types['bottom']
            self.rect,self.collision_types,self.hitlistsH,self.hitlistsV = self.move(self.rect,self.movement,Grounds+[i.rect for i in Things.Pswitchs if not i.holded and not i.eaten],Slopes,colObjs)# and i.collision_types['bottom']])
            
            if bef != self.collision_types['bottom']:
                
                if abs(self.speed) > 5:
                    self.onspd = abs(self.speed)
                    self.gotoffground = True
                else:
                    self.gotoffground = False
            if not bef and self.collision_types['bottom']:
                self.gotoffground = False
                
                
            
        if self.onseesaw:
            self.collision_types['bottom'] = True
          
        if self.collision_types['bottom'] and not self.death:
            self.yv = 0
        if self.onplatform:
            if self.yv > 0:
                self.collision_types['bottom'] = True
##        if self.RidingYoshi:         
##            self.Yoshi.rect.bottom = self.rect.bottom#self.Yoshi.Movemotion(self,Ground) #여기서 요시 혀와 괸련된 수행을 하고 self.attack를 False로 만들어 주는 곳
            #요시의 Movemotion을 여기서 담당하지 않으면 마리오가 제대로 땅에 안 붙어있음

        old = self.rect.bottom
        if self.MegamanMode:
            if self.Slide:
                self.rect.height = 32
            else:
                self.rect.height = 55

        self.rect.bottom = old
        if not self.death and not self.calm:
            try:
                if self.MegamanMode:
                    self.MegamanMotion()
                else:
                    self.MoveMotion()
            except KeyError as e:
                self.RelativeHeight = False
                self.player = "m"
                self.playername = "Mario"
                self.MoveTimer -= 1
                self.MoveMotion()
                #self.MegamanMotion()
                

        if self.Underwater:
            self.yvLimit = 4

        if self.yv > self.yvLimit:
            self.yv = self.yvLimit
        if self.Underwater:
            if self.holding:
                if self.yv < -self.yvLimit:
                    self.yv = -self.yvLimit
##            else:
##                if self.yv < -8:
##                    self.yv = -8

##        for i in Things.Pswitchs:
##            if not i.holded:
##                if i.rect in self.hitlistsH and (i.rect in self.hitlistsV):
        if not self.calm and not Globals.AutoScroll and False:#self.rect.x < 32 * 10:
                if self.rect.left - self.scroll[0] < 0:
                        self.rect.left = self.scroll[0]
                        self.speed = 0             
        if self.death:
            #(1,1),(2,1),(3,-1),(4,-1)
            self.heading = -2 * ((self.DeathTimer // 4) % 2) + 1
            #self.DeathTimer = 1 -> 1 - int(self.DeathTimer / 3) = 1
            #self.DeathTimer = 2 -> 1 - int(self.DeathTimer / 3) = 1
            #self.DeathTimer = 3 -> 1 - int(self.DeathTimer / 3) = -1
            #self.DeathTimer = 4 -> 1 - int(self.DeathTimer / 3) = -1
            if self.WaitAfterDeath >= 1:
                self.WaitAfterDeath += 1


                
            if self.DeathMotion:
                self.Deathmotion()
            elif True:#not pygame.mixer.Channel(0).get_busy():
                if self.rect.top - self.scroll[1] > 480:
                    self.BlackScreen = True
                    if self.WaitAfterDeath == 0:
                        self.WaitAfterDeath = 1
                        
            if self.WaitAfterDeath == 100:
                Globals.WaterTheme = False
                Globals.SnowTheme = False
                self.death = False
                self.BlackScreen = False
                self.WaitAfterDeath = 0
                self.life -= 1
                self.DeathTimer = -1
                Globals.MarioAt = Globals.StartLvlIdx
                ROM.initialize()
                ROM.LoadLevel(Globals.Lvidx,Globals.StartLvlIdx)

##                Globals.WaterTheme = True
##                Globals.AutoScroll = True

                #startTime = timer() # 타이머 초기화

                self.AutoScroll = Globals.AutoScroll
                self.ScrollLimit = Globals.ScrollLimit

                self.DeadInstantly = False
                self.speed = 0
                self.yv = 0
                self.state = "small"
                self.fire = False
                self.cape = False
                self.scroll = [0,0]
                self.rect.x, self.rect.bottom = Globals.StartPoint
                self.holding = False
                self.Holded_Obj = None

                self.RidingCloud = False
                self.pause = False
                self.calm = False
                self.cannotmove = False
                pygame.mixer.music.load(Globals.BGM)
                pygame.mixer.music.play(-1)
                
            self.DeathTimer += 1
        if self.AutoScroll:
            if self.rect.x - self.scroll[0] < -100:
                self.Death(Instantly = True)
                self.AutoScroll = False
            if self.AutoScroll and not self.calm:
                    if self.rect.right - self.scroll[0] > SW:
                        self.rect.right = 640 + self.scroll[0]
                        self.speed = 0
    
        
        if not self.realend:
            if self.rect.top > Ground.rangeY[1] * 32 + 32 and not self.death:
                
                self.Death(Instantly = True)
            if self.yv>=0 and self.collision_types['bottom']:
                self.jumping=False
            if self.Gameclear:
                self.AutoScroll = False
                self.cannotmove=True
                self.sitting=False
                if self.rect.x > [i for i in Goal.Goals if i.Done][0].x + 300:
                    self.speed=0
                    self.heading=-1
                else:
                    self.heading=1
                    self.holding=False
                    self.running=False
                    self.turning=False
                    self.sitting=False
                if not pygame.mixer.music.get_busy() and not self.walktoend:
                    if self.GotInRealGoal:
                        pygame.mixer.music.load("Sounds/Clear2.WAV")
                        pygame.mixer.music.play()
                        self.walktoend=True
                    else:
                        self.Death()
                        
            else:
                self.Run()
                    
            if self.walktoend:
                global tm
                tm+=1
                if tm>50:
                    self.speed=3
                    pygame.mixer.Sound("Sounds/smw_goal_iris-out.wav").play()
                    self.heading=1
                    syv=-10
                    self.realend=True

                else:
                    self.image=self.images[self.state+"_"+self.player+ "_yoshi" * self.RidingYoshi +"_"+"win.png"]
        else:
            self.running=True
            self.speed+=0.2
            if self.rect.x - self.scroll[0] > SW:
                print("Thanks for playing!")
                global sp_clearedLevels
                sp_clearedLevels += 1
                self.holding = False
                self.Holded_Obj = None
                Globals.Lvidx += 1
                Globals.LevelCount = 2
                Globals.WaterTheme = False
                Globals.SnowTheme = False
                Globals.AutoScroll = False
                
                Globals.CurrentPipes = []
                Globals.StartPoint = (32 * 10, 32 * 2)#임시
                Globals.RegisteredCPidx = -1#CP가 안 찍혀있도록 초기화
                ROM.initialize()
                Globals.StartLvlIdx = 0
                ROM.LoadLevel(Globals.Lvidx)
                self.AutoScroll = Globals.AutoScroll
                self.ScrollLimit = Globals.ScrollLimit
                Globals.MarioAt = 0
                self.speed = 0
                self.yv = 0
                tm = 0

                #startTime = timer() # 타이머 초기화
                self.rect.x, self.rect.bottom = Globals.StartPoint
                self.realend = False
                self.walktoend = False
                self.Gameclear = False
                self.cannotmove = False
                pygame.mixer.music.load(Globals.BGM)
                pygame.mixer.music.play(-1)

        if self.flying and not self.running:
            self.flying = False
        self.AirSpinTimer += 1
        if self.dive and self.speed == 0 and self.collision_types['bottom']:
            self.dive = False
##        self.FireTimer = 5
##        self.Fireball(self)
##        pygame.mixer.Sound("Sounds/smw_fireball.wav").play()
    

    def gameclear(self,RealGoal):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Sounds/Clear1.WAV")
        pygame.mixer.music.play()
        self.Ptimer=-9999
        self.Gameclear=True
        self.GotInRealGoal = RealGoal
        self.speed=3

    def WallJumpDetection(self,event):
        if not self.collision_types['bottom'] and not self.RidingYoshi and not self.Underwater:
            if self.collision_types['right']:
                if key[pygame.K_LEFT]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.rect.x += 1
                            self.yv = -10
                            self.speed = 8
                            self.collision_types['right'] = False
                            pygame.mixer.Sound("Sounds/mario-wa.WAV").play()
            if self.collision_types['left']:
                if key[pygame.K_RIGHT]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                    
                            self.rect.x -= 1
                            self.yv = -10
                            self.speed = -8
                            self.collision_types['left'] = False
                            pygame.mixer.Sound("Sounds/mario-wa.WAV").play()
    def FireFireball(self):
        if self.MegamanMode:
            if len(self.Fireballs) < 3000000 and not self.Slide:
                self.ShootTimer = 16
                self.Fireball(self,MM = True)
                pygame.mixer.Sound("Sounds/SE_BUSTER.wav").play()

        else:
            if len(self.Fireballs) < 2:
                self.FireTimer = 5
                self.Fireball(self)
                pygame.mixer.Sound("Sounds/smw_fireball.wav").play()

    def events(self,event):
        global idx,Temp,Target,again,CRAZY,easteregg
        if self.collision_types['bottom'] and self.JumpTimer > 0 and self.Prun and self.jumping:
            self.JumpTimer = 0  
        if easteregg == [pygame.K_a,pygame.K_d,pygame.K_a,pygame.K_d,pygame.K_v,pygame.K_v,pygame.K_s,pygame.K_s]:
            easteregg = [0] * 8
            self.player = "l"
            self.playername  = "Luigi"
        elif easteregg == [pygame.K_f,pygame.K_u,pygame.K_c,pygame.K_k,pygame.K_SPACE,pygame.K_y,pygame.K_o,pygame.K_u]:
            easteregg = [0] * 8
            print("NO BAD WORDS!")
            #self.life = 990
        elif easteregg == [pygame.K_s,pygame.K_e,pygame.K_u,pygame.K_n,pygame.K_g,pygame.K_w,pygame.K_o,pygame.K_o]:
            easteregg = [0] * 8
            print("ㅎㅇ")
        elif easteregg == [pygame.K_m,pygame.K_a,pygame.K_r,pygame.K_i,pygame.K_o,pygame.K_3,pygame.K_3,pygame.K_3]:
            self.Mario3 = True
            self.Mario1 = False
        elif easteregg == [pygame.K_m,pygame.K_a,pygame.K_r,pygame.K_i,pygame.K_o,pygame.K_1,pygame.K_1,pygame.K_1]:
            self.Mario1 = True
            self.Mario3 = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:#록맨
                self.fire = False
                self.cape = False
                self.MegamanMode = not self.MegamanMode

            for i in range(len(easteregg)):
                if i == 7:
                    easteregg[i] = event.key
                    break
                easteregg[i] = easteregg[i+1] #앞으로 한칸씩 밀기

            if event.key == pygame.K_n:
                pygame.mixer.music.stop()
                    
            
            if event.key == pygame.K_v:
                if self.player == "m":
                    self.player = "t"
                    self.playername  = "Toadette"
                else:
                    self.player = "m"
                    self.playername  = "mario"
            
            if event.key == pygame.K_d:
                if self.ExtraScroll <= 0:
                    self.ExtraScroll += 100
                
            elif event.key == pygame.K_a:
                if self.ExtraScroll >= 0:
                    self.ExtraScroll -= 100

            if not self.calm and not self.attack and not self.climbing:
                if event.key == pygame.K_LEFT: #반대 방향으로 틀었을 때
                    if self.heading == 1 or Target == 1:
                        Temp = True
                        idx = 2 #도는 것을 원할히 하기 위해 idx = 2
                        Target = -1
                elif event.key == pygame.K_RIGHT:
                    if self.heading == -1 or Target == -1:
                        Temp = True
                        idx = 2
                        Target = 1
             
            if not self.calm and not self.death:
                if event.key == pygame.K_TAB:
                    CRAZY = not CRAZY
                    if CRAZY:
                        mario.blurness = 2
                    else:
                        mario.blurness = 1
                if event.key == pygame.K_UP:
                    if self.RidingCloud:
                        self.RidingCloud = False
                        self.TheActualCloud.riding = False
                        self.TheActualCloud = None
                        self.yv -= 17
                        pygame.mixer.Sound("Sounds/Jump.wav").play()

                    if self.climbing:
                        self.climbing = False
                        self.yv -= 17
                        self.heading = self.oldheading
                        pygame.mixer.Sound("Sounds/Jump.wav").play()
                    if self.Underwater:
                        FullyInsideWater = True
                        surf, norm = Globals.water_collision_test(self.rect)
                        for w in surf:
                            if key[pygame.K_z]:#지금 waters가 unload가 안됨 -> 고치자/함수를 만들어 코드의 길이를 줄일까? / 그리고 물에서는 떨어지는 속도가 좀 느려야됨
                                self.yv = -17
                                self.jumpingout = True
                                self.Underwater = False
                                        
                        if not self.holding and not self.jumpingout or Globals.WaterTheme:
                            self.sitting = False
                            self.yv -= 5
                            self.MoveTimer = -1
                            
                            
                            self.swim = True
                            if self.yv > 7:
                                self.yv = 7
                            if self.yv < -7:
                                self.yv = -7
                            pygame.mixer.Sound("Sounds/smw_swimming.wav").play()

                
                if not self.jumping and (self.collision_types['bottom'] or self.Onslope) and not self.dive and not self.flying and not self.Underwater:
                    if event.key == pygame.K_DOWN:
                        if self.holding and self.Underwater:
                            pygame.mixer.Sound("Sounds/smw_swimming.wav").play()
                    if event.key == pygame.K_UP:
                        self.JumpTimer = 128
                        
                        self.onplatform = False #이게 있어야 platform에서 벗어날수 있음?
                        self.SlippingDown = False
                        self.Onslope = False
                        if abs(self.speed) == MaxPSpd + 1 * self.starman:
                            #self.RunJumping = True #달리는 동안에는 뛴 이후부터는 모양을 바꾸면 안됨
                            self.jumpcombo += 1
                        else:
                            self.jumpcombo = 0
                        
                        if self.cape and abs(self.speed) >= MaxPSpd + 1 * self.starman and not self.rising:
                            self.yv = -45
                            self.jumping = True
                            self.rising = True
                        else:
                            self.jumping = True
                            if self.MegamanMode:
                                if self.Slide and not key[pygame.K_DOWN]:
                                    self.Slide = False
                                    self.yv = -18
                                else:
                                    if key[pygame.K_DOWN]:
                                        self.Slide = True
                                        self.SlideTimer = 24
                                    else:
                                        self.yv = -18
                            else:
                                self.yv = -JUMPPOWER * (1 + abs(self.speed) / 45) * ((self.jumpcombo == 3) * 0.2 + 1)#15
                                if (self.Mario1 and self.state =="small"): pygame.mixer.Sound("Sounds/jump3.wav").play()

                                elif (self.Mario1 and self.state =="big") or self.Mario3: pygame.mixer.Sound("Sounds/smb_sound_effects_big_jump.wav").play()
                            
                                else: pygame.mixer.Sound("Sounds/Jump.wav").play()
                                
                                if self.jumpcombo == 2:
                                    if PLAYTRIPLEJUMPSOUND: pygame.mixer.Sound("Sounds/mario-wa.WAV").play()
                                    
                                if self.jumpcombo == 3:
                                    if PLAYTRIPLEJUMPSOUND: pygame.mixer.Sound("Sounds/Jump2.WAV").play() #wahoo
                                    self.jumpcombo = 0                            

                            self.Onslope = False
                    elif event.key == pygame.K_c and not self.Mario1 and not self.Underwater:
                        self.climbing = False
                        self.SlippingDown = False
                        self.Onslope = False
                        self.jumping = True
                        if self.cape and abs(self.speed) >= MaxPSpd + 1 * self.starman and not self.rising:
                            self.yv = -45
                            self.rising = True
                            self.SpinJump = True
                            self.TurnAround = True
                            self.collision_types['bottom'] = False

                            pygame.mixer.Sound("Sounds/Spin Jump.wav").play()
                            
                        elif not self.RidingYoshi:
                            if self.holding:
                                pygame.mixer.Sound("Sounds/Jump.wav").play()
                            else:
                                self.SpinJump=True
                                self.TurnAround = True
                                pygame.mixer.Sound("Sounds/Spin Jump.wav").play()
                        
                            self.yv=-15*(1+abs(self.speed)/60)#13
                            self.collision_types['bottom'] = False
                    
                        

                if self.RidingYoshi:
                    if event.key == pygame.K_c:
                        self.jumping=True
                        
                        if abs(self.speed) == MaxPSpd + 1 * self.starman:
                            self.RunJumping = True
                        if self.collision_types['bottom']:
                            pygame.mixer.Sound("Sounds/Spin Jump.wav").play()
                            self.SpinJump=True
                            self.collision_types['bottom']=False
                            self.speed = self.heading*-3
                            self.yv-=12

                        else:
                            self.SpinJump = False
                            self.yv=-20
                        self.TurnAround = True
                        
                        self.Yoshi.MarioRiding = False
                        self.RidingYoshi = False
                else:
                    if event.key == pygame.K_x:
                        if not self.dive:
                            self.dive = True
                            self.speed += self.heading * 8
                            self.yv -= 10
                    if event.key == pygame.K_s:
                        if (self.fire or self.MegamanMode) and not self.SpinJump and not self.sitting and not self.SlippingDown and not self.pause:
                            self.FireFireball()
                    if event.key == pygame.K_c:
                        if self.AirSpinTimer > 12 and self.yv > 0 and not True:
                            self.again = 1
                            self.TurnAround = True
                            self.TurnDirection = self.heading
                            if self.heading == 0:
                                self.TurnDirection = self.LookingBack * 2 - 1
                            self.yv -= 6
                            pygame.mixer.Sound("Sounds/WU_SE_PLY_SPIN_ONCE.wav").play()
                            self.AirSpinTimer = -1
                            self.MoveTimer = -1

                    if event.key == pygame.K_s and self.cape and not self.SpinJump:# and not self.TurnAround:
                        self.TurnAround = True
                        self.MoveTimer = -1
                        self.CapeAttack = True
                        self.TurnDirection = self.heading
                        if self.heading == 0:
                            self.TurnDirection = self.LookingBack * 2 - 1
                        self.again = 0 #공중에서 떨어지거나 올라갈 때 끊김없이하기 위해
                        pygame.mixer.Sound("Sounds/Spin Jump.wav").play()


                    if self.flying and ((self.heading == 1 and event.key == pygame.K_LEFT) or (self.heading == -1 and event.key ==  pygame.K_RIGHT)):
                    
                        if self.AbleToBoost and self.yv > 2:
                            if self.ExtraBoost:
                                self.yv = -30
                            else:
                                self.yv = -20
                            pygame.mixer.Sound("Sounds/smw_cape_rise.wav").play()
                        self.AbleToBoost = False
                        self.ExtraBoost = False
                        self.CapeTimer = 0
                       
                    
                        
                if (event.key == pygame.K_s) and self.RidingYoshi:
                    if self.Yoshi.holding:
                        pygame.mixer.Sound("Sounds/smw_yoshi_spit.wav").play()
                        self.Yoshi.holding = False
                        self.Yoshi.tongue.eatenObject.rect.center = self.Yoshi.tongue.rect.center
                        try:
                            self.Yoshi.tongue.eatenObject.ThrownBehavior(self,key[pygame.K_DOWN])
                        except:pass

                        self.Yoshi.tongue.eatenObject.eaten = False
                        self.Yoshi.tongue.eatenObject.reload()

                        self.Yoshi.tongue.eatenObject = None #이게 없으면 요시 입에서 무한으로 나옴 

                        
##                        self.Yoshi.mouth.eaten = False
##                       
##                        self.Yoshi.tongue.containment = None
##                        self.Yoshi.mouth.rect.center = self.Yoshi.tongue.rect.center
##                        self.Yoshi.mouth.speed = self.heading * 10
##                        self.Yoshi.holding = False
##                        self.Yoshi.mouth = None
                        
                    elif not self.attack:
                        self.attack = True
                        self.Yoshi.tongue.stretch = True
                        self.MoveTimer = -1
                        pygame.mixer.Sound("Sounds/smw_yoshi_tongue.wav").play()

                        self.image=self.images[self.state+"_"+self.player+"_"+"yoshi_attack1.png"]

                   
                
                #if event.key == pygame.K_SPACE:mario.gameclear()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_c:
                if self.jumping:
                    if self.yv<-5:
                        self.yv=-5


    def events2(self):
        global startpressing,a
        key=pygame.key.get_pressed()
        if not startpressing:
            startpressing=False

        if not self.calm:
            if self.jumpable and not self.jumping:
                if key[pygame.K_UP] or key[pygame.K_c]:
                    self.yv=-18
                    self.jumping=True
                    
##                    if self.yv > -10:
##                        startpressing=True
##                        self.yv-=a
##                        a+=1
##                    else:
##                        if startpressing:
##                            startpressing=False
##                            self.jumping=True
##                else:
##                    if startpressing:
##                        startpressing=False
##                        self.jumping=True

#위에 것도 충분히 작동함                    
                
                    
startpressing=False
a=0
##def MoveScreen():
##    global syv
##    os.environ['SDL_VIDEO_WINDOW_POS'] = "640,"+str(syv)
##    syv+=1
##
#mariok= Mario(32 * 15,0,"Mario",False)#6390
##
#luigi = Mario(32 * 20,0,"Luigi",False)#6390

#Globals.StartPoint[0],Globals.StartPoint[1] - 64,

toad = Mario(32 * 3,32 * 0,"Mario",False)#(15000,-1700,"Toadette",False)#13552+128,150 / 12052+128,150
##for i in range(5):
##    Mario(5365 + i *100,250,"Mario",False)

Grounds,Slopes,Waters=[],[],[]


#참고로 P스위치 누를 때 마리오 발바닥이랑 스위치 사이 거리 조사 후 밟음 처리하셈
def fill(surf, color):
    """Fill all pixels of the surface with color, preserve transparency."""

    surface = surf.copy()
    w, h = surface.get_size()
    surface.set_colorkey((0,0,0,0))
    surface.set_alpha()
    r, g, b, o= color
    Color = (r,g,b,o)#70)
    for x in range(w):
        for y in range(h):
            if surface.get_at((x,y))[0:3] != (0,0,0):
                surface.set_at((x, y),Color)#mix(list(surface.get_at((x, y)))))
    return surface
            
import random
img=pygame.image.load("Sprites/Blocks/P Switch/Blue Pressed.png")
#톰니바퀴 만들자
f=0
what = 0
I=0
k=0
chara = ["Mario","Luigi"]#,"Toadette"]
def blurSurf(surface, amt):
    if amt < 1.0:
        amt =1
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

def IsRectOnScreen(rect,mario): 
    return mario.rangeX[0] * 32 - rect.width <= rect.x <= mario.rangeX[1] * 32 and mario.rangeY[0] * 32 - rect.height <= rect.y <= mario.rangeY[1] * 32
    


def DrawMario(mario,image):
    if not mario.Nodisplay:            
        draw(mario,image)

        if mario.starman:
            mario.opacity = 128
            draw(mario,fill(mario.image,c))
            mario.opacity = 0


def draw(mario,image):
    w,h = image.get_width(),image.get_height()
    pos = (mario.rect.centerx - w / 2 - mario.scroll[0] + mario.DisplayAddPos[0] * mario.RidingYoshi,mario.rect.bottom - h-mario.scroll[1] + mario.DisplayAddPos[1] * mario.RidingYoshi)

    if mario.heading == 1 * (-2 * mario.MegamanMode + 1):
        blit_alpha(screen,image,pos,mario.opacity)
    elif mario.heading == -1 * (-2 * mario.MegamanMode + 1) or mario.heading == 0:
        blit_alpha(screen,pygame.transform.flip(image,True,False),pos,mario.opacity)

    else:
        if mario.climbing:
            blit_alpha(screen,image,(mario.rect.centerx - w / 2-mario.scroll[0],mario.rect.bottom - h-mario.scroll[1]),mario.opacity)

#mario powerdown 할 때 문제들 수정

#들고 있던 물건들이 마리오에서 처음으로 벗어난 후 작동해야함 (p switch 도)
L=0
c = pygame.Color(0,0,0)
c2 = pygame.Color(0,0,0)

CRAZY = False
img = pygame.transform.scale(pygame.image.load("totalblack.png").convert_alpha(),(int(SW * 0.5),int(SH * 0.5)))#Effect/ef_blackout.png"),(1440,1080))
re = img.get_rect()
gay = pygame.image.load("totalblack.png").convert_alpha()

#tracemalloc.start()
MEM = 0
OLDMEM = 0

TestImage = Globals.trans_img_size(pygame.image.load("Sprites/Still1.png"),3,alpha = False)
def random_set():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

#====THIS CODE BELOW SHOULD BE MODIFIED WHEN NECESSARY!!!=====#
pygame.event.set_allowed([QUIT])#, KEYDOWN, KEYUP]) #Does this even work?
#=============================================================#



#Colliding Objects 라고 list 만들자
#All enemies 만들자
elapsed_time = 0
while True:
    remaining_time = 300 - elapsed_time

    #OLDMEM = copy.deepcopy(MEM)
    #tracemalloc.clear_traces()
    Globals.loop(marios[0])
    screen.fill((0,0,0))

    

    for event in pygame.event.get():
        for mario in marios:
        
            if not mario.cannotmove:
                if not mario.MegamanMode:
                    mario.WallJumpDetection(event)
                mario.events(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if mario.WaitForB:
                if event.key in [pygame.K_c,pygame.K_s]:
                    mario.GamePause = False
                    mario.pause = False
                    mario.WaitForB = False
                    mario.TargetText.activated = False
                    mario.TargetText.decrease = True
            else:
                if event.key == pygame.K_RETURN:
                    if not mario.Gameclear and not mario.death:
                        pygame.mixer.Sound("Sounds/smw_pause.wav").play()
                        if mario.GamePause:#저 GamePause를 Globals에 넣는게 낫지 않을까...?
                            mario.GamePause = False
                            mario.pause = False
                            pygame.mixer.music.unpause()
                        else:
                            mario.GamePause = True
                            mario.pause = True
                            pygame.mixer.music.pause()

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
##    if sp_clearedLevels == 5:
##        screen.fill((0,128,0))
##        
##
##        TS,TR = toad.text_objects("CONGRATULATIONS!",16,(255,255,255))
##        TR.center = (SW / 2, SH / 2)
##        screen.blit(TS,TR)
##        
##        TS,TR = toad.text_objects("YOUR TIME IS: " + str(int(elapsed_time // 60)) + " min " + str(int(elapsed_time % 60)) + " seconds",12,(255,255,255))
##        TR.center = (SW / 2, SH / 2 + 30)
##        screen.blit(TS,TR)
##
##        screen2.blit(screen,ScreenPos)
##        pygame.display.update()    
##        CLOCK.tick(FPS)
##
##        continue
    
    for mario in marios:

        
        mario.PlatformSpd = [0,0]
        
        if type(ROM.Levels[Globals.Lvidx]) == str:
            name = ROM.Levels[Globals.Lvidx]
        else:
            name = ROM.Levels[Globals.Lvidx][Globals.MarioAt]
        pygame.display.set_caption("Super Mario World - {} - Life: {} - Coin: {} - FPS: {}".format(name,mario.life,mario.coin,int(CLOCK.get_fps())))#,str(OLDMEM/1024)[:4])

        if mario.life == 0:
            pygame.draw.rect(screen,(255,0,0),(0,0,640,485))
            pygame.mixer.music.stop()

            TS,TR = mario.text_objects("GAME OVER",16)
            TR.center = (320,240)
            screen.blit(TS,TR)

            TS,TR = mario.text_objects("You came up to stage " + str(sp_clearedLevels + 1),12,(255,255,255))
            TR.center = (320,240 + 32)
            screen.blit(TS,TR)

            TS,TR = toad.text_objects("YOUR TIME IS: " + str(int(elapsed_time // 60)) + " min " + str(int(elapsed_time % 60)) + " seconds",12,(255,255,255))
            TR.center = (SW / 2, SH / 2 + 60)
            screen.blit(TS,TR)


##            TS,TR = mario.text_objects("Copyright (c) 2019 - 2023 suhoihn",16)
##            TR.center = (320,440)
##            screen.blit(TS,TR)
            continue
        if not mario.GamePause:
            elapsed_time = int(timer() - startTime)
        if mario.life > 999:
            pygame.draw.rect(screen,(255,0,0),(0,0,640,485))
            pygame.mixer.music.stop()
            TS,TR = mario.text_objects("1000목숨 어케 모았누",40)
            TR.center = (320,240)
            screen.blit(TS,TR)

            TS,TR = mario.text_objects("copyright (c) 2019 - 2022 suhoihn",15)
            TR.center = (320,300)
            screen.blit(TS,TR)
            continue

        #mario.blurness = random.random() * 10
        
        global key
        key=pygame.key.get_pressed()
        I %= 640
        
        if mario.starman:
            f+=20
            
            if Globals.GlobalTimer % 2 == 0:
                Effects.Effect(random.randint(mario.rect.left,mario.rect.right),random.randint(mario.rect.top,mario.rect.bottom),4)
            if f==20:
                mario.combo = 1
                pygame.mixer.music.load("BGM/Super Mario World- Starman Extended.mp3")
                pygame.mixer.music.play(-1)
            I+=1
            c.hsla=((I/2+f)%360,50,50,100)

        else:
            k=1
            mario.starman=False
            if f!=0 and not mario.death and not mario.Gameclear:
                pygame.mixer.music.load(Globals.BGM)
                pygame.mixer.music.play(-1)
            f=0


        
        c2.hsla = ((Globals.GlobalTimer * 10) % 360,50,50,100)
        if CRAZY:
            screen.fill(c2)
        BackGround.loop(screen,mario)
        mario.events2()
        
        
        for j in marios:
            j.scroll[0] = sum([k.scroll[0] for k in marios]) / len(marios)#self.scroll =  marios[0].scroll
            j.scroll[1] = sum([k.scroll[1] for k in marios]) / len(marios)#self.scroll =  marios[0].scroll

        Ground.Waterloop(screen,mario)
        Goal.loop(screen,mario)

        PureGrounds,Slopes,Waters = Ground.loop(screen,mario)
        cape.loop(screen,mario)
        Vine.loop(screen,mario,Grounds)
        Grounds = []
        colObjs = [] #stores every objects that are collidable (Regardless of the status)
        #Grounds += PureGrounds

        #생성, 파괴시에만 업데이트 되는걸로?
        colObjs += Pipe.pipes
        colObjs += Firebar.Firebars
        colObjs += Platform.Platforms
        #colObjs += Block.Blocks
        
        colObjs += Cannon.Cannons
        colObjs += Spike.Spikes
        colObjs += 와리가리.swings
        colObjs += 와리가리.rotatingplatforms
        colObjs += [i for i in Spring.Springs if not i.holded]
        colObjs += Things.Pswitchs
        #이렇게 해 놓고 각 collision objects마다 식별 할 수 있는 ID 같은게 필요함

        Grounds += [i.rect for i in Pipe.pipes]# if IsRectOnScreen(i.rect,mario)]
        Grounds += [i.rect for i in Firebar.Firebars if IsRectOnScreen(i.rect,mario)]
        Grounds += [i.rect for i in Platform.Platforms]# if mario.yv > 0]# and i.rect.top <= mario.rect.bottom + i.speedy <= i.rect.top + 10]

        for i in Block.Blocks:
            if IsRectOnScreen(i.rect,mario) or i.type == "OnOffSwitch":
                if i.type == "ActiveWhenP":
                    if mario.Pactivated:
                        if not i.hit:      
                            Grounds.append(i.rect)
                            colObjs.append(i)
                       
                elif i.type == "QBlock":
                    if not i.Invisible:
                        Grounds.append(i.rect)
                        colObjs.append(i)
                        
                elif i.type == "BreakableBlock":
                    if i.ContainmentType == None:
                        if not i.hit and not mario.Pactivated:
                            Grounds.append(i.rect)
                            colObjs.append(i)
                    else:
                        Grounds.append(i.rect)
                        colObjs.append(i)
                        
                elif i.type == "OnOffSwitch":
                    Grounds.append(i.rect)
                    colObjs.append(i)
                    
                elif i.type == "OnOffBlock":
                    if i.state == Block.OnOffState:
                        Grounds.append(i.rect)
                        colObjs.append(i)
                    
                elif i.type == "cerment_brick": #모든 type에 경우에 따라 분류함
                    Grounds.append(i.rect)
                    colObjs.append(i)

                elif i.type == "Cloud": 
                    Grounds.append(i.rect)
                    colObjs.append(i)
                elif i.type == "TextBlock": 
                    Grounds.append(i.rect)
                    colObjs.append(i)

            
        
        
        Grounds+=[j for i in Cannon.Cannons for j in i.rects if IsRectOnScreen(j,mario)]
        Grounds+=[i.rect for i in Spike.Spikes if IsRectOnScreen(i.rect,mario)]

        #저거 위에 없애면 빨라지긴 하는데 쉘이 리스폰이 안됨;;

        
        Grounds+=[i.rect for i in 와리가리.swings]# if mario.yv > 0]
        Grounds+=[j for i in 와리가리.rotatingplatforms for j in i.platforms]
        Grounds+=[i.rect for i in Spring.Springs if not i.holded]

        #Grounds = sorted(Grounds, key = lambda r:r.x)
        Yoshi.loop(screen,Grounds,mario)

        if (not mario.death and not mario.LayorTop and not mario.holding) or mario.heading == 0:
            DrawMario(mario,mario.image)

        Yoshi.draw(screen,Grounds,mario)
        Firebar.loop(screen,mario)
        Coin.loop(screen,mario)

        Enemy.loop(screen,Grounds,mario,Slopes)
        Mushroom.loop(screen,mario,Grounds,Slopes)#나올때 블록 뒤에서 나와야됨
        Block.loop(screen,mario)
        
        
        Thwomp.loop(screen,Grounds,mario)
        
        Cannon.loop(screen,mario)
        
        
        Spiny.loop(screen,mario,Grounds)
        Spring.loop(screen,mario,Grounds)
        

        Platform.loop(screen,mario)
        와리가리.loop(screen,mario)
        Things.loop(screen,mario,Grounds)

        Spike.loop(screen,mario)
        seesaw.loop(screen,mario)

        for i in mario.Fireballs:
            if not mario.GamePause:
                i.Physics(Grounds,Slopes,mario)
            screen.blit(i.image,(i.rect.x - mario.scroll[0], i.rect.y - mario.scroll[1]))
        

##        if mario.death:
##            if mario.DeathTimer == 1:
##                with open("deaths.txt","r+") as f:
##                    DeathSpots = eval(f.readline())
##                    DeathSpots.append((mario.rect.x,mario.rect.y))
##                    f.close()
##                with open("deaths.txt","w") as f:
##                    f.write(str(DeathSpots))
##                    f.close()
##            else:
##                for i in DeathSpots:
##                    screen.blit(deathimage,(i[0] - mario.scroll[0], i[1] - mario.scroll[1]))
##        else:
##            DeathSpots = []
        Galumba.loop(screen,mario,Grounds)
        if (mario.death or mario.LayorTop) or (mario.holding and mario.heading != 0):
            DrawMario(mario,mario.image)


        Pipe.loop(screen,mario)
        Lakitu.loop(screen,mario)
        
        Effects.loop(screen,mario)
        
        if mario.Mario1:
            mario.holding = False

        if not mario.GamePause:
            mario.Physics()

        if mario.Mario1:
            mario.holding = True
            
        if mario.RidingYoshi:
            mario.holding = False
        
        if key[pygame.K_l]:
            print(mario.rect.centerx // 32,mario.rect.bottom // 32)
##        img = pygame.transform.scale(gay,(int(SW * (1 * math.sin(Globals.GlobalTimer * 0.1) + 1)),int(SH * (1 * math.sin(Globals.GlobalTimer * 0.1) + 1))))#Effect/ef_blackout.png"),(1440,1080))
##        re = img.get_rect()
##
##        re.center = mario.rect.center
##        if not mario.starman:
##            screen.blit(img,(re.x - mario.scroll[0],re.y - mario.scroll[1]))
##            r1 = pygame.Rect((0,0,SW,re.y - mario.scroll[1]))
##            r2 = pygame.Rect((0,re.y - mario.scroll[1] + re.height,SW,SH - (re.y - mario.scroll[1] + re.height)))
##
##            r3 = pygame.Rect((0,0,re.x - mario.scroll[0],SH))
##            r4 = pygame.Rect((re.x - mario.scroll[0] + re.width,0,SW - (re.x - mario.scroll[0] + re.width),SH))
##
##            pygame.draw.rect(screen,(0,0,0),r1)
##            pygame.draw.rect(screen,(0,0,0),r2)
##            pygame.draw.rect(screen,(0,0,0),r3)
##            pygame.draw.rect(screen,(0,0,0),r4)

        #str(remaining_time // 100) + str(remaining_time % 100 // 10) + str(remaining_time % 10)
##        TS,TR = mario.text_objects("Life: " + str(mario.life),16,color = (255,255,255))
##        TR.topleft = (0,SH - 32)
##        screen.blit(TS,TR)
##
##        TS,TR = mario.text_objects("Elapsed Time: " + str(int(elapsed_time)),16,color = (255,255,255))
##        TR.topleft = (0,SH - 16)
##        screen.blit(TS,TR)


        if mario.BlackScreen:
            pygame.draw.rect(screen,(0,0,0),(0,0,640,485))
    
    #pygame.draw.rect(screen,(255,0,0),(mario.rect.x-mario.scroll[0],mario.rect.y-mario.scroll[1],mario.rect.width,mario.rect.height))
##    for i in range(6):
##        if i < mario.Pmeter:pygame.draw.polygon(screen,(255,0,0),((120 + 20 * i,410),(100 + 20 * i,420),(100 + 20 * i,400)))
##        else: pygame.draw.polygon(screen,(255,255,255),((120 + 20 * i,410),(100 + 20 * i,420),(100 + 20 * i,400)))

        if mario.calm or CRAZY:
            screen = blurSurf(screen,mario.blurness)
        for i in ExplosionParticles:
            i.loop(mario)
            screen.blit(ExplosionImage[(Globals.GlobalTimer // 4) % 5],(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))


##        mag = 0.25#1.2 + 0.5 * math.sin(Globals.GlobalTimer / 10)
##        finalscreen = pygame.transform.scale(screen,(SW * mag,SH * mag))
##        ScreenPos = (-SW * 0.5 * (mag - 1),-SH*0.5 *(mag - 1))

    if CRAZY:
        blit_alpha(screen2,screen,(0,0),64)
    else:
        screen2.blit(screen,ScreenPos)

    
    #TEST IMAGE
##    TestImage.set_palette([(0,0,0,255),(0,0,0),random_set(),random_set()])
##    for i in range(1):
##        screen2.blit(TestImage,(i * 10,i))

    pygame.display.update()    
    CLOCK.tick(FPS)

    MEM = tracemalloc.get_traced_memory()[0]    

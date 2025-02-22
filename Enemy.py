#Enemy
import pygame,cape,math,Effects,Block,copy,os,Globals
from Globals import SW,SH
import random
KoopaTroopas = []
Koopas = []

Memory = []#This acts like ROM

AllImages = {}
AllTypes = ["Koopa","BuzzyBeetle","Spiny"]
for Type in AllTypes:
    file_list = os.listdir("./Sprites/" + Type)
    for i in file_list:
        if Type in ["Koopa","Spiny"]:
            AllImages[i] = Globals.trans_img_size(pygame.image.load("Sprites/" + Type +"/" + i),2)
            #여기는 등껍질 속에 있는 알맹이 이미지도 포함

        else:
            AllImages[i] = Globals.trans_img_size(pygame.image.load("Sprites/" + Type +"/" + i),1)

#pygame.transform.scale(pygame.image.load("Sprites/Koopa/Koopa_KickedOff1.png"),(30,32)).convert_alpha()

Needles = []
temp = Globals.trans_img_size(pygame.image.load("Sprites/Spiny/SpinySpike.png"),2)
NeedleImages = []
for i in range(8):
    NeedleImages.append(pygame.transform.rotate(temp,-45 * i))
del temp

NeedleSpd = 3
from math import *
def calc_proj_vx(p1,p2,Vy,g = 1):#Vy는 양수여야됨,g는 중력가속도           
    dx = p2[0] - p1[0]
    dy = abs(p2[1] - p1[1])
    
    #g = 1
    t1 = Vy / g
    t2 = sqrt( (2 * dy / g) + (Vy / g) ** 2 )
    t = t1 + t2
    Vx = dx / t

    return Vx

class SpinyNeedle:
    def __init__(self,center,direction):#dir 0 - up, 1 - right, 2 - down, 3 - left...
        self.direction = direction

        self.rect = pygame.Rect(0,0,8,8)#히트박스 조정
        self.rect.center = center
        if direction == 0: self.moveDir = (0,-1)
        if direction == 1: self.moveDir = (1,-1)
        if direction == 2: self.moveDir = (1,0)
        if direction == 3: self.moveDir = (1,1)
        if direction == 4: self.moveDir = (0,1)
        if direction == 5: self.moveDir = (-1,1)
        if direction == 6: self.moveDir = (-1,0)
        if direction == 7: self.moveDir = (-1,-1)


        Needles.append(self)
    def loop(self,mario):
        self.rect.centerx += self.moveDir[0] * NeedleSpd
        self.rect.centery += self.moveDir[1] * NeedleSpd
        if mario.rect.colliderect(self.rect): mario.Death()
        if not Globals.IsRectOnScreen(self.rect,mario): Needles.remove(self)
        

class Koopa:
    def __init__(self,x,y,KickedOff,heading):
        self.image = AllImages["Koopa_KickedOff1.png"]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.KickedOff = KickedOff
        self.heading = heading  
        self.yv = 0
        self.abc = 0
        self.speed = 0
        self.movement = [0,0]
        self.MotionTimer = 0
        self.Dead = False
        self.stomped = False
        self.mix = False
        self.EnteringShell = None
        self.Onslope = False
        self.TempInvincibleTimer = 16#처음 16프레임동안은 무적
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        Koopas.append(self)
        
    def Physics(self,Ground,mario,Slope):
        if self.TempInvincibleTimer > 0: self.TempInvincibleTimer -= 1
        self.movement = [self.speed, self.yv]
        if self.stomped:#밟혔을 때 
            if self.MotionTimer > 20:
                Koopas.remove(self)
        else:
            self.rect, self.collision_types = self.move(self.rect,self.movement,Ground,Slope)
            
            if self.collision_types['bottom']:
                if not self.Dead:
                    self.yv = 0
                self.speed *= 0.7 #여기에 있어야 속도를 유지해야 하는 구간에서도 영향을 안 받음

            self.yv += 0.8
            if abs(self.speed) < 1:
                self.speed = 0

            if self.Dead:#걷어 차이거나 구르는 껍데기에 맞았을 때
                self.speed = self.heading * 3
                self.image = AllImages["Koopa_KickedOff1.png"]

            else:
                for i in KoopaTroopas:
                    if self.mix:
                        self.abc += 1
                        if self.abc == 1:
                            self.yv = -8
                            self.speed = 4 * self.heading
                        if self.rect.centerx * self.heading > self.EnteringShell.rect.centerx * self.heading:
                            self.abc = 0
                            self.EnteringShell.ShellEmpty = False
                            self.EnteringShell.FlippedAngle = 0
                            self.EnteringShell.ShellInsideTimer = 440
                            Koopas.remove(self)
                            return
                      
                    if self.rect.colliderect(i.rect) and not self.mix and not self.KickedOff:
                        if i.state == "Dead" or i.state == "Normal":
                            if not i.ShellEmpty:
                                self.heading *= -1
                                i.heading *= -1
                            
                                #self.rect.x += self.heading * 4
                        elif i.state == "Roll":
                            self.Dead = True
                            self.yv = -5
                            i.combo +=1
                            if i.combo > 8:
                                i.combo = 8
                                mario.life += 1
                            pygame.mixer.Sound("Sounds/combo"+str(i.combo)+".WAV").play()

                            
                    self.rect.x += 30 * self.heading
                    if self.rect.colliderect(i.rect) and not self.mix and not i.holded and i.state == "Dead" and i.type == "Koopa":
                        if i.ShellEmpty and not self.KickedOff:
                            self.mix = True
                            self.EnteringShell = i
                    self.rect.x -= 30 * self.heading


                if self.KickedOff:
                    if self.MotionTimer == 0:
                        self.speed = self.heading * 10
                        
                    if self.MotionTimer % 10 == 0:
                        self.image = AllImages["Koopa_KickedOff1.png"]
                    elif self.MotionTimer % 10 == 5:
                        self.image = AllImages["Koopa_KickedOff2.png"]
                    if self.MotionTimer > 110:
                        self.KickedOff = False
                        
                        
                    if self.rect.colliderect(mario.rect) and self.TempInvincibleTimer == 0:
                        self.Dead = True
                        pygame.mixer.Sound("Sounds/smw_kick.wav").play()
                        self.yv = -5
                        
                        
                else:
                    self.speed = self.heading * 2
                    if self.MotionTimer % 10 == 0:
                        self.image = AllImages["Koopa_walk1.png"]
                    elif self.MotionTimer % 10 == 5:
                        self.image = AllImages["Koopa_walk2.png"]

                    if self.collision_types['left'] or self.collision_types['right']:
                        self.heading *= -1
                        self.speed = 0

                    if self.rect.colliderect(mario.rect):
                        if mario.rect.bottom - self.rect.top < 20 and mario.movement[1] > 0:
                            if mario.SpinJump:
                                pygame.mixer.Sound("Sounds/stomp2.wav").play()
                                mario.yv = -3
                                Effects.Effect(mario.rect.centerx,mario.rect.bottom,2,particles = True,TI = 2)
                                Koopas.remove(self)
                                return #아래 명령은 실행 되면 안됨
                            else:
                                oldpos = self.rect.bottom
                                self.image = AllImages["Koopa_stomped.png"]
                                self.rect.height = self.image.get_height()
                                self.rect.bottom = oldpos
                                self.stomped = True
                                mario.yv = -10
                                mario.jumpable = True
                                mario.jumping = False
                                mario.combo += 1
                                if mario.combo > 8:
                                    mario.life += 1
                                    mario.combo = 8
                                pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()
                                self.MotionTimer = 0
                                self.speed = 0
                        else:
                            mario.Death()

        self.MotionTimer += 1
            
    def collision_test(self,rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        
        return hit_list

    def move(self,rect,movement,tiles,slopes):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        if not self.Dead:
            rect.y += 20
            self.Onslope = False
            for ramp in slopes:
                hitbox = ramp.rect
                if rect.colliderect(hitbox):
                    rel_x = rect.x - hitbox.x

                    if ramp.heading == "NE":
                        pos_height = rel_x + hitbox.width 
                    elif ramp.heading == "NW":
                        pos_height = 32 - rel_x 
                    elif ramp.heading == "ENE1" or ramp.heading == "ENE2":
                        pos_height = 0.5 * (rel_x + hitbox.width) + 16
                    elif ramp.heading == "WNW1" or ramp.heading == "WNW2":
                        pos_height = 0.5 * (32 - rel_x) + 16
                    else:
                        pos_height = 69
                        
                    pos_height = min(pos_height, 32)
                    pos_height = max(pos_height, 0)
                    target_y = hitbox.y + 32 - pos_height
                    
                    if rect.bottom > target_y:
                        
                        rect.bottom = target_y

                        collision_types['bottom'] = True
                        self.Onslope = True
                        
            if not self.Onslope:
                rect.y -= 20
            
        rect.x += movement[0]
        hit_list = Globals.collision_test(rect,tiles)
        if not self.Dead:
            for tile in hit_list:
                if movement[0] > 0:
                    rect.right = tile.left
                    collision_types['right'] = True
                elif movement[0] < 0:
                    rect.left = tile.right
                    collision_types['left'] = True

        rect.y += movement[1]
        hit_list = Globals.collision_test(rect,tiles)
        if not self.Dead:
            for tile in hit_list:
                if movement[1] > 0:
                    rect.bottom = tile.top
                    collision_types['bottom'] = True
                elif movement[1] < 0:
                    rect.top = tile.bottom
                    collision_types['top'] = True
            
        return rect, collision_types
            
            
        

OldAngle = 0
WingImages = [Globals.trans_img_size(pygame.image.load("Sprites/Props/wing1.png"),2),
              Globals.trans_img_size(pygame.image.load("Sprites/Props/wing2.png"),2)]
              
              
class KoopaTroopa: #Shell
    def __init__(self,x,y,Type = "Koopa", OnlyShell = False, Tlist = None, winged = False, Thrown = False,heading = 1):
        self.type = Type
        self.x = x
        self.y = y
        self.holded = False
        self.Dead = False
        self.IsInsideMario = False

        self.Flip = False#도는 동안만 활성화
        if OnlyShell:
            self.ShellEmpty = True
            self.state = "Dead"
        else:
            self.ShellEmpty = False
            self.state = "Normal"

        self.Onslope = False
        self.Onslope2 = False

        self.alreadyHit = False
        self.hitFrom = 0

        self.OnlyShell = OnlyShell

        self.EscapeTarget = None


        self.RightAfterThrowing = False

        self.Flipped = False#뒤집히면 항상 활성화
        self.Shaking = False
        
        self.yv = 0
        self.speed = 0

        self.movement = [0,0]
        self.heading = heading#-1

        self.NotHoldingRightAfterJumpingTimer = 0 #마리오가 뛰자마자 껍데기를 잡지 못하게 함
        self.AvailableTimer = 0 #껍데기를 던지고 마리오가 맞아도 안 죽는 시간
        self.NotKickingRightAfterThrowingTimer = 0 #던지자 마자 차는거 방지용
        self.MoveTimer = 0 #모션

        self.CanStepOnIt = True

        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}

        self.combo = 1
        self.FlippedAngle = 0
        self.ShellInsideTimer = 0

        
        self.image = AllImages[Type + "1.png"]
        self.rect = self.image.get_rect()
        #self.rect.height = 32
        self.rect.topleft = (x,y)

        self.winged = winged
        self.marioOn = False
        self.lastPos = 0
        self.solid = False

        self.eaten = False
        
        #====For Spiny====#
        self.Alternation = False#바늘을 정방향, 대각선으로 쏠지 결정(True - 정방향, False - 대각선)
        self.Thrown = Thrown
        self.ThrownInit = Thrown#1회 반복용, init에서는 mario가 인자로 없어서 실행 불가        
        if Tlist == None:
            KoopaTroopas.append(self)
        else:
            Tlist.append(self)
        self.marioAway = False
        
    def reload(self):
        KoopaTroopas.append(self)

        
    def ray(self,Ground):
        if self.state == "Normal" and self.collision_types['bottom']:
            if self.heading == 1:
                r2 = pygame.Rect(self.rect.right + self.speed + 1,self.rect.bottom + 1,1,1)
            else:
                r2 = pygame.Rect(self.rect.left - self.speed - 1,self.rect.bottom + 1,1,1)

            if Globals.collision_test(r2,Ground) == []:# and Globals.slope_collision_test(r2) == None:
                self.heading *= -1


            
            
        
    def ThrownBehavior(self,mario,keydown,yoshi = False):#parameter = (looking up, sitting) etc...
        #print("throw shell, key: ", keydown)
        if mario.LookingUp:
            k = mario.heading
            if mario.heading == 0:
               k = 1 #0일때 맞는 것은 불가능 하므로
            self.rect.y -= 30
            self.speed = abs(mario.speed) * mario.heading * 0.5
            self.NotKickingRightAfterThrowingTimer = 20
            pygame.mixer.Sound("Sounds/smw_kick.wav").play()
        else:
            if keydown:
                self.NotKickingRightAfterThrowingTimer = 20

                k = mario.heading
                if mario.heading == 0:#앞 뒤 보는 방향에 따라 이것도 달라지게 하자
                    k = 1#0일때 맞는 것은 불가능 하므로
                        
                if (k == 1 and mario.speed < 0) or (k == -1 and mario.speed > 0):
                    self.speed = -mario.speed
                else:
                    self.speed = mario.speed
                    

                    self.rect.x += 10 * k
                
                if mario.speed == 0:
                    self.speed = 2 * k
                
            else:
                pygame.mixer.Sound("Sounds/smw_kick.wav").play()
                self.state = "Roll"
                self.ShellInsideTimer = 0
                
                if mario.heading == 0:
                    self.heading = mario.oldheading * -1
                    self.rect.centerx = mario.rect.centerx + 24 * mario.oldheading
                    
                else:
                    self.heading = mario.heading
                    
                    
                self.AvailableTimer = 0

    
    def Physics(self,Ground,mario,Slope):
        global OldAngle
        if self.ThrownInit:
            self.ThrownInit = False
            self.speed = calc_proj_vx(self.rect.center,(mario.rect.centerx + 35 * mario.speed, mario.rect.centery),10,Globals.GRAVITY)
            self.yv = -10
        #print(self.speed)
        self.movement = [0,0]
        key = pygame.key.get_pressed()

        if self.alreadyHit:
            self.state = "Dead"
            self.MoveTimer = -1
            if not self.Flipped:
                self.Flip = True
            self.FlippedAngle = 0
            self.speed = -self.hitFrom * 1
            self.yv = -15
            

            self.ShellInsideTimer = 0
            pygame.mixer.Sound("Sounds/smw_kick.wav").play()

        for i in KoopaTroopas:
            if i.eaten or self.eaten: continue
            if i.rect.colliderect(self.rect) and self != i and i.state != "Gone" and self.state != "Gone" and not (self.winged):# and self.state in ["BuzzyBeetle","Spiny"]) :
                if self.holded:#마리오가 들고 있는 껍데기랑 다른 껍데기랑 충돌
                    i.state = "Gone"
                    self.state = "Gone"
                    self.holded = False
                    mario.holding = False
                    self.speed = -4 * mario.oldheading
                    i.speed = 4 * mario.oldheading
                    i.rect.y = self.rect.y
                    self.yv = -10
                    i.yv = -10
                    pygame.mixer.Sound("Sounds/smw_kick.wav").play()
                    return#이게 없으면 한 번에 3개씩 사라지기도 함

                else:
                    if self.state != "Roll":#평범하게 걷고 있는 애들끼리 충돌
##                        if self.heading == 1 and i.heading == 1:
##                            pass#가능한가?
##                        elif self.heading == 1 and i.heading == -1:
##                            self.rect.right = i.rect.left; i.rect.left = self.rect.right
##                        elif self.heading == -1 and i.heading == 1:
##                            self.rect.left = i.rect.right; i.rect.right = self.rect.left
    
                        if i.state != "Roll":
                            self.heading *= - 1
                            i.heading *= -1
                        if self.state == "Normal": self.rect.x += 4 * self.heading
                        if i.state == "Normal": i.rect.x += 4 * i.heading
                        

                    else:#굴러가는 껍데기랑 다른 껍데기 충돌 여부
                        if i.state == "Roll":#둘 다 굴러가는 껍데기라며
                            self.speed = -self.heading * 4
                            i.speed = self.heading * 4
                            i.rect.y = self.rect.y
                            self.yv = -10
                            i.yv = -10
                            
                            self.state = "Gone"
                            pygame.mixer.Sound("Sounds/smw_kick.wav").play()
                        else:#하나만 굴러가는 껍데기라면
                            self.combo += 1
                            if self.combo > 8:
                                self.combo = 8
                                mario.life += 1
                            pygame.mixer.Sound("Sounds/combo"+str(self.combo)+".WAV").play()
                            
                        i.state = "Gone"

        if not self.Dead and not self.eaten:
            self.MoveTimer += 1
            self.NotHoldingRightAfterJumpingTimer += 1
            if self.holded:
                mario.Holded_Object_Loop(self)
                    
            if self.state == "Normal":
                if self.winged:
                    if self.type == "Koopa":
                        self.speed = self.heading * 2
                        if self.collision_types['bottom']:
                            self.yv = -15#random.randint(10,25)
                    elif self.type == "Spiny":
                        self.speed = self.heading * 2#(Globals.GlobalTimer / 100)                   
                elif not self.Thrown:
                    self.speed = self.heading * 2
                if self.type == "Spiny" and (self.winged or self.Thrown):
                    if self.winged:
                        if self.MoveTimer % 64 == 0:
                            for i in range(4):
                                SpinyNeedle(self.rect.center,2 * i + self.Alternation)
                            self.Alternation = not self.Alternation

                    if self.MoveTimer % 12 == 0:
                        self.image = AllImages[self.type + "Ball1.png"]
                    elif self.MoveTimer % 12 == 6:
                        self.image = AllImages[self.type + "Ball2.png"]
                else:
                    if self.MoveTimer % 12 == 0:
                        self.image = AllImages[self.type + "1.png"]
                    elif self.MoveTimer % 12 == 6:
                        self.image = AllImages[self.type + "2.png"]
                    
            elif self.state == "Dead":
                self.combo = 1
                self.rect.height = 32
                if self.ShellEmpty:
                    self.image = AllImages[self.type + " Shell1.png"]
                else:
                    if self.type == "Koopa":
                        if self.MoveTimer % 60 == 0:
                            self.image = self.image = AllImages[self.type + "_ShellInside1.png"]
                        elif self.MoveTimer % 60 == 50:
                            self.image = self.image = AllImages[self.type + "_ShellInside2.png"]
                    else:
                        self.image = AllImages[self.type + " Shell1.png"]

                    
                    if self.ShellInsideTimer > 500:
                        self.state = "Normal"
                        self.Flipped = False
                        self.Shaking = False
                        self.FlippedAngle = 0
                        self.ShellInsideTimer = 0

                        if self.type == "Koopa": self.rect.height = 52
                        else: self.rect.height = 32
                        if self.holded:
                            self.holded = False
                            mario.holding = False

                    elif self.ShellInsideTimer == 440:
                        OldAngle = self.FlippedAngle
                        
                    elif self.ShellInsideTimer > 440:
                        self.Shaking = True
                        if self.ShellInsideTimer % 4 == 0:
                            self.FlippedAngle = OldAngle - 8
                        elif self.ShellInsideTimer % 4 == 2:
                            self.FlippedAngle = OldAngle + 8
                    self.ShellInsideTimer += 1


            elif self.state == "Roll":
                self.Shaking = False
                if self.Flip:
                    self.FlippedAngle = 0
                    self.Flipped = True
                    self.Flip = False#뒤집자마자 차면 기울어짐

                self.ShellInsideTimer = 0
                self.speed = 10 * self.heading
                self.image = self.image = AllImages[self.type + " Shell"+str(((self.MoveTimer // 4) % 3) + 1) + ".png"]
        if self.state == "Gone":
            self.winged = False
            self.FlippedAngle = 0
            self.Flipped = True
            self.Shaking = False
            self.image = self.image = AllImages[self.type + " Shell1.png"]
            self.Dead = True
            if self.rect.top - mario.scroll[1] >= Globals.SH:
                KoopaTroopas.remove(self)


        if mario.cape and self.rect.colliderect(cape.cape.rect) and mario.TurnAround and not self.holded and not self.Flip and not self.rect.colliderect(mario.rect) and self.state != "Gone":
            self.state = "Dead"
            self.MoveTimer = -1
            if not self.Flipped:
                self.Flip = True
            self.FlippedAngle = 0
            self.speed = 0
            self.yv = -20
            self.ShellInsideTimer = 0
            pygame.mixer.Sound("Sounds/smw_kick.wav").play()

        if self.Flip:
            if self.FlippedAngle < 180:
                self.FlippedAngle += 20
            else:
                self.FlippedAngle = 0
                self.Flip = False
                self.Flipped = True
        self.AvailableTimer += 1

        self.solid = True
        if self.rect.colliderect(mario.rect) and self.state != "Gone":
            self.solid = False


        if mario.RidingYoshi:
            if mario.attack:
                #닿았을 때 이미 eaten으로 설정하고 visual copy만 전달해줌?
                if self.eaten:
                    self.rect.center = mario.Yoshi.tongue.rect.center
                elif mario.Yoshi.tongue.eatenObject == None:
                    if mario.Yoshi.tongue.rect.colliderect(self.rect):

                        #registerHit라고 함수 만들자 -> 이 모든걸 간편히!
                        self.eaten = True
                        mario.Yoshi.tongue.waitForTakeBack = True
                        mario.Yoshi.tongue.stretch = False
                        mario.Yoshi.tongue.waitTimer = 8
                        
                        mario.Yoshi.tongue.eatenObject = self
                        #Enemies.remove(self)
            else:
                if self.eaten:
                    mario.Yoshi.holding = True
                    #mario.Yoshi.tongue.eatenObject = self
                    KoopaTroopas.remove(self)
                
                

        if self.holded:
            self.yv = 0                

        else:
            self.lastPos = copy.deepcopy(self.rect.topleft)
            self.movement = [self.speed, self.yv]
            if not self.winged or (self.winged and self.type == "Koopa") and not self.eaten:
                self.yv += Globals.GRAVITY
                if self.yv > 15 and not self.Thrown:
                    self.yv = 15
                self.rect, self.collision_types = self.move(self.rect,self.movement,Ground,Slope)
            else:
                if self.marioOn:
                    self.yv = max(self.yv - 0.15, -2)
                else:
                    self.yv = 0
                    
                self.rect.x += self.speed
                self.rect.y += self.yv#self.y + 40 * math.sin(Globals.GlobalTimer / 10)#self.yv
                
        if self.collision_types['left'] or self.collision_types['right']:
            self.heading *= -1

        if self.state != "Gone":
            if self.collision_types['bottom']:
                if self.Thrown: self.Thrown = False
                self.yv = 0
                if self.state == "Dead": self.speed *= 0.7

            if self.collision_types['top']:
                self.yv = 0

        if abs(self.speed) < 1 or self.holded:
            self.speed = 0

        for i in mario.Fireballs:
            if self.rect.colliderect(i.rect) and not i.blocked:
                if self.type == "BuzzyBeetle":
                    if mario.MegamanMode:
                        i.blocked = True
                        pygame.mixer.Sound("Sounds/11 - Dink.wav").play()
                    else: 
                        Effects.Effect(self.rect.centerx,self.rect.centery,2,particles = False)
                        mario.Fireballs.remove(i)
                elif self.state != "Gone":
                    self.state = "Gone"
                    
                    pygame.mixer.Sound("Sounds/smw_kick.wav").play()
                    mario.Fireballs.remove(i)

                

        if self.NotKickingRightAfterThrowingTimer > 0:
            self.NotKickingRightAfterThrowingTimer -= 1
        
        if self.type == "Koopa":
            self.ray(Ground)

        
        if self.IsInsideMario:#방금 마리오가 밟았고 아직 쉘에서 벗어나지 않은경우
            if not mario.rect.colliderect(self.rect):
                self.IsInsideMario = False

        prev = self.marioOn
    
            
        self.marioOn = False
        if self.winged and self.type == "BuzzyBeetle":
            self.speed = 1 * self.heading
            newPos = copy.deepcopy(self.rect.topleft)
            #self.rect.x = self.lastPos[0]
            self.rect.y = self.lastPos[1] - 1
                
            if self.rect.colliderect(mario.rect) and self.state != "Gone":# and mario.yv >= 0 and mario.rect.bottom < self.rect.centery:#마리오와 충돌했을 때 모든 것을 처리
                if self.rect in mario.hitlistsV:#처음 밟음
                    if not prev:
                        self.yv = 4
                    self.marioOn = True
                    self.speed = 1 * self.heading
                    
                mario.PlatformSpd = [newPos[0] - self.lastPos[0], newPos[1] - self.lastPos[1]]
                #print(self.solid,mario.PlatformSpd)
            self.rect.topleft = newPos
        
        if self.rect.colliderect(mario.rect) and self.state != "Gone":#마리오와 충돌했을 때 모든 것을 처리
##            if self.winged and self.type == "BuzzyBeetle":
##                print("a")#mario.Death()
            if mario.starman:#마리오가 무적이라면
                if self.holded:
                    self.holded = False
                    mario.holding = False
                mario.combo += 1
                if mario.combo > 8:
                    mario.combo = 8
                    mario.life += 1
                pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()
                self.state = "Gone"

            elif mario.SlippingDown:#마리오가 경사로에서 미끄러져 내려오고 있다면
                if (self.state == "Normal" or self.state == "Dead"):
                    self.state = "Gone"
                    if mario.combo > 8:
                        mario.combo = 8
                        mario.life += 1
                    pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()
                    mario.combo += 1

            elif not self.holded and not (self.winged and self.type in ["BuzzyBeetle","Spiny"]):#평범하게 밟거나 부딫혔을 때
                if (mario.rect.bottom < self.rect.bottom and (mario.movement[1] > 0 or self.yv)): #위에서 내리 찍었는가? #x좌표의 범위도 추가:
                    mario.jumpable = True
                    mario.jumping = False
                    if mario.SpinJump:#스핀 점프
                        if self.type == "Spiny" and self.state == "Normal":
                            self.IsInsideMario = True
                            mario.yv = -12
                            Effects.Effect(mario.rect.centerx,mario.rect.bottom,1)
                            pygame.mixer.Sound("Sounds/smw_stomp_no_damage.wav").play()
                            
                            #mario.rect.bottom = self.rect.top#이걸 다른걸로 대채할 방법은 없을까? -> 벽에 끼일 우려가 있음

                        else: #그냥 거북이거나 하잉바일때 또는 구르는 상태일 때(가시돌이도 포함)
                            pygame.mixer.Sound("Sounds/stomp2.wav").play()
                            mario.yv=-3
                            KoopaTroopas.remove(self)
                            Effects.Effect(mario.rect.centerx,mario.rect.bottom,2,particles = True,TI = 2)
                            return #아래 명령은 실행 되면 안됨 -> 진짜?
                        
                    elif not self.IsInsideMario:#그냥 점프
                        if self.winged:
                            self.yv = 0
                            self.winged = False
                            pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()
                            mario.yv = -12
                            mario.combo += 1
                            self.IsInsideMario = True
                            if mario.combo > 8:
                                mario.life += 1
                                mario.combo = 8

                        elif self.state == "Normal" or self.state == "Roll":
                            if self.type != "Spiny" or (self.type == "Spiny" and self.state == "Roll"):
                                self.state = "Dead"
                                self.speed = 0
                                self.CanStepOnIt = True
                                self.IsInsideMario = True
                                mario.yv = -12
                                
                                if not self.ShellEmpty and self.type == "Koopa":#거북이 알맹이가 밖으로 나옴
                                    self.ShellEmpty = True
                                    Koopa(self.rect.x, self.rect.y, True,  2 * (mario.rect.centerx <= self.rect.centerx) - 1)#이미지 자체가 반대로 뒤집혀 있기 때문에 -1 곱해줌(self.heading은...?)

                                #mario.rect.y -= 10#???
                                
                                self.NotHoldingRightAfterJumpingTimer = 0
                                #mario.rect.bottom = self.rect.top
                                pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()
                                mario.combo += 1
                                if mario.combo > 8:
                                    mario.life += 1
                                    mario.combo = 8
                                    
                                old = self.rect.bottom
                                self.rect.height = 32
                                self.rect.bottom = old
                                
                            if self.type == "Spiny" and self.state == "Normal":
                                mario.Death()

                                

                else:
                    if (self.state == "Normal" or self.state == "Roll") and self.AvailableTimer > 8 and not self.IsInsideMario: #던지고 조금 있다가 맞았는가 & 밟은게 아닌 경우
                        mario.Death()
                        #print(mario.rect.bottom,self.rect.bottom,mario.movement[1])

                if self.state == "Dead":
                    if mario.rect.top < self.rect.bottom < mario.rect.top + 20 and self.type == "Spiny" and self.yv > 0:#가시에다가 머리박은 경우
                        mario.Death()
                        
                    if mario.running:
                        if not mario.holding and self.NotHoldingRightAfterJumpingTimer > 10 and not mario.RidingYoshi:
                            mario.holding = True
                            self.holded = True
                            return
                    
                    if not self.IsInsideMario and self.NotKickingRightAfterThrowingTimer == 0:#위에 구문이 실행되면 이건 실행되면 안됨(2번 차짐)      
                        if mario.rect.centerx <= self.rect.centerx:#마리오가 껍데기를 어느 방향에서 찻는지
                            self.heading = 1
                        else:
                            self.heading = -1
                            
                        self.state = "Roll"
                        self.IsInsideMario = True
                        self.AvailableTimer = 0
                        
                        pygame.mixer.Sound("Sounds/smw_kick.wav").play()


    
    def collision_test(self,rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        
        return hit_list

    def remove(self):
        KoopaTroopas.remove(self)
        
    def move(self,rect,movement,tiles,slopes):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}                
        rect.x += movement[0]
        if not self.Dead:
            #==== 중요!! ====#
            #절대 아래 스크립트의 위치를 바꾸지 마시오(바꾸면 쉘이 제대로 안 굴러가거나 슬로프를 이상하게 올라가거나, 바닥에 붙지 않음)
            
            #== rect를 바닥에 붙이게 하는 부분(없으면 내리막에서 통통 튀기면서 내려감) ==#
            #이 부분은 무조건 slope를 고정하는 스크립트 전에 있어야됨
            #안그러면 문제가 생김 -> 슬로프를 이상하게 올라가거나 아예 바닥에 붙지 않는다
            if self.collision_types['bottom']:
                oldpos = copy.deepcopy(rect.y)
                check = False
                for i in range(16):
                    if Globals.slope_collision_test(rect) != None:
                        check = True
                        break
                    rect.y += 1

                if not check: rect.y = oldpos

            #== rect를 슬로프에 고정시키는 부분 ==#
            #이 부분이 아래 rect들과의 horizontal collision을 처리하기 전에 이루어 져야 슬로프를 올라가면서 collision_types의 left나 right가 활성화 안됨
            #이 부분의 위치가 잘못될 경우 쉘이 구를 때 슬로프 중간에서 갑자기 방향을 틈
            #  / 
            # /ㅁ <- 요 rect와 collision이 일어나기 때문
            
            self.Onslope = False
            r = Globals.slope_collision_test(rect)
            if r != None:
                rect.bottom = r
                collision_types['bottom'] = True
                self.Onslope = True

            hit_list = Globals.collision_test(rect,tiles)
            for tile in hit_list:
                if movement[0] > 0:
                    rect.right = tile.left
                    collision_types['right'] = True
                elif movement[0] < 0:
                    rect.left = tile.right
                    collision_types['left'] = True
                for j in Block.Blocks:
                    
                    if tile == j.rect and self.state == "Roll":
                        try: j.ActivatedByShell = True
                        except:pass
                                
        rect.y += math.ceil(movement[1])
        if not self.Dead:
            hit_list = Globals.collision_test(rect,tiles)
            self.alreadyHit = False
            for tile in hit_list:
                if movement[1] > 0:
                    rect.bottom = tile.top
                    collision_types['bottom'] = True
                elif movement[1] < 0:
                    rect.top = tile.bottom
                    collision_types['top'] = True
        
                
                for j in Block.Blocks:
                    if tile == j.rect:
                        if not self.alreadyHit and movement[1] > 0:
                            a = False
                            try: a = j.hit
                            except: pass
                            if a:
                                self.hitFrom = j.hitFrom
                                self.alreadyHit = True
                                break

                        if movement[1] < 0 and self.state == "Dead":
                            try: j.ActivatedByShell= True
                            except:pass


        return rect, collision_types

RMemory = []
def loop(screen,Ground,mario,Slope):
    for i in RMemory:
        #x좌표만 체크
        if -i.rect.width < i.x - mario.scroll[0] < SW:#Globals.IsRectOnScreen(pygame.Rect((i.x,i.y),i.rect.size),mario):#mario.rangeX[0] * 32 < i.x < mario.scroll[0] or mario.scroll[0] + 640 < i.x < mario.rangeX[1] * 32:# and  mario.scroll[1] + 480 > i.rect.bottom > mario.rangeY[1] * 32:
            if i.marioAway:
                i.__init__(i.x,i.y,i.type,OnlyShell = i.OnlyShell, winged = i.winged,heading = i.heading)

##                i.rect.topleft = (i.x,i.y)
##                KoopaTroopas.append(i)
                RMemory.remove(i)
        else:
            i.marioAway = True

    for i in Needles:
        #pygame.draw.rect(screen,(255,0,0),(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1],i.rect.width,i.rect.height))

        if not mario.pause:
            i.loop(mario)
        img = NeedleImages[i.direction]
        screen.blit(img,(i.rect.centerx - img.get_width() / 2 - mario.scroll[0],i.rect.centery - img.get_height() / 2 - mario.scroll[1]))

    for i in KoopaTroopas:

        if not (i.winged and i.type == "BuzzyBeetle"):#이게 없으면 모양이 살짝 이상해짐
            if not mario.pause:
                i.Physics(Ground,mario,Slope)
            
        if i.Flip or i.Shaking:
            img = pygame.transform.rotate(i.image,i.FlippedAngle)
        else:
            img = i.image

            
        if i.heading==-1:screen.blit(pygame.transform.flip(img,False,i.Flipped),(i.rect.x-mario.scroll[0],i.rect.bottom - i.image.get_height() -mario.scroll[1]))
        else:screen.blit(pygame.transform.flip(img,True,i.Flipped),(i.rect.x-mario.scroll[0],i.rect.bottom - i.image.get_height() -mario.scroll[1]))

        if i.winged:
            screen.blit(pygame.transform.flip(WingImages[(Globals.GlobalTimer // 8) %2],i.heading == 1,False),(i.rect.x - 20 * i.heading - mario.scroll[0],i.rect.y - 5 - mario.scroll[1]))

        #pygame.draw.rect(screen,(255,0,0),(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1],i.rect.width,i.rect.height))

        if i.rect.right < mario.rangeX[0] * 32 or  i.rect.left > mario.rangeX[1] * 32 or  i.rect.top > mario.rangeY[1] * 32:#i.rect.top > mario.scroll[1] + 480: #
            if i.state != "Gone" and not i.holded:
                #i.__init__(i.x,i.y,i.type,Tlist = RMemory,OnlyShell = i.OnlyShell, winged = i.winged,heading = i.heading)
                i.marioAway = False
                RMemory.append(i)
                KoopaTroopas.remove(i)

        if not mario.pause:
            if (i.winged and i.type == "BuzzyBeetle"):#날개달린 하잉바만 해당됨(언젠가 이렇게 안해도 되게 고치자)
                #아예 이게 아래 있으면 쉘을 들고 다닐때 모양이 이상해짐
                i.Physics(Ground,mario,Slope)


    #print(len(RMemory),len(KoopaToopas))
    for i in Koopas:
        #if (mario.rangeX[0]) * 32 <= i.rect.centerx <= (mario.rangeX[1]) * 32:
        if i.heading==1:screen.blit(i.image,(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
        else:screen.blit(pygame.transform.flip(i.image,True,i.Dead),(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
        if not mario.pause:
            i.Physics(Ground,mario,Slope)
        #pygame.draw.rect(screen,(255,0,0),(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1],i.rect.width,i.rect.height))

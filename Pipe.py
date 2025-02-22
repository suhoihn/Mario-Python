#pipe
import pygame
import ROM,Globals
pipes = []
DelTarget = None
class pipe:
    def __init__(self,x,y,idx,direction="UP",length = 2,LvTrans = False,TargetLevelIdx = 0,Enterable = True):
        self.x=x
        self.rootX=x
        self.idx = idx
        self.LvTrans = LvTrans
        self.y=y
        self.target=None
        self.Enterable = Enterable#나올수만 있음
        self.direction=direction
        self.length = length
        #self.image = pygame.transform.scale(pygame.image.load("Sprites/Blocks/pipe.png"),(64,64)).convert_alpha()
        self.segment_image = pygame.transform.scale(pygame.image.load("Sprites/Blocks/pipe2.png"),(64,32)).convert_alpha()#이거 64,64아닌것 같은데...?
        self.TargetLevelIdx = TargetLevelIdx

        t = pygame.transform.scale(pygame.image.load("Sprites/Blocks/pipe.png"),(64,64)).convert_alpha()
        self.CompleteImg = pygame.Surface((64,32 * length))#파이프가 []==== 모양인걸 기준으로 두고 direction에 따라서 돌리는걸로
        self.CompleteImg.fill((255,0,0))
        self.CompleteImg.blit(t,(0,0))#파이프 맨 앞 꼬다리
        for i in range(length - 2):
            self.CompleteImg.blit(self.segment_image,(0,64 + 32 * i))

        self.dv = (0,0)#Direction Vector
        if self.direction == "DOWN":
            self.key = pygame.K_DOWN
            self.dv = (0,1)
            self.image = self.CompleteImg
        elif self.direction == "UP":
            self.image = pygame.transform.flip(self.CompleteImg,False,True)
            self.dv = (0,-1)
            self.key=pygame.K_z
            
        elif self.direction=="LEFT":
            self.image = pygame.transform.flip(pygame.transform.rotate(self.CompleteImg,-90),False,False)
            self.dv = (-1,0)
            self.key=pygame.K_LEFT
            
        elif self.direction=="RIGHT":
            self.image = pygame.transform.flip(pygame.transform.rotate(self.CompleteImg,90),False,True)
            self.dv = (1,0)
            self.key=pygame.K_RIGHT

        
        self.image = self.image.convert_alpha()
        self.image.set_colorkey((255,0,0))
        self.movement = [0.0]
        self.rect = self.image.get_rect()#pygame.Rect(self.x,self.y,self.width,self.height)

                
        if self.direction == "UP" or self.direction == "DOWN":
            self.PipeDirection = "vertical"
            #self.rect.height = 64 + 32 * (self.length - 2)
            if self.direction == "UP": self.rect.topleft = (x,y - (length - 2) * 32)
            if self.direction == "DOWN": self.rect.topleft = (x,y)

                
        elif self.direction == "LEFT" or self.direction == "RIGHT":
            self.PipeDirection = "horizontal"
            #self.rect.width = 64 + 32 * (self.length - 2)

            
            self.rect.topleft = (x,y)
        self.images = []
        for i in range(length - 2):
            R = self.segment_image.get_rect()
            if self.dv[0] == 0:
                R.left = self.rect.left
                if self.dv[1] == 1:
                    R.top = self.rect.top + 64 + i * R.height * self.dv[1]
                elif self.dv[1] == -1:
                    R.bottom = self.rect.bottom - 64 + i * R.height * self.dv[1]
                    
            elif self.dv[1] == 0:
                R.top = self.rect.top
                if self.dv[0] == 1:
                    R.left = self.rect.left + 64 + i * R.width * self.dv[0]
                elif self.dv[0] == -1:
                    R.right = self.rect.right - 64 + i * R.width * self.dv[0]
            self.images.append(R)
        self.timer = 0
        self.Descend = False
        self.Rise = False
        pipes.append(self)

    def loop(self,mario):
        global pipes,DelTarget
        self.Descend = False
        self.Rise = True
                
        self.timer = 0

        
    def remove(self):
        pipes.remove(self)

    def PipeReset(self,mario):
        global DelTarget
        mario.calm = False
        self.Rise = False
        self.target = None
        mario.cannotmove = False
        mario.blurness = 1
        if DelTarget != None:
            pipes.remove(DelTarget)
            DelTarget = None
            mario.AutoScroll = Globals.AutoScroll

    def Physics(self,mario):
        global DelTarget,pipes
        key = pygame.key.get_pressed()
        if key[self.key] and not self.Descend and not self.Rise and self.idx != -1 and self.Enterable:
            if self.rect in mario.hitlistsV and self.rect.centerx - 10 < mario.rect.centerx < self.rect.centerx + 10:#self.rect.left < mario.rect.left and mario.rect.right < self.rect.right:
                mario.PipeEnterType = self.PipeDirection
                if self.direction=="DOWN":
                    if mario.rect.bottom == self.rect.y:
                        mario.heading *= mario.RidingYoshi
                        self.Descend=True
                        pygame.mixer.Sound("Sounds/smw_powerdown.wav").play()

                        
                elif self.direction=="UP":
                    if mario.rect.top == self.rect.bottom:
                        mario.heading *= mario.RidingYoshi
                        self.Descend = True
                        pygame.mixer.Sound("Sounds/smw_powerdown.wav").play()
                        
            elif self.rect in mario.hitlistsH:
                mario.PipeEnterType = self.PipeDirection
                if self.direction=="LEFT" and mario.collision_types['bottom'] and abs(mario.rect.bottom - self.rect.bottom) < 3 :
                    if mario.rect.left == self.rect.right:
                        self.Descend = True
                        pygame.mixer.Sound("Sounds/smw_powerdown.wav").play()
                        mario.heading = -1
                        
                elif self.direction=="RIGHT" and mario.collision_types['bottom'] and abs(mario.rect.bottom - self.rect.bottom) < 3:
                    if mario.rect.right == self.rect.left:
                        self.Descend = True
                        pygame.mixer.Sound("Sounds/smw_powerdown.wav").play()
                        mario.heading = 1
                        #holding 하는 경우는 반대로 진입
                
        if self.Descend:
            self.timer+=1
            mario.calm=True
            mario.SpinJump = False
            mario.sitting = False
            if self.direction=="DOWN":
               # mario.heading = 0
                if mario.rect.y<self.rect.y:
                    mario.rect.y+=2
                else:
                    self.loop(mario)
            elif self.direction=="UP":
                #mario.heading = 0
                if mario.rect.bottom>self.rect.bottom:
                    mario.rect.y-=2
                else:
                    self.loop(mario)
            elif self.direction=="LEFT":
                if mario.rect.right>self.rect.right:
                    mario.rect.x-=1
                else:
                    self.loop(mario)
                
            elif self.direction=="RIGHT":
                if mario.rect.left<self.rect.left:
                    mario.rect.x+=1
                else:
                    self.loop(mario)
                    
                    
        if self.Rise:
            if self.timer < 30:
                mario.blurness += 0.4
            elif self.timer == 30:
                mario.BlackScreen = True
                if self.LvTrans:
                    #만약 2개 이상 레벨을 한 맵에 추가하고 싶다면 각 파이프에 일일이 지정해야됨
                    if Globals.LevelCount > 2: Globals.MarioAt = self.TargetLevelIdx
                    else:
                        Globals.MarioAt = (Globals.MarioAt + 1) % 2
                        
                    
                    ROM.initialize()
                    ROM.LoadLevel(Globals.Lvidx,MarioAt = Globals.MarioAt)
                    mario.AutoScroll = False
                    List = Globals.CurrentPipes
                    DelTarget = self
                    List.append(self)#루프는 돌아가야되니까...근데 나중에 제거해야됨
                    #print(len(pipes))
                    pipes = List
                    mario.ScrollLimit = Globals.ScrollLimit
                    if not mario.starman:
                        pygame.mixer.music.fadeout(500)
                        pygame.mixer.music.load(Globals.BGM)
                        pygame.mixer.music.play(-1)

                    try:
                        mario.Holded_Obj.reload()
                    except Exception as e:
                        print(e)
                    


                else:
                    List = pipes
                for i in List:
                    if self != i and self.idx == i.idx:
                        self.target = i
                        break
                if self.target.direction=="DOWN":
                    mario.rect.centerx,mario.rect.top=self.target.rect.centerx,self.target.rect.top

                elif self.target.direction=="UP":
                    mario.rect.centerx,mario.rect.bottom=self.target.rect.centerx,self.target.rect.bottom
                    
                elif self.target.direction=="LEFT":
                    mario.rect.right,mario.rect.bottom=self.target.rect.right,self.target.rect.bottom
                    
                elif self.target.direction=="RIGHT":
                    mario.rect.left,mario.rect.bottom=self.target.rect.left,self.target.rect.bottom


            elif self.timer > 30 + 50:
                mario.BlackScreen = False
                if self.target.direction=="DOWN":#마리오 발바닥 = 파이프 발바닥까지 반복?
                    mario.heading *= mario.RidingYoshi#mario.heading = mario.heading * mario.RidingYoshi
                    mario.PipeEnterType = "vertical"
                    if mario.rect.bottom > self.target.rect.y:
                        mario.rect.y -= 2 #올라가는 거는 빨라야함 (마리오가 위로 길쭉하니까)
                        mario.blurness -= 0.4
                    else:
                        self.PipeReset(mario)
                elif self.target.direction=="UP":
                    mario.heading *= mario.RidingYoshi
                    mario.PipeEnterType = "vertical"
                    if mario.rect.y < self.target.rect.bottom:
                        mario.rect.y += 2
                        mario.blurness -= 0.4
                    else:
                        self.PipeReset(mario)
                elif self.target.direction=="LEFT":
                    mario.heading = 1
                    mario.PipeEnterType = "horizontal"
                    if mario.rect.left < self.target.rect.right:
                        mario.rect.x += 1
                        mario.blurness -= 0.4
                    else:
                        self.PipeReset(mario)
                    
                elif self.target.direction=="RIGHT":
                    mario.heading = -1
                    mario.PipeEnterType = "horizontal"
                    if mario.rect.right > self.target.rect.left:
                        mario.rect.x -= 1
                        mario.blurness -= 0.4
                    else:
                        self.PipeReset(mario)
            
        
            self.timer += 1



#이동 = (0,1) 이런식으로 해도 될듯
def loop(screen,mario):
    for i in Globals.CurrentPipes:
        i.Physics(mario)
##        for j in i.images:
##            if -j.width < j.x - mario.scroll[0] < Globals.SW and -j.height < j.y - mario.scroll[1] < Globals.SH:
##                screen.blit(i.segment_image,(j.x - mario.scroll[0],j.y - mario.scroll[1]))

        if -i.rect.width < i.rect.x - mario.scroll[0] < Globals.SW and -i.rect.height < i.rect.y - mario.scroll[1] < Globals.SH and i != DelTarget:#DelTarget은 마리오가 파이프를 빠져나온 후 없어지므로 그 전까지는 그리지 않는걸로
            screen.blit(i.image,(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
        
   

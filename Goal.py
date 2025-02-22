import pygame,Globals,os
Goals = [] #골은 하나만 있으면 됨 -> 재미로 fake도 만듦
CPs = []
class Goal:
    class Flag:
        def __init__(self,Pole):
            self.x = Pole.x+20
            self.y = Pole.y
            self.Pole = Pole
            self.image = pygame.transform.scale(pygame.image.load("Sprites/Blocks/flag.png").convert_alpha(),(50,16))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.yv = 1
        def Physics(self,mario):
            self.y+=self.yv
            if self.y<self.Pole.y or self.y+self.rect.height>self.Pole.y+self.Pole.rect.height:
                self.yv*=-1
            self.rect=pygame.Rect(self.x,self.y,self.rect.width,self.rect.height)
            if mario.rect.colliderect(self.rect):
                mario.gameclear(self.Pole.IsTrueGoal)
                self.Pole.Done = True
    def __init__(self,x,y,IsTrueGoal):
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Blocks/pole.png").convert_alpha(),(96,290))
        self.rect = self.image.get_rect()
        self.Done=False
        self.IsTrueGoal = IsTrueGoal
        self.rect.bottom=y+64
        self.x=x
        self.y=self.rect.y
        self.flag=self.Flag(self)
        Goals.append(self)

idx = 0#이러지 말고 따로 지정 할 수 있게...
#0부터 시작, RegisteredCPidx = -1인 경우 체크포인트가 안 찍혔다는 뜻
class CheckPoint:
    def __init__(self,x,y):
        global idx
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Checkpoint/CP1.png").convert_alpha(),(64,128))
        self.x, self.y = x, y - 128 + 32 + 10
        self.tape = pygame.transform.scale(pygame.image.load("Sprites/Checkpoint/CP_tape.png").convert_alpha(),(32,6))
        self.touched = False
        self.idx = idx
        idx += 1
        if Globals.RegisteredCPidx == self.idx and Globals.StartLvlIdx == Globals.MarioAt:#이미 찍은 체크포인트가 죽고 살아났을때 이미 찍혀있도록 만듦.
            #만약 MainLevel(MarioAt = 0)에서 체크포인트를 찍었을 때(RegisteredCPidx = 0, StartLvlIdx = 0) SubLevel(MarioAt = 1)에 있는 체크포인트(RegisteredCPidx = 0)는 StartLvlIdx != MarioAt이므로 안 찍혀 있게 됨
            #"Globals.StartLvlIdx == Globals.MarioAt" 부분이 없을 경우 SubLevel에서의 체크포인트가 이미 찍혀있음
            self.touched = True
        self.images = []
        for i in os.listdir("Sprites/Checkpoint"):
            self.images.append(pygame.transform.scale(pygame.image.load("Sprites/Checkpoint/" + i).convert_alpha(),(64,128)))

        CPs.append(self)

    def Physics(self,mario):
        if not self.touched:
            if mario.rect.colliderect(pygame.Rect(self.x + 16,self.y + 40,32,6)) and not self.touched:
                self.touched = True
                mario.state = "big"
                Globals.RegisteredCPidx = self.idx
                Globals.StartLvlIdx = Globals.MarioAt
                Globals.StartPoint = (self.x + 16, self.y + 128 - 10)
                pygame.mixer.Sound("Sounds/smw_midway_gate.wav").play()
        self.image = self.images[(Globals.GlobalTimer // 8) % 4]

def loop(screen,mario):
    for i in Goals:
        screen.blit(i.image,(i.x - mario.scroll[0], i.y - mario.scroll[1]))

        if not i.Done:
            screen.blit(i.flag.image,(i.flag.x - mario.scroll[0], i.flag.y - mario.scroll[1]))
            if not mario.pause:
                i.flag.Physics(mario)

    for i in CPs:
        screen.blit(i.image,(i.x - mario.scroll[0], i.y - mario.scroll[1]))
        if not i.touched:
            screen.blit(i.tape,(i.x + 16 - mario.scroll[0], i.y + 40 - mario.scroll[1]))

        if not mario.pause:
            i.Physics(mario)

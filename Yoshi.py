#Yoshi
import pygame,Enemy,Cannon,Things,Spiny,copy,Pipe,Globals
Yoshis = []
#요시가 떨어지고 남은 잔해를 먹는 거 고치기(예를 들어 밟은 대포, 죽은 거북이 등등)
#요시가 혀를 내밀때 말고도 다시 들어오게할 때도 먹을 수 있어야 함
class Yoshi:
    class Tongue:
        def __init__(self,yoshi):
            self.add = 0
            self.x = 0 #혀의 x좌표
            self.y = 0
            self.yoshi = yoshi
            self.stretch = False
            self.takeback = False
            self.waitForTakeBack = False
            self.waitTimer = 0
            self.image=pygame.image.load("Sprites/Yoshi/Yoshi_tongue.png")
            self.eatenObject = None
            self.containment = None

            self.width = 16#self.image.get_width()
            self.height = 16#self.image.get_height()

            self.rect = self.image.get_rect()

        def Physics(self,mario,Grounds):
            if self.yoshi.MarioRiding:
                print(self.stretch, self.takeback, self.waitForTakeBack, self.eatenObject)
                
            self.x = self.yoshi.rect.centerx + self.yoshi.heading * self.yoshi.rect.width / 2 + self.add - 5#  + mario.speed
            self.y = self.yoshi.rect.bottom - 20 -20 * (not mario.collision_types['bottom'])#rect.bottom을 쓰는 이유는 앉을때도 위치가 변하지 않으므로
            self.rect.x = self.x
            self.rect.centery = self.y
            if self.stretch:
                if self.add * self.yoshi.heading < 32 * 2 + 16: #self.yoshi.heading = 1 일 때  -> self.add < 100
                                                      #self.yoshi.heading == -1일 때 -> self.add * -1 < 100 => self.add > -100  (요시가 보는 방향에 따라 수식 달라짐, 아래 있는 것들도 비슷한 원리)
                    self.add += 6 * self.yoshi.heading
                    for i in Things.Pswitchs:
                        if i.rect.colliderect(self.rect) and self.containment == None:
                            
                            self.containment = i
                            i.IsinYoshiMouth = True
                            self.stretch = False
                            self.takeback = True
                            
                            break
                        
                else:
                    self.takeback = True
                    self.stretch = False


            if self.waitForTakeBack:
                self.waitTimer -= 1
                if self.waitTimer <= 0:
                    self.waitTimer = 0
                    self.takeback = True
                    self.waitForTakeBack = False

            if self.containment != None:
                self.containment.rect.center = self.rect.center#(self.x,self.rect.centery)

            if self.takeback:
                if self.add * self.yoshi.heading > 0: #요기
                    self.add -= 6 * self.yoshi.heading
                    
                else:
                    self.add = 0
                    self.takeback = False
                    mario.attack = False
                    
                    
                    if self.containment != None:
                        self.yoshi.mouth = self.containment
                        self.containment.eaten = True
                
                
                        
                
            

    def __init__(self,x,y):
        self.x=x #For display
        self.y=y
        self.image=pygame.image.load("Sprites/Yoshi/Yoshi_idle.png").convert_alpha()
        self.movement=[0,0]
        self.yv=0
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}

        self.tongue = self.Tongue(self)

        self.mouth = None

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.MarioRiding = False
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.heading=1
        self.MoveTimer=0
        self.turning=False
        self.hitlistsV=[]
        self.hitlistsH=[]
        self.holding = False
        self.runaway = False
        Yoshis.append(self)
        
    def collision_test(self,rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    
    def move(self,rect,movement,tiles):
        returnlist=[]
        
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        rect.x+=movement[0]
        
        hit_list = Globals.collision_test(rect,tiles)
        returnlist.append(hit_list)
        
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        
        hit_list = Globals.collision_test(rect,tiles)
        returnlist.append(hit_list)
        
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types,returnlist[0],returnlist[1]

    def Movemotion(self,mario,Ground):
        self.MoveTimer += 1
        if self.MarioRiding:
            mario.LayorTop = True
            self.runaway = False
            if mario.attack:
                if mario.MoveTimer < 8:
                    self.image=pygame.image.load("Sprites/Yoshi/Yoshi_eat.png").convert_alpha()

                
##                if not self.tongue.takeback:
##                    self.tongue.stretch = True
                self.rect.height = 64

                if self.collision_types['bottom']:
                    self.image=pygame.image.load("Sprites/Yoshi/Yoshi_eat.png").convert_alpha()
                else:
                    self.image=pygame.image.load("Sprites/Yoshi/Yoshi_midair_eat.png").convert_alpha()

                if mario.sitting:
                    self.rect.height = 56

            elif self.turning:
                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_" + "hold_" * self.holding + "turn.png").convert_alpha()
                mario.LayorTop = False

            elif mario.sitting:
                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_" + "hold_" * self.holding + "crouch.png").convert_alpha()
                self.rect.height = 56

                
            else:
                self.rect.height = 64
                if self.collision_types['bottom']:
                    if abs(mario.speed)>0:
                        if self.MoveTimer % 12 == 0:
                            self.image=pygame.image.load("Sprites/Yoshi/Yoshi_" + "hold_" * self.holding + "walk1.png").convert_alpha()
                        elif self.MoveTimer % 12 == 4:
                            self.image=pygame.image.load("Sprites/Yoshi/Yoshi_" + "hold_" * self.holding + "walk2.png").convert_alpha()
                        elif self.MoveTimer % 12 == 8:
                            self.image=pygame.image.load("Sprites/Yoshi/Yoshi_" + "hold_" * self.holding + "walk3.png").convert_alpha()
                    else:
                        self.image=pygame.image.load("Sprites/Yoshi/Yoshi_" + "hold_" * self.holding + "walk1.png").convert_alpha()
                else:
                    if self.yv<0:
                        self.image=pygame.image.load("Sprites/Yoshi/Yoshi_" + "hold_" * self.holding + "jump.png").convert_alpha()

                    else:
                        self.image=pygame.image.load("Sprites/Yoshi/Yoshi_" + "hold_" * self.holding + "walk2.png").convert_alpha()
            if mario.calm:
                self.image = pygame.image.load("Sprites/Yoshi/Yoshi_" + "hold_" * self.holding + "turn.png").convert_alpha()
        
        elif self.runaway:
            self.movement[0] = 5 * self.heading
                
            if self.MoveTimer % 12 == 0:
                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_walk1.png").convert_alpha()
            elif self.MoveTimer % 12 == 3:
                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_runaway2.png").convert_alpha()
            elif self.MoveTimer % 12 == 6:
                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_walk3.png").convert_alpha()
            elif self.MoveTimer % 12 == 9:
                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_runaway1.png").convert_alpha()
##            elif self.MoveTimer %6 == 5:
##                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_walk3.png")
##            elif self.MoveTimer %6 ==6:
##                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_runaway3.png")
        else:
            if self.MoveTimer % 26 == 0:
                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_idle.png").convert_alpha()
            elif self.MoveTimer% 26 == 8 :
                self.image=pygame.image.load("Sprites/Yoshi/Yoshi_walk1.png").convert_alpha()

        
    def Physics(self,Ground,mario):
        self.movement=[0,0]
        #key = pygame.key.get_pressed()

        if self.yv > 20:
            self.yv = 20
            
        if mario.rect.colliderect(self.rect):
            if mario.yv > 0 and mario.rect.bottom > self.rect.bottom - 15 and not self.MarioRiding and not mario.holding and not mario.climbing:
                self.MarioRiding = True
                pygame.mixer.Sound("Sounds/yoshi.wav").play()


        if self.collision_types['bottom']:
            self.yv = 0
        if self.MarioRiding:
            self.Movemotion(mario,Ground)
            if self.mouth != None:
                self.holding = True

            self.collision_types = mario.collision_types
            self.rect.bottom = mario.rect.bottom
            if not mario.calm:
                self.heading = mario.heading
            self.yv=mario.yv
            mario.RidingYoshi = True
            mario.TurnAround = False
            mario.Yoshi = self
            self.rect.width = self.image.get_width()
            if mario.heading == 1:
                self.rect.left = mario.rect.left
            else:
                self.rect.right = mario.rect.right
            
        else:
            if self.collision_types['bottom'] and not self.runaway:
                self.yv =- 3
            
            self.yv += 1
            self.movement[1] = self.yv
            self.rect.height = 64
            self.Movemotion(mario,Ground)
            self.rect,self.collision_types,self.hitlistsV,self.hitlistsH=self.move(self.rect,self.movement,Ground)
            if self.collision_types['right'] or self.collision_types['left']:
                self.heading *= -1
            
            
        

            
def loop(screen,Ground,mario):
    for i in Yoshis:
        if not mario.pause:
        #pygame.draw.rect(screen,(0,255,0),(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1],i.rect.width,i.rect.height))
        #pygame.draw.rect(screen,(0,255,0),(i.tongue.rect.x-mario.scroll[0],i.tongue.rect.y-mario.scroll[1],i.tongue.rect.width,i.tongue.rect.height))        
            i.Physics(Ground,mario)
            i.tongue.Physics(mario,Ground)
##        if i.heading==1:screen.blit(i.image,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))
##        else:screen.blit(pygame.transform.flip(i.image,True,False),(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))

def draw(screen,Ground,mario):   
    for i in Yoshis:
##        size = i.image.get_size()
##        i.image=pygame.transform.scale(seungwoo,size)
        if i.rect.left > mario.rangeX[0] * 32 and i.rect.right < mario.rangeX[1] * 32 and i.rect.bottom < mario.rangeY[1] * 32 and i.rect.top > mario.rangeY[0] * 32:

            if mario.attack:#i.tongue.stretch or i.tongue.takeback:
                if i.heading==1:screen.blit(i.tongue.image,(i.tongue.rect.x - mario.scroll[0],i.tongue.rect.y - mario.scroll[1]))
                else:screen.blit(pygame.transform.flip(i.tongue.image,True,False),(i.tongue.rect.x - mario.scroll[0],i.tongue.rect.y - mario.scroll[1]))

                pygame.draw.line(screen,(183,41,1),(i.rect.centerx + (i.rect.width / 2 - 15 ) * i.heading - mario.scroll[0],i.tongue.rect.centery - mario.scroll[1]),(i.tongue.rect.x - mario.scroll[0],i.tongue.rect.centery - mario.scroll[1]),5)

            k = i.rect.height - i.image.get_height()
            if i.heading==1:screen.blit(i.image,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1] + k))
            else:screen.blit(pygame.transform.flip(i.image,True,False),(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1] + k))

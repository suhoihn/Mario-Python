#galumba
import pygame,Effects,math,copy,Globals,Enemy
from Block import Blocks
Galumbas = []
class galumba:
    def __init__(self,x,y):
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Galumba/galumba1.png"),(32,32)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y

        self.MoveTimer = 0
        self.EscapeTarget = None
        self.Flipped = False

        self.yv = 0
        self.heading = -1
        self.holded = False
        self.speed = -2
        self.movement=[0,0]
        self.Dead = False
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}

        Galumbas.append(self)


    def move(self,rect,movement,tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        rect.x+=movement[0]
        if not self.Dead:
            hit_list = Globals.collision_test(rect,tiles)
            for tile in hit_list:
                if movement[0] > 0:
                    rect.right = tile.left
                    collision_types['right'] = True
                elif movement[0] < 0:
                    rect.left = tile.right
                    collision_types['left'] = True
        rect.y += math.ceil(movement[1])#예전에 언급했듯이, 이게 1미만(e.g.0.6)이면 0픽셀만큼 움직여서 콜리션 타입 자체가 실행이 안되므로 0,0.6이 계속 반복되는 상황이 일어난단마리오레오존맛탱
        if not self.Dead:
            hit_list = Globals.collision_test(rect,tiles)
            for tile in hit_list:
                if movement[1] >= 0:
                    rect.bottom = tile.top
                    collision_types['bottom'] = True
                    for j in Blocks:
                        if tile == j.rect:
                            a = False
                            try: a = j.hit
                            except: pass
                            if a:
                                collision_types['bottom'] = False
                                self.Flipped = True
                                self.speed = 0
                                self.yv = -15
                                pygame.mixer.Sound("Sounds/smw_kick.wav").play()
                                break

                elif movement[1] < 0:
                    
                    rect.top = tile.bottom
                    collision_types['top'] = True
                    for j in Blocks:
                        if tile == j.rect:
                            try: j.ActivatedByShell= True
                            except:pass

        return rect, collision_types

    def ThrownBehavior(self,mario,keydown):
        pygame.mixer.Sound("Sounds/smw_kick.wav").play()
        if not mario.LookingUp:
            if keydown:
                self.speed = 3 * mario.heading
                self.yv = 0
            else:
                self.yv = -5
                self.speed = (abs(mario.speed) * 0.8 + 8) * mario.heading
    def reload(self):
        Galumbas.append(self)

    def Physics(self,mario,Ground):
        self.MoveTimer += 1
        key = pygame.key.get_pressed()
        if self.MoveTimer % 10 == 0:
            self.image = pygame.transform.scale(pygame.image.load("Sprites/Galumba/galumba1.png"),(32,32))
        elif self.MoveTimer % 10 == 5:
            self.image = pygame.transform.scale(pygame.image.load("Sprites/Galumba/galumba2.png"),(32,32))
    
        for i in mario.Fireballs:
            if self.rect.colliderect(i.rect) and not self.Dead:
                self.Dead = True
                self.Flipped = True
                self.heading = abs(i.speed)/i.speed
                self.speed = 3 * self.heading
                mario.Fireballs.remove(i)
                pygame.mixer.Sound("Sounds/smw_kick.wav").play()


        if self.EscapeTarget != None:#겹쳐있는거에서 빠져나올 때
            if not self.EscapeTarget.colliderect(self.rect):
                self.EscapeTarget = None

        if self.rect.colliderect(mario.rect) and not self.holded:
            if mario.starman and not self.Dead:
                self.Dead = True
                self.Flipped = True
                self.heading = mario.heading
                self.speed = 3 * self.heading
                pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()
                mario.combo +=1
                if mario.combo > 8:
                    mario.combo = 8
                    mario.life += 1
            if self.Flipped:
                if not self.Dead:
                    if mario.running and not mario.holding:
                        mario.holding = True
                        self.holded = True

            else:
                if mario.SpinJump and mario.yv > 0 and not self.holded:
                    mario.yv -= 10
                    mario.jumpable = True
                    mario.jumping = False
                    pygame.mixer.Sound("Sounds/stomp2.wav").play()
                    Galumbas.remove(self)
                    #self.yv =- 7.5
                    Effects.Effect(mario.rect.centerx,mario.rect.bottom,2,particles = True,TI = 2)
                    #return                

                elif mario.movement[1] > 0 and mario.rect.bottom - self.rect.top < 16 and not mario.starman:
                        self.Flipped = True
                        self.speed = 0
                        mario.yv = -10
                        mario.jumpable = True

                        mario.jumping = False
                        mario.combo+=1
                        if mario.combo > 8:
                            mario.life+=1
                            mario.combo = 8
                        pygame.mixer.Sound("Sounds/combo"+str(mario.combo)+".WAV").play()

                else:
                    mario.Death()



        for i in Enemy.KoopaTroopas:
            if i.rect.colliderect(self.rect):
                if (i.state == "Dead" or i.state == "Normal") and self.holded:
                    pass
                if i.state == "Roll":
                    if self.holded:
                        self.speed = -self.heading * 4
                        i.speed = self.heading * 4
                        i.rect.y = self.rect.y
                        self.yv = -10
                        i.yv = -10
                        
                        self.state = "Gone"

                        pygame.mixer.Sound("Sounds/smw_kick.wav").play()
                    elif not self.Dead:
                        self.Dead = True
                        self.Flipped = True
                        i.combo += 1
                        if i.combo > 8:
                            i.combo = 8
                            mario.life += 1
                        pygame.mixer.Sound("Sounds/combo"+str(i.combo)+".WAV").play()


        if self.holded:
            if mario.starman:
                self.holded = False
                mario.holding = False

            
            mario.Holded_Object_Loop(self)

        else:
            self.yv += Globals.GRAVITY
            self.movement = [self.speed,self.yv]
            self.rect,self.collision_types = self.move(self.rect,self.movement,Ground)
           
            if abs(self.speed) < 1:
                self.speed = 0
            if self.collision_types['bottom']:
                self.yv = 0
                if self.Flipped:
                    self.speed *= 0.7

            if self.collision_types['top']:
                self.yv = 0


            if self.collision_types['left'] or self.collision_types['right'] and not self.Dead:
                if self.Flipped:
                    self.speed = 0
                else:
                    self.speed *= -1
                    self.heading *= -1

        for i in Galumbas:
            if i.rect.colliderect(self.rect):
                if i != self:
                    if self.Flipped and (self.yv != 0 or self.holded) and not self.Dead:
                        pygame.mixer.Sound("Sounds/smw_kick.wav").play()
                        self.heading = 2 * (self.rect.x > i.rect.x) - 1
                        i.heading = self.heading * -1
                        i.Flipped = True
                        mario.holding = False
                        i.speed = 3 * i.heading
                        self.speed = 3 * self.heading
                        i.Dead = True
                        self.Dead = True
                        i.rect.bottom = self.rect.bottom
                        self.holded = False
                        i.holded = False
                        self.yv = -4
                        i.yv = -4

                        
                        
                    if not self.Flipped and self.EscapeTarget == None and not self.Dead and not i.Dead:
                        self.EscapeTarget = copy.deepcopy(i.rect)
                        i.EscapeTarget = copy.deepcopy(self.rect)
                        self.speed *= -1
                        i.speed *= -1
                        i.heading *= -1
                        self.heading *= -1
def loop(screen,mario,Ground):
    for i in Galumbas:
        if 0 <= i.rect.x-mario.scroll[0] <= 640 and 0 <= i.rect.y-mario.scroll[1] <= 480:
            if not mario.pause:
                i.Physics(mario,Ground)
            screen.blit(pygame.transform.flip(i.image,(i.heading == 1),i.Flipped),(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))

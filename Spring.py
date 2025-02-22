#Spring
import pygame,Globals
RMemory = []#Respawn Memory
Springs = []
class Spring:
    def __init__(self,x,y,direction = 0):
        self.direction = direction  # 0 - vertical, 1 - horizontal
        self.speed = 0
        self.yv = 0
        self.movement = [0,0]
        self.images = [pygame.image.load("Sprites/Spring/Spring1.png").convert_alpha(),
                       pygame.image.load("Sprites/Spring/Spring2.png").convert_alpha(),
                       pygame.image.load("Sprites/Spring/Spring3.png").convert_alpha()]

        if self.direction == 1:
            for n,i in enumerate(self.images):
                self.images[n] = pygame.transform.rotate(i,90)
                
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.holded = False
        self.stepped = False
        self.JumpedOn = False

        self.eaten = False

        self.MotionTimer = 0
        self.LockedPos = 0
        self.ThrownTimer = 0
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        Springs.append(self)
    def move(self,rect,movement,tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        rect.x += movement[0]
        hit_list = Globals.collision_test(rect,tiles)
        
        for tile in hit_list:
            if tile == self.rect: continue
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = Globals.collision_test(rect,tiles)
        for tile in hit_list:
            if tile == self.rect: continue
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
       
        return rect, collision_types
        
    def reload(self):
        Springs.append(self)

    def ThrownBehavior(self,mario,keydown):
        if not mario.LookingUp:
            if keydown:
                self.speed = 3 * mario.heading
                self.yv = 0
            else:
                self.yv = -5
                self.speed = (abs(mario.speed) * 0.8 + 8) * mario.heading

    def Physics(self,mario,Ground):
        self.movement = [0,0]
        self.movement[0] = self.speed
        self.movement[1] = self.yv
        self.rect,self.collision_types = self.move(self.rect,self.movement,Ground)
        self.yv += Globals.GRAVITY
        
        if self.collision_types['bottom']:
            self.speed *= 0.85

        if abs(self.speed) < 1:
            self.speed = 0
            
        if self.yv > 15:
            self.yv = 15
            
        if mario.RidingYoshi:
            if mario.attack:
                if self.eaten:
                    self.rect.center = mario.Yoshi.tongue.rect.center
                else:
                    if mario.Yoshi.tongue.rect.colliderect(self.rect):
                        self.eaten = True
            else:
                if self.eaten:
                    mario.Yoshi.holding = True
                    mario.Yoshi.tongue.eatenObject = self
                    Springs.remove(self)

        if self.stepped:
            if self.MotionTimer == 0:
                if self.direction == 0: self.LockedPos = self.rect.bottom
                else: self.LockedPos = self.rect.bottom
                
            self.MotionTimer += 1
            
            if self.MotionTimer == 2:
                self.image = self.images[1]
            elif self.MotionTimer == 4:
                self.image = self.images[2]
            elif self.MotionTimer == 6:
                self.image = self.images[1]
            elif self.MotionTimer >= 8:
                self.image = self.images[0]
                self.stepped = False
        else:
            self.MotionTimer = 0


        if self.direction == 0: #vertical
                    
                

            if self.MotionTimer != 0:
                self.rect.height = self.image.get_height()
                self.rect.bottom = self.LockedPos

            if self.collision_types['bottom'] or self.collision_types['top']:
                self.yv = 0
            if self.collision_types['left'] or self.collision_types['right']:
                self.speed = 0
                
            if mario.running:
                if self.rect in mario.hitlistsH and not mario.holding and mario.rect.bottom > self.rect.top + 15:
                    if self.ThrownTimer > 20:
                        self.holded = True
                        mario.holding = True
            key = pygame.key.get_pressed()
            if self.holded:
                self.ThrownTimer = 0
                self.yv = 0
                mario.Holded_Object_Loop(self)#그냥 holded object를 assign해버리자
                
            else:
                self.ThrownTimer += 1
                if self.rect in mario.hitlistsV and mario.collision_types['bottom']:# and self.rect.left <= mario.rect.right and mario.rect.left <= self.rect.right and mario.rect.bottom - self.rect.top < 17 and mario.yv > 0:
                    #mario.jumpable = True
                    mario.jumping = True
                    pygame.mixer.Sound("Sounds/smw_spring_jump.wav").play()
                    self.stepped = True
                    self.JumpedOn = True

                #print(self.stepped)#,self.JumpedOn)

                if self.stepped and self.JumpedOn:
                    if key[pygame.K_UP]:
                        mario.yv = -23
                    else:
                        mario.yv = -10
                    self.JumpedOn = False
        else:
            if self.rect in mario.hitlistsH:
                pygame.mixer.Sound("Sounds/smw_spring_jump.wav").play()
                self.stepped = True
                if mario.collision_types['left']:
                    mario.collision_types['left'] = False
                    mario.speed = -15
                elif mario.collision_types['right']:
                    mario.collision_types['right'] = False
                    mario.speed = 15

def loop(screen,mario,Ground):
    for i in Springs:
        if i.rect.left > mario.rangeX[0] * 32 and i.rect.right < mario.rangeX[1] * 32 and i.rect.bottom < mario.rangeY[1] * 32 and i.rect.top > mario.rangeY[0] * 32 or i.holded:
            if not mario.pause:
                i.Physics(mario,Ground)
            screen.blit(i.image,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))
        else:
            RMemory.append(i)
            Springs.remove(i)

    for i in RMemory:
        if mario.scroll[0] > i.x > mario.rangeX[0] * 32 or mario.scroll[0] + 640 < i.x < mario.rangeX[1] * 32 or mario.scroll[1] > i.y > mario.rangeY[0] * 32 or mario.scroll[1] + 480 < i.y < mario.rangeY[1] * 32:# and i.transition:
            Spring(i.x,i.y,direction = i.direction)
            RMemory.remove(i)



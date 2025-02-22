#Holdable things
import pygame,math,Effects,Globals
RMemory = []#Respawn Memory
Pswitchs=[]
class Pswitch:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.image=pygame.image.load("Sprites/Blocks/P Switch/Blue-Normal.png").convert_alpha()
        self.yv=0
        self.timer=0
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.holded=False
        self.eaten = False
        self.activated=False
        self.speed=0
        self.movement=[0,0]
        self.transition = False
        #self.hitlistsV = []
        self.collision_types={'top':False,'bottom':False,'right':False,'left':False}
        Pswitchs.append(self)
        
    def reload(self):
        Pswitchs.append(self)
        
    def collision_test(self,rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile) and tile != self.rect:
                hit_list.append(tile)
        return hit_list

    def move(self,rect,movement,tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    
        
        rect.x+=movement[0]
        hit_list = Globals.collision_test(rect,tiles)
        for tile in hit_list:
            if tile != self.rect:
                if movement[0] > 0:
                    rect.right = tile.left
                    collision_types['right'] = True
                elif movement[0] < 0:
                    rect.left = tile.right
                    collision_types['left'] = True
                
        rect.y += math.ceil(movement[1])
        hit_list = Globals.collision_test(rect,tiles)
        for tile in hit_list:
            if tile != self.rect:
                if movement[1] > 0:
                    rect.bottom = tile.top
                    collision_types['bottom'] = True
                elif movement[1] < 0:
                    rect.top = tile.bottom
                    collision_types['top'] = True

        
        return rect, collision_types

    def remove(self):
        Pswitchs.remove(self)
    
    def ThrownBehavior(self,mario,keydown):
        if not mario.LookingUp:
            if keydown:
                self.speed = 3 * mario.heading
                self.yv = 0
            else:
                self.yv = -5
                self.speed = (abs(mario.speed) * 0.8 + 8) * mario.heading

    def Physics(self,mario,Ground):
        
        # 스위치는 마리오만 벽 취급 (for P-Jumps)
        key = pygame.key.get_pressed()
        self.movement = [0,0]
        if self.activated:
            if self.timer == 0:
                mario.playPsong()
            self.timer+=1
            if self.timer > 10:
                mario.onpswitch = False
                Effects.Effect(self.rect.centerx,self.rect.centery,2,particles = False,TI = 8)

                Pswitchs.remove(self)

                
        
        if mario.running:
            if self.rect in mario.hitlistsH or (self.rect in mario.hitlistsV and mario.collision_types['top']):
                if not mario.holding and not self.activated:
                    self.holded = True
                    mario.holding = True

        self.movement[0] += self.speed
        if self.holded:
            self.yv = 0
            mario.Holded_Object_Loop(self)

        else:
            self.yv += Globals.GRAVITY
            self.movement[1] = self.yv

            self.rect,self.collision_types = self.move(self.rect,self.movement,Ground)
            if self.collision_types['top']: self.yv = 0
            if self.collision_types['bottom']:
                self.yv = 0
                self.speed *= 0.85
            if self.collision_types['left'] or self.collision_types['right']:
                self.speed = 0
            if abs(self.speed) < 1:
                self.speed = 0
            
                

        oldpos = self.rect.bottom
        if self.activated:
            self.image = pygame.image.load("Sprites/Blocks/P Switch/Blue Pressed.png") 
            self.rect.height = self.image.get_height()
           
        self.rect.bottom = oldpos
        if self.activated :
            if mario.onpswitch and self.rect in mario.hitlistsV and not mario.jumping:
                mario.rect.bottom = self.rect.top
                mario.collision_types['bottom'] = True
                mario.yv = 0
            
            
        if self.yv > 15:
            self.yv = 15
            
        if self.rect in mario.hitlistsV and mario.collision_types['bottom']:
            self.activated=True
            if self.timer == 0:
                mario.onpswitch = True
                mario.rect.bottom = self.rect.top
                
                
        
        
        
def loop(screen,mario,Ground):
    for i in Pswitchs:
        if not i.eaten:
            if i.rect.left > mario.rangeX[0] * 32 and i.rect.right < mario.rangeX[1] * 32 and i.rect.bottom < mario.rangeY[1] * 32 and i.rect.top > mario.rangeY[0] * 32 or i.holded:
                if not mario.pause:
                    i.Physics(mario,Ground)
                screen.blit(i.image,(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
            else:
                i.transition = False
                RMemory.append(i)
                Pswitchs.remove(i)
        
    for i in RMemory:
        if mario.scroll[0] > i.x > mario.rangeX[0] * 32 or mario.scroll[0] + 640 < i.x < mario.rangeX[1] * 32 or mario.scroll[1] > i.y > mario.rangeY[0] * 32 or mario.scroll[1] + 480 < i.y < mario.rangeY[1] * 32:# and i.transition:
            Pswitch(i.x,i.y)
            RMemory.remove(i)

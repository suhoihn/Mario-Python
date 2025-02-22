#Mushroom
import pygame,math,Globals
Mushrooms = []
def collision_test(rect,tiles):
    return Globals.collision_test(rect,tiles)
class Mushroom:
    def __init__(self,Box,Type = "Mushroom"):#Relative -> 마리오가 큰 상태면 그에 따라 다르게 나오는 것
        self.x = Box.rect.x
        self.y = Box.rect.y
        self.idx = 0
        self.Box = Box
        self.Out = False
        self.Gone = False
        self.type = Type
        if self.type == "Mushroom":
            self.image = pygame.transform.scale(pygame.image.load("Sprites/Mushrooms/1.png"),(32,32)).convert_alpha() #16 16
        else:
            self.image = pygame.transform.scale(pygame.image.load("Sprites/Mushrooms/2.png"),(32,32)).convert_alpha() #16 16
        
        self.Onslope = False
        self.Onslope2 = False
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}

        self.rect = self.image.get_rect()
        self.rect.topleft = Box.rect.topleft
        
        self.yv = 0
        self.heading = 1
        self.speed = 0
        self.idx -= 1.2#나오는 속도
        self.state="Out"
        pygame.mixer.Sound("Sounds/powerup.wav").play()
        Mushrooms.append(self)
        
    def move(self,rect,movement,tiles,slopes):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        for i in range(4):
            if self.Onslope:# or collision_types['bottom']:
                rect.y += 5
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
                    pos_height = 0
                # add constraints
                pos_height = min(pos_height, 32)
                pos_height = max(pos_height, 0)
                target_y = hitbox.y + 64 - pos_height
                
                if rect.bottom > target_y:
                    
                    rect.bottom = target_y

                    collision_types['bottom'] = True
                    self.Onslope = True
                    self.Onslope2 = True
                    
        if not self.Onslope and self.Onslope2:
            self.Onslope2 = False
            rect.y -= 20
            
        rect.x += movement[0]
        hit_list = collision_test(rect,tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = collision_test(rect,tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        
            

        return rect, collision_types

    def PopOut(self):
        self.idx -= 1.2#나오는 속도
        self.state="Out"
        #self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        

        if not self.Out:
            if self.rect.top == self.Box.rect.top:#처음 나왔을 때
                self.idx = self.Box.rect.top - 1
                pygame.mixer.Sound("Sounds/powerup.wav").play()
            if self.rect.bottom > self.Box.rect.top:
                self.rect.y = self.idx
            else:
                self.Out=True

    def Physics(self,mario,Grounds,Slopes):
        if self.Out:
            self.speed = 3 * self.heading
            self.yv += 0.8
            self.rect, self.collision_types = self.move(self.rect, [self.speed, self.yv], Grounds, Slopes)
            if self.collision_types['bottom']:
                self.yv = 0
            if self.collision_types['left'] or self.collision_types['right']:
                self.heading *= -1
        else:
            if self.rect.bottom > self.Box.rect.top:
                self.rect.y -= 1
            else:
                self.Out=True
  
        if self.rect.colliderect(mario.rect) and not self.Gone and self.Out:
            if self.type == "Mushroom":
                if mario.state == "big" or mario.fire or mario.cape or mario.MegamanMode:
                    pygame.mixer.Sound("Sounds/smw_reserve_item_store.wav").play()

                else:
                    pygame.mixer.Sound("Sounds/smw_mushroom.wav").play()
                    mario.MoveTimer = -1
                    mario.PowerChange = True
                    mario.howchanging = "Grow"
            elif self.type == "1up":
                mario.life += 1
                pygame.mixer.Sound("Sounds/combo8.WAV").play()

            self.Gone = True
                
            
        if self.Gone or self.rect.top > Globals.rangeY[1] * 32:
            Mushrooms.remove(self)

class Feather:
    def __init__(self,Box):
        self.Box = Box
        self.idx = 0
        self.Out = False
        self.Gone = False
        self.state = "Out"
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Mushrooms/Feather.png"),(32,32)) #16 16
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Box.rect.x, Box.rect.y
        self.yv = 0
        pygame.mixer.Sound("Sounds/powerup.wav").play()
        Mushrooms.append(self)

    def PopOut(self):
        self.state = "Out"

        if not self.Out:
            if self.rect.bottom > self.Box.rect.top - 30:
                self.rect.y -= 5
            else:
                self.Out=True

    def Physics(self,mario,k,p):
        if self.Out:
            self.idx += 1
            self.rect.centerx = self.Box.rect.centerx + math.sin(math.pi + self.idx * 0.15) * 30
            self.rect.y += 1.25
        else:
            if self.rect.bottom > self.Box.rect.top - 30:
                self.rect.y -= 5
            else:
                self.Out=True

        if self.rect.colliderect(mario.rect) and not self.Gone and self.Out:
            self.Gone = True
            mario.fire = False
            if mario.cape or mario.MegamanMode:
                pygame.mixer.Sound("Sounds/smw_reserve_item_store.wav").play()
                
            else:
                pygame.mixer.Sound("Sounds/smw_feather_get.wav").play()
                
                
                mario.MoveTimer = -1
                mario.PowerChange = True
                mario.howchanging = "Grow"
                mario.cape = True
                
            
        if self.Gone:
            Mushrooms.remove(self)

class FireFlower:
    def __init__(self,Box):
        self.Box = Box
        self.Out = False
        self.Gone = False
        self.state = "Out"
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Mushrooms/FireFlower.png"),(32,32)).convert_alpha() #16 16
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Box.rect.x, Box.rect.y
        pygame.mixer.Sound("Sounds/powerup.wav").play()
        Mushrooms.append(self)
        

    def PopOut(self):
        self.state = "Out"
        if self.rect.top == self.Box.rect.top:#처음 나왔을 때
            pygame.mixer.Sound("Sounds/powerup.wav").play()

        if self.rect.y > self.Box.rect.y - self.Box.rect.height:
            self.rect.y -= 1.2
        else:
            self.Out=True

    def Physics(self,mario,k,p):
        if not self.Out:
            if self.rect.y > self.Box.rect.y - self.Box.rect.height:
                self.rect.y -= 1.2
            else:
                self.Out=True

        if self.rect.colliderect(mario.rect) and not self.Gone and self.Out:
            self.Gone = True
            mario.cape = False
            if mario.MegamanMode:
                if mario.MMFire:
                    pygame.mixer.Sound("Sounds/smw_reserve_item_store.wav").play()
                else:
                    pygame.mixer.Sound("Sounds/smw_mushroom.wav").play()
                    mario.MoveTimer = -1
                    mario.PowerChange = True


            elif mario.fire:
                pygame.mixer.Sound("Sounds/smw_reserve_item_store.wav").play()
                
            else:
                pygame.mixer.Sound("Sounds/smw_mushroom.wav").play()
                
                mario.state = "big"
                mario.MoveTimer = -1
                mario.PowerChangeReserved = True
                mario.howchanging = "Grow"
                mario.fire = True
            
            
        if self.Gone:
            Mushrooms.remove(self)
class MegamanPowerup:
    def __init__(self,Box):
        self.Box = Box
        self.Out = False
        self.Gone = False
        self.state = "Out"
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Mushrooms/MM1up.png"),(32,32)).convert_alpha() #16 16
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Box.rect.x, Box.rect.y
        pygame.mixer.Sound("Sounds/powerup.wav").play()
        Mushrooms.append(self)
        

    def PopOut(self):
        self.state = "Out"
        if self.rect.top == self.Box.rect.top:#처음 나왔을 때
            pygame.mixer.Sound("Sounds/powerup.wav").play()
        if self.rect.y > self.Box.rect.y - self.Box.rect.height:
            self.rect.y -= 1
        else:
            self.Out=True

    def Physics(self,mario,k,p):
        if not self.Out:
            if self.rect.y > self.Box.rect.y - self.Box.rect.height:
                self.rect.y -= 1
            else:
                self.Out=True

        if self.rect.colliderect(mario.rect) and not self.Gone and self.Out:
            self.Gone = True
            mario.cape = False
            mario.fire = False
            mario.state = "small"
            mario.sitting = False
            mario.holding = False
            mario.MegamanMode = True
            pygame.mixer.Sound("Sounds/Mega Man 4 SFX (9).wav").play()            
            
        if self.Gone:
            Mushrooms.remove(self)

class Star:
    def __init__(self,Box):
        self.Box = Box
        self.idx = 0
        self.Out = False
        self.Gone = False
        self.state = "Out"
        self.image = pygame.transform.scale(pygame.image.load("Sprites/Mushrooms/star1.png"),(32,32)).convert_alpha() #16 16
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Box.rect.x, Box.rect.y

        self.Onslope = False
        self.Onslope2 = False
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.yv = 0
        self.heading = 1
        Mushrooms.append(self)

    def PopOut(self):
        self.state = "Out"
        if not self.Out:
            if self.rect.bottom > self.Box.rect.top:
                self.rect.y -= 1.2
            else:
                self.Out=True
        
    def move(self,rect,movement,tiles,slopes):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        for i in range(4):
            if self.Onslope:# or collision_types['bottom']:
                rect.y += 5
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
                    pos_height = 0

                # add constraints
                pos_height = min(pos_height, 32)
                
                pos_height = max(pos_height, 0)
                target_y = hitbox.y + 32 - pos_height
                
                if rect.bottom > target_y:
                    
                    rect.bottom = target_y

                    collision_types['bottom'] = True
                    self.Onslope = True
                    self.Onslope2 = True
                    
        if not self.Onslope and self.Onslope2:
            self.Onslope2 = False
            rect.y -= 20
        rect.x+=movement[0]
        hit_list = collision_test(rect,tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = collision_test(rect,tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        
            

        return rect, collision_types
    def Physics(self,mario,Grounds,Slopes):
        if self.Out:
            self.yv += 0.8
            self.rect, self.collision_types = self.move(self.rect, [3 * self.heading, self.yv], Grounds, Slopes)
            if self.collision_types['bottom']:
                self.yv = -10
            if self.collision_types['top']:
                self.yv = 0
            if self.collision_types['left'] or self.collision_types['right']:
                self.heading *= -1
        else:
            if self.rect.bottom > self.Box.rect.top:
                self.rect.y -= 1.2
            else:
                self.Out=True

        if self.rect.colliderect(mario.rect) and not self.Gone and self.Out:
            self.Gone = True
            pygame.mixer.Sound("Sounds/smw_mushroom.wav").play()
            mario.StarTimer = pygame.time.get_ticks()
            mario.MoveTimer = -1
            mario.starman = True
            
        if self.Gone:
            Mushrooms.remove(self)
    
            
        
        

def loop(screen,mario,Grounds,Slopes):
    #print(len(Mushrooms))
    for i in Mushrooms:
        screen.blit(i.image,(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
        if not mario.pause:
            i.Physics(mario,Grounds,Slopes)
        
        

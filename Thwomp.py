import pygame, Effects,Globals
Thwomps = []
class Thwomp:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rootY = y
        self.images = [Globals.trans_img_size(pygame.image.load("Sprites/thwomp/thwomp.png"),2),#fall
                       Globals.trans_img_size(pygame.image.load("Sprites/thwomp/thwomp2.png"),2),#glance(L)
                       pygame.transform.flip(Globals.trans_img_size(pygame.image.load("Sprites/thwomp/thwomp2.png"),2),True,False),#glance(R)
                       Globals.trans_img_size(pygame.image.load("Sprites/thwomp/thwomp3.png"),2)]#normal
                       
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.falling=False
        self.GoUp=False
        self.timer=0
        self.Dead=False
        self.movement=[0,0]
        Thwomps.append(self)
    def Physics(self,Ground,mario):
        if self.rect.colliderect(mario.rect):
            if mario.rect.bottom < self.rect.centery:#self.collision_check(self.rect,self.movement,[mario.rect])['top']==True or self.collision_check(self.rect,self.movement,[mario.rect])['bottom']==True:
                if mario.SpinJump:
                    pygame.mixer.Sound("Sounds/smw_stomp_no_damage.wav").play()
                    mario.yv = -10
                    Effects.Effect(mario.rect.centerx,mario.rect.bottom,1)

                    mario.jumping = False
                    mario.jumpable = True
                else:
                    mario.Death()
            else:
                mario.Death()
                
        self.image = self.images[3]
        if not self.GoUp and not self.falling and self.rect.centery < mario.rect.bottom:
            if abs(mario.rect.centerx - self.rect.centerx) < 256:
                if mario.rect.centerx > self.rect.centerx:
                    self.image = self.images[2]
                else:
                    self.image = self.images[1]
        
        if abs(mario.rect.centerx - self.rect.centerx) < 128 and not (True in [self.rect.colliderect(i) for i in Ground]) and not self.GoUp and self.rect.centery < mario.rect.bottom: # 올라가는 동안은 다시 내려오면 안됨
            self.falling = True
    
        if self.falling:
            self.timer = 0# 한번만 trigger 끝가지 내려오면 위로만 올라가기
            self.rect.y += 10
            self.movement = [0,10]
            self.image = self.images[0]
            if Globals.collision_test(self.rect,Ground):
                pygame.mixer.Sound("Sounds/smash.wav").play()
                self.falling = False
                self.GoUp = True
                mario.ScreenShake(50,3)

        if self.GoUp and self.rect.y > self.rootY:
            if self.timer > 80:
                self.rect.y -= 2
                self.movement = [0,-2]
            else:
                self.image = self.images[0]
                self.timer += 1
        else:       
            self.GoUp = False


        #self.move(self.rect,self.movement,Ground)
##        else:
##            self.angle+=10
##            self.rootX+=2
##            self.y+=6
                

    def move(self,rect,movement,tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
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
        #return rect, collision_types
        
    def collision_test(self,rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list




def loop(screen,Ground,mario):
    for i in Thwomps:
        if not mario.GamePause:
            i.Physics(Ground,mario)
        screen.blit(i.image,(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
        #pygame.draw.rect(screen,(255,0,0),(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1],*i.rect.size))

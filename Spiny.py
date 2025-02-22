#spiny
import pygame,Effects
Spinies=[]
class spiny(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.image=pygame.transform.scale(pygame.image.load("Sprites/Spiny/spiny1.png"),(32,32))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

        self.IsinYoshiMouth = False
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.MoveTimer=0
        self.yv=0
        self.heading=1
        self.Dead=False
        
        self.movement=[0,0]
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}

        Spinies.append(self)

    def collision_test(self,rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self,rect,movement,tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        rect.x+=movement[0]
        hit_list = self.collision_test(rect,tiles)
        if not self.Dead:
            for tile in hit_list:
                if movement[0] > 0:
                    rect.right = tile.left
                    collision_types['right'] = True
                elif movement[0] < 0:
                    rect.left = tile.right
                    collision_types['left'] = True
        rect.y += movement[1]
        hit_list = self.collision_test(rect,tiles)
        if not self.Dead:
            for tile in hit_list:
                if movement[1] > 0:
                    rect.bottom = tile.top
                    collision_types['bottom'] = True
                elif movement[1] < 0:
                    rect.top = tile.bottom
                    collision_types['top'] = True
        return rect, collision_types

    def remove(self):
        Spinies.remove(self)
    def Physics(self,mario,Ground):
        if self.IsinYoshiMouth:
            self.movement=[0,0]
        else:
            self.MoveTimer+=1
            if self.MoveTimer %4 == 0:
                self.image=pygame.transform.scale(pygame.image.load("Sprites/Spiny/spiny1.png"),(32,32))
            elif self.MoveTimer %4 == 2:
                self.image=pygame.transform.scale(pygame.image.load("Sprites/Spiny/spiny2.png"),(32,32))

            for i in Spinies:
                if i.rect.colliderect(self.rect):
                    self.heading*=-1
                    i.heading*=-1

            if self.collision_types['bottom']:# or self.collision_types['top']:
                self.yv=0
            if self.collision_types['left'] or self.collision_types['right']:
                self.heading*=-1

            if self.rect.colliderect(mario.rect) and mario.yv>5 and mario.SpinJump:
                mario.jumpable=True
                mario.jumping=False
                mario.yv=-8
                Effects.Effect(mario.rect.centerx,mario.rect.bottom,1)
                pygame.mixer.Sound("Sounds/smw_stomp_no_damage.wav").play()

            
            self.movement[0]=self.heading*2
            self.movement[1]=self.yv
            self.rect,self.collision_types=self.move(self.rect,self.movement,Ground)
            self.yv+=0.2
            if self.yv>20:
                self.yv=20

def loop(screen,mario,Ground):
    for i in Spinies:
        if not mario.pause:
            i.Physics(mario,Ground)
        if i.heading==-1:screen.blit(i.image,(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))
        else:screen.blit(pygame.transform.flip(i.image,True,False),(i.rect.x-mario.scroll[0],i.rect.y-mario.scroll[1]))


#cape
import pygame,os
class Cape:
    def __init__(self):
        self.image = pygame.image.load("Sprites/Cape/idle.png").convert_alpha()
        self.idx = 0

        self.images = {}
        file_list = os.listdir("Sprites/Cape")
           
        for i in file_list:
            self.images[i] = pygame.image.load("Sprites/Cape/" + i).convert_alpha()


        self.offset = [0,0]

    def Physics(self,mario):
        self.idx += 1
        self.offset = [0,0]

        if mario.TurnAround:
            if mario.yv > 0:
                self.image = self.images["fall1.png"]
                self.offset = [15,30]
                
            else:
                if mario.heading == 1 or mario.heading == -1: #마리오가 도는 방향에 맞춰
                    self.image = self.images["walk2.png"]
                    
                elif mario.heading == 0:
                    self.image = self.images["slowdown1.png"]

                
                self.offset = [18,20]
            
        else:
              
            if mario.collision_types['bottom']:
                if abs(mario.speed) > 0:#not (key[pygame.K_LEFT] and key[pygame.K_RIGHT]):
                    self.offset = [18,18]
                    if 0 <= self.idx % 8 < 2:
                        self.offset = [18,10]
                    if self.idx % 8 == 0:
                        self.image = self.images["walk1.png"]
                    if self.idx % 8 == 2:
                        self.image = self.images["walk2.png"]
                    if self.idx % 8 == 4:
                        self.image = self.images["walk3.png"]
                    if self.idx % 8 == 6:
                        self.image = self.images["walk4.png"]
                else:
                    self.offset = [6,0]
                    self.idx = 0
                    if not mario.SlippingDown:
                        self.image = self.images["idle.png"]

            else:
                if mario.yv <= 0 and not mario.SlippingDown:
                    self.image = self.images["idle.png"]
                    self.offset[0] = 8
                    
                else:
                    self.offset = [12,20]
                    if self.idx % 6 == 0:
                        self.image = self.images["fall1.png"]
                    elif self.idx % 6 == 2:
                        self.image = self.images["fall2.png"]
                    elif self.idx% 6 == 4:
                        self.image = self.images["fall3.png"]
                   

       
            if mario.heading == 0:
                self.image = self.images["back.png"]
                self.offset[1] = 0

        
        self.rect = self.image.get_rect()

        if mario.RidingYoshi:
            self.offset[0] += 5
            self.offset[1] += 18
        
                
        self.rect.bottom = mario.rect.bottom - self.offset[1]
        if mario.heading == 1 or (mario.heading == 0 and (mario.TurnAround and mario.LookingBack)):
            self.rect.left = mario.rect.left - self.offset[0]
        elif mario.heading == -1 or (mario.heading == 0 and (mario.TurnAround and not mario.LookingBack)):
            self.rect.right = mario.rect.right + self.offset[0]
        else:
            self.rect.centerx = mario.rect.centerx

        #마리오 스크립트에 넣자
        key = pygame.key.get_pressed()
        if not mario.collision_types['bottom']:
            if key[pygame.K_UP]:
                mario.yvLimit = 4
            else:  
                mario.yvLimit = 12

                
                
cape = Cape()
capes = [cape]#호환성 이유
def loop(screen,mario):
    for i in capes:
        if mario.cape and not mario.flying:
            i.Physics(mario)
            if not mario.Nodisplay and mario.CapeDisplay:
                if mario.heading == 1 or (mario.heading == 0 and mario.LookingBack):
                    screen.blit(pygame.transform.flip(i.image,True,False),(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))
                elif mario.heading == -1 or (mario.heading == 0 and not mario.LookingBack):
                    screen.blit(i.image,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))
        else:
            mario.yvLimit = 12

#성공
import pygame,sys,math
screen = pygame.display.set_mode((640,480))
ground = pygame.transform.scale(pygame.image.load("모양 2.png"),(320,480))
ground_m = pygame.mask.from_surface(ground)
DOT = pygame.mask.from_surface(pygame.Surface((10,10)).convert_alpha())
slope=0
pygame.init()
pygame.mixer.music.load("BGM/Athletic Theme.mp3")
pygame.mixer.music.play(-1)


Map ="""
        000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000(000000000000000000000000000000000000002300000G0000000000000
        00000000000000000000000000000000000000000000000000000000000000011111110000000000000002111300000000000000000000000000000000000(000000000000000000000000000000000000000465000213000000000000
        0000000000000000000000000000000000000000000000000000000000000000000000000000000000000455560000000000000000000000000000000000(0000000000000000000000000000000000000000460000456000000000000
        000000000000000000000000011111110000000000000000000000000000000000000000000000000000045556000000000000000000000000000000000(00000000000000000000000000000000000000000460005456000000000000
        00000000000000000000000000000000000000000000000000000000000000000000000000000000000004555600000000000000000000000000000000()00000000000000000000000021300000000000000460000456000000000000
        000000000000000021111302300000002300000000000000000000000000000000000000000000000000045556000000000000000000000000000000000000000000000000000000000045600000000000000465000456000000000000
        001010002111300045555604600000005500000000000000000000000000000000000000001000000000045556000000000000000000000000000000(0000)000000000000000000000045600000000000000000000456000000000000
        215151115555511155555501111111115511111111111111111111111111111111111111111111111111155555111111111111111111111111111111111111111111111111111111111155511111111111111111111555111111111111"""


scroll = [0,0]

game_map = []
for row in Map.split("\n"):
    game_map.append(list(row))
TM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top_middle.png")),(32,32))
TL=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top_left.png")),(32,32))
TR=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top_right.png")),(32,32))
LM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_left_middle.png")),(32,32))
MM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_middle_middle.png")),(32,32))
RM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_right_middle.png")),(32,32))
S1=pygame.transform.scale((pygame.image.load("Sprites/Ground/slope.png")),(32,32))
S2=pygame.transform.flip(S1,True,False)
def draw(screen):
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                screen.blit(TM,(x*32-int(scroll[0]),y*32-int(scroll[1])))
            elif tile == '2':
                screen.blit(TL,(x*32-int(scroll[0]),y*32-int(scroll[1])))
            elif tile == '3':
                screen.blit(TR,(x*32-int(scroll[0]),y*32-int(scroll[1])))
            elif tile == '4':
                screen.blit(LM,(x*32-int(scroll[0]),y*32-int(scroll[1])))
            elif tile == '5':
                screen.blit(MM,(x*32-int(scroll[0]),y*32-int(scroll[1])))
            elif tile == '6':
                screen.blit(RM,(x*32-int(scroll[0]),y*32-int(scroll[1])))
            elif tile == '(':
                screen.blit(S1,(x*32-int(scroll[0]),y*32-int(scroll[1])))
            elif tile == ')':
                screen.blit(S2,(x*32-int(scroll[0]),y*32-int(scroll[1])))                
            x += 1
        y += 1
def loop(screen):
    Grounds = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                Grounds.append([TM,(x*32,y*32)])
            elif tile == '2':
                Grounds.append([TL,(x*32,y*32)])
            elif tile == '3':
                Grounds.append([TR,(x*32,y*32)])
            elif tile == '4':
                Grounds.append([LM,(x*32,y*32)])
            elif tile == '5':
                Grounds.append([MM,(x*32,y*32)])
            elif tile == '6':
                Grounds.append([RM,(x*32,y*32)])
            elif tile == '(':
                Grounds.append([S1,(x*32,y*32)])
            elif tile == ')':
                Grounds.append([S2,(x*32,y*32)])
                
            x += 1
        y += 1
    return Grounds

def LevelCollide(surface,pos):
    for i in loop(screen):
        if pygame.mask.from_surface(i[0]).overlap(surface,(pos[0] - i[1][0] , pos[1] - i[1][1])):
            
            return True
    return False#ground_m.overlap(surface,pos)
old = 0
class Player(object):
    def __init__(self,x,y):
        self.image = pygame.image.load("Sprites/Mario/small_m_still.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 0
        self.yv=0
        self.slide = False
        self.Onslope = False
    def update(self):
        global slope,scroll,old

        #print(scroll)
        
        scroll[0] += (self.rect.x-scroll[0]-300)/5
        scroll[1] += (self.rect.bottom-scroll[1]-300)/5

        
        key = pygame.key.get_pressed()

        if key[pygame.K_c]:
            self.rect.x -= 10
        if key[pygame.K_RIGHT]:
            self.speed+=2
            self.rect.y-=slope
        if key[pygame.K_LEFT]:
            self.speed-=2

        if abs(self.speed) > 15:
            self.speed = abs(self.speed)/self.speed*15

        self.speed *= 0.7

        self.rect.y += 2 #잠깐 아래로 내려서 땅에 닿았는지 확인(이거 안하면 정확히 측정안되고 true false 번갈아서 미친듯이 나온다)
        self.Onslope = False
        if LevelCollide(self.mask,(self.rect.x,self.rect.y)):
            
            self.Onslope = True
        else:
            self.Onslope = False
            
        self.rect.y -= 2
        if not self.Onslope:#else:
            self.yv+=1
        
        self.rect.x += self.speed

        
        
##        slope = 0
##        
##        self.ray1 = 0
##        self.ray2 = 0
##        for i in range(50):
##            if LevelCollide(DOT,(self.rect.left,self.rect.bottom-i)):
##                self.ray1 = i
##                
##            pygame.draw.rect(screen,(255,0,0),(self.rect.left,self.rect.bottom+i,1,1))
##        for i in range(50):
##            if LevelCollide(DOT,(self.rect.right,self.rect.bottom-i)):
##                self.ray2 = i
##            pygame.draw.rect(screen,(255,0,0),(self.rect.right,self.rect.bottom+i,1,1))
##
##        print(self.ray1,self.ray2)
##        if self.ray1 == 49 or self.ray2 == 49:
##            self.ray1=0
##            self.ray2=0
##        slope = (self.ray2 - self.ray1)/(self.rect.width)
        
        k = 0
##        oldpos = (self.rect.x, self.rect.y)
        #print(self.yv,self.Onslope)
        if self.Onslope:
            for i in range(8):
                if LevelCollide(self.mask,(self.rect.x,self.rect.y)):
                    break
                self.rect.y+=1
                k += 1
       # print(k)

##        if k == 8:
##            self.rect.x, self.rect.y = oldpos


        add=0
        for i in range(8):
            if LevelCollide(self.mask,(self.rect.x,self.rect.y)):
                self.rect.y-=1
                add+=1
            else:
                break
        
                    
    
        if LevelCollide(self.mask,(self.rect.x,self.rect.y)):
            self.rect.y += add
            for i in range(math.ceil(abs(self.speed))): #밀어내 버리기
                if LevelCollide(self.mask,(self.rect.x,self.rect.y)):
                    self.rect.x+=abs(self.speed)/self.speed*-1
                    

                else:
                    self.speed = 0
                    break
            
        
        
        if self.yv > 15:
            self.yv = 15
        
            
        self.rect.y+=self.yv

        
        if key[pygame.K_DOWN]:
            self.slide = True

        
        if LevelCollide(self.mask,(self.rect.x,self.rect.y)):
            for i in range(math.ceil(abs(self.yv))): #밀어내 버리기
                if LevelCollide(self.mask,(self.rect.x,self.rect.y)):
                    self.rect.y+=abs(self.yv)/self.yv*-1
                        
##            if self.yv == 0:
##                self.yv = 1
##            if key[pygame.K_UP] and abs(self.yv)/self.yv == 1:
##                self.yv=-10
##                self.Onslope = False
##                self.slide = False
##            else:
##                if self.slide:
##                    self.speed=-self.yv
##                else:
##                    self.yv=0
        if self.Onslope:
            self.yv = 0
        if self.Onslope and key[pygame.K_UP]:
            self.yv = -15
        
        
        
        

        if self.slide:
            self.yv+=0.7
            

        
                    
                


        

mario = Player(4500,0)
CLOCK = pygame.time.Clock()
while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #screen.blit(ground,(0,0))
    draw(screen)
    mario.update()
    pygame.draw.rect(screen,(0,0,0),(mario.rect.x - scroll[0] , mario.rect.y - scroll[1] ,mario.rect.width,mario.rect.height))
    pygame.display.update()
    CLOCK.tick(60)

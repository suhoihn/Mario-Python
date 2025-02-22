#Just like an RPG
#Tile -> (16,16)
import pygame,sys
import Map_Split_Code_for_RPG as RPGtool
pygame.init()
screen=pygame.display.set_mode((640,480)) # -> 40 30 tiles per screen
print("initializing... Please wait")
Tiles=[]
Map=[]
Map_s="""00000000000000000000000001111111111111111100000000000000000000000000
         00000000000000000000000001000000000000000100000000000000000000000000
         00000000000000000000011111000000010000000111110000000000000000000000
         00000000000000000000010001000000111000000100010000000000000000000000
         00000000000000000000010100000000010000000001010000000000000000000000
         00000000000000000000000001000111000111000100000000000000000000000000
         000000000000000000000000010001000S0001000100000000000000000000000000
         00000000000000000000000001111111111111111100000000000000000000000000"""
for i in Map_s.split("\n"):
    Temp=[]
    for j in i:
        Temp.append(j)
    Map.append(Temp)

#print(Map)
Loaded_Maps = RPGtool.Split(Map,10,8)

class Tile(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.rect=pygame.Rect(x,y,64,64)
        Tiles.append(self)
        
class Player(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.dx=0
        self.dy=0
        self.rect=pygame.Rect(x,y,16,16)
        self.scroll=[0,0]
    def move(self,dx,dy):

        self.rect.x+=dx
        self.rect.y+=dy
        for i in Tiles:
            if self.rect.colliderect(i.rect):
                if dx>0:
                    self.rect.right = i.rect.left
                if dx<0:
                    self.rect.left = i.rect.right
                if dy>0:
                    self.rect.bottom = i.rect.top
                if dy<0:
                    self.rect.top = i.rect.bottom
        

    def update(self):
        self.scroll[0] += (self.rect.x-self.scroll[0]-320)/30
        self.scroll[1] += (self.rect.y-self.scroll[1]-240)/30
        

x=0
y=0
for i in Map:
    x=0
    for j in i:
        if j == "S":
            p = Player(x,y)
        elif j == '1':
            Tile(x,y)
        x+=64
    y+=64
CLOCK=pygame.time.Clock()
while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        p.move(-2,0)
    elif key[pygame.K_RIGHT]:
        p.move(2,0)
        
    if key[pygame.K_UP]:
        p.move(0,-2)
    elif key[pygame.K_DOWN]:
        p.move(0,2)
    

        
    for i in Tiles:
        pygame.draw.rect(screen,(0,0,0),(i.x-p.scroll[0],i.y-p.scroll[1],64,64))
    pygame.draw.rect(screen,(255,0,0),(p.rect.x-p.scroll[0],p.rect.y-p.scroll[1],16,16))
    p.update()
    pygame.display.update()
    CLOCK.tick(60)

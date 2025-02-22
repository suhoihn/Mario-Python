import pygame,sys,math
screen = pygame.display.set_mode((640,480))
MapImage = pygame.transform.scale(pygame.image.load("모양 1.png"),(640,480))
Map = pygame.mask.from_surface(MapImage)
def ColMap(mask,pos):
    return Map.overlap(mask,pos)

class Player:
    def __init__(self,x,y):
        self.image = pygame.image.load("Sprites/Mario/small_m_still.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mask = pygame.mask.from_surface(self.image)
        self.xv = 0
        self.yv=0


    def loop(self):
        key = pygame.key.get_pressed()
        if not ColMap(self.mask,(self.rect.x,self.rect.y)):
            self.yv+=1
        else:
            self.yv=0
            
            if key[pygame.K_UP]:
                self.yv-=10
        self.rect.x+=self.xv
        print(self.xv) 
        for i in range(math.ceil(abs(self.xv))):
            if ColMap(self.mask,(self.rect.x,self.rect.y)):
                self.rect.x+=abs(self.xv)/self.xv
        
        for i in range(math.ceil(abs(self.yv))):
            if not ColMap(self.mask,(self.rect.x,self.rect.y)):
                self.rect.y+=abs(self.yv)/self.yv
##            else:
##                self.rect.y-=abs(self.yv)/self.yv

        if key[pygame.K_LEFT]:
            self.xv-=0.1
            
        if key[pygame.K_RIGHT]:
            self.xv+=0.1

            
        
            


player = Player(0,0)
CLOCK = pygame.time.Clock()
while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.draw.rect(screen,(0,0,0),player.rect)
    player.loop()
    screen.blit(MapImage,(0,0))
    pygame.display.update()
    CLOCK.tick(60)

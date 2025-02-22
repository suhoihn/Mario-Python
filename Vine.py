import pygame,Block,Globals
Vines = []
class Head:
    def __init__(self,Box):
        self.x = Box.rect.x
        self.y = Box.rect.y
        self.Box = Box

        self.images = [pygame.transform.scale(pygame.image.load("Sprites/Vine/vine3.png"),(32,32)).convert_alpha(),
                       pygame.transform.scale(pygame.image.load("Sprites/Vine/vine4.png"),(32,32)).convert_alpha()]
    
        self.image = self.images[0]    
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.grow = True

        self.MotionIdx = 0
        self.ImageIdx = 0

        self.PartitionIdx = 0

        self.Partitions = 0

        Vines.append(self)

    def Physics(self,Ground):
        self.MotionIdx += 1
        self.PartitionIdx += 1
        self.rect.y -= 4
        self.rect.height += 4
        for i in Block.Blocks:
            if i.rect.colliderect(pygame.Rect(self.rect.topleft,(32,32))) and self.PartitionIdx > 16:
                self.grow = False#이거 코인한테 처맞아도 사라짐
                
        if self.MotionIdx % 8 == 0:
            self.image = self.images[0]
        if self.MotionIdx % 8 == 4:
            self.image = self.images[1]

        if self.PartitionIdx % 8 == 0: # 16이 될 때마다 32만큼 움직였으므로
            self.Partitions += 1

        if self.Partitions >= 128: self.grow = False

        
#메모리 차원에서 없앰               
##    class Vine:
##        def __init__(self,x,y,Head):
##            self.idx = (Head.PartitionIdx // 16) % 2        
##            self.rect = pygame.Rect(x,y,32,32)
##            Head.Partitions.append(self)

            
VineStemImg = [pygame.transform.scale(pygame.image.load("Sprites/Vine/vine1.png"),(32,32)).convert_alpha(),
               pygame.transform.scale(pygame.image.load("Sprites/Vine/vine2.png"),(32,32)).convert_alpha()]
               
def loop(screen,mario,Ground):
    for i in Vines:
        for j in range(i.Partitions):
            if True:#Globals.IsRectOnScreen(j.rect,mario):
                screen.blit(VineStemImg[j % 2],(i.rect.x - mario.scroll[0],i.y - j * 32 - 32 - mario.scroll[1]))
        if Globals.IsRectOnScreen(i.rect,mario):
            if i.grow:
                i.Physics(Ground)      
                screen.blit(i.image,(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))

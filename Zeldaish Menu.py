import pygame,sys
pygame.init()
screen=pygame.display.set_mode((640,480))

h=0
CLOCK=pygame.time.Clock()
img=pygame.image.load("Sprites/Old/SMW1.png")
while True:
    Frame = pygame.Surface((400,h))
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if h<300:
        h+=5

    Frame.blit(img,(150,200))
    
    screen.blit(Frame,(120,80))
    pygame.display.update()
    CLOCK.tick(60)

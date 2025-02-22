import pygame,sys,math
pygame.init()
screen = pygame.display.set_mode((640,480))
player = pygame.Rect(0,0,50,50)
xv=0
yv=0
speed = 5
friction = 0.7
slope = 0
#level = [pygame.Rect(0,380,640,100),pygame.Rect(200,330,40,50)]
CLOCK = pygame.time.Clock()
img = pygame.transform.scale(pygame.image.load("./모양 1.png").convert_alpha(),(640,480))
player_img = pygame.transform.scale(pygame.image.load("Sprites/Mario/small_m_still.png").convert_alpha(),(28,40))
player_mask=pygame.mask.from_surface(player_img)
player = player_img.get_rect()
level = pygame.mask.from_surface(img)
def collevel(rect):
    return level.overlap(player_mask,(player.x,player.y))

while True:
    screen.fill((255,255,255))
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    if key[pygame.K_RIGHT]:
        xv += speed
    elif key[pygame.K_LEFT]:
        xv -= speed

    xv *= friction
    player.x += xv
    if collevel(player):
        slope = 0
        while slope < 8:# or not collevel(player):
            slope +=1
            player.y-=1
        if collevel(player):
            player.y += slope
            for k in range(math.ceil(abs(xv))):
                if collevel(player):
                    player.x += abs(xv)/xv*-1
            xv=0
    player.y+=yv
    if collevel(player):
        for k in range(math.ceil(abs(yv))):
            if collevel(player):
                player.y += abs(yv)/yv*-1
        if key[pygame.K_UP] and abs(yv)/yv==1 :
            yv=-20
        else:
            yv=0
    else:
        yv+=1
                    

##    for i in level:
##        pygame.draw.rect(screen,(0,0,0),i)
    screen.blit(img,(0,0))
    pygame.draw.rect(screen,(255,0,0),player)
    pygame.display.update()
    CLOCK.tick(30)

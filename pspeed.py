#Pswitch timer practice
import pygame,sys
screen = pygame.display.set_mode((640,480))
#지금 s를 누른 상태라고 가정하고... -> 땅에 있고, 풀 스피드이면... p speed에 도달한다 이말이여
#점프하고 128 프레임 후에 pspeed 초기화
#8프레임 마다 pmeter증가(max 48)
pmeterseg = 0
timer = 0
CLOCK = pygame.time.Clock()
while True:
    screen.fill((0,0,0))
    timer += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pass
    print(pmeterseg)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
        if pmeterseg < 6 and timer % 8 == 0:
            pmeterseg += 1
    else:
        if timer % 24 == 0 and pmeterseg > 0:
            pmeterseg -= 1
    for i in range(6):
        if i < pmeterseg:pygame.draw.polygon(screen,(255,0,0),((120 + 20 * i,310),(100 + 20 * i,320),(100 + 20 * i,300)))
        else: pygame.draw.polygon(screen,(255,255,255),((120 + 20 * i,310),(100 + 20 * i,320),(100 + 20 * i,300)))
    pygame.display.update()
    CLOCK.tick(60)

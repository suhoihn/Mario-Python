#Slope test 3
import pygame,sys
pygame.init()
screen=pygame.display.set_mode((640,480))
d1=(500,400)
d2=(100,100)

px=100

player = pygame.Rect(0,0,50,50)
xv=0
yv=0
Onslope = False
SlippingDown=False

def f(x):
    y = (d2[1]-d1[1])/(d2[0]-d1[0])*(x-d1[0])+d1[1]
    return y

deg = (d1[1]-d2[1])/(d1[0]-d2[0])
yvalue=f(0)

CLOCK = pygame.time.Clock()
while True:
    screen.fill((255,255,255))
    key = pygame.key.get_pressed() 
    yv += 0.5
    if player.bottomright[1] >= f(player.bottomright[0]) and min(d1[0],d2[0]) <= player.bottomright[0] <= max(d1[0],d2[0]): #플레이어의 오른쪽 아래 y좌표가 f(x) 그래프 안에 포함되어있는가? / 플레이어의 x좌표 값이 범위내에 있는가?
        Onslope=True
    print(xv)
        
    if key[pygame.K_UP] and Onslope:
        yv=-10
        Onslope=False
        SlippingDown=False
    if key[pygame.K_DOWN] and Onslope:
        SlippingDown = True

    if SlippingDown:
        xv += 0.2
    else:
        xv = 0

    if xv>10:xv=10
    if yv>10:yv=10
        
    if Onslope:
        if not SlippingDown:
            if key[pygame.K_LEFT]:
                player.bottomright = (player.bottomright[0]-2,f(player.bottomright[0]))
            if key[pygame.K_RIGHT]:
                player.bottomright = (player.bottomright[0]+2,f(player.bottomright[0]))
        else:
            player.bottomright = (player.bottomright[0]-xv,f(player.bottomright[0]))
        yv=0
    else:   
        player.y += yv
        if not SlippingDown:
            if key[pygame.K_LEFT]:
                player.x -= 2
            if key[pygame.K_RIGHT]:
                player.x += 2
        else:
            player.bottomright = (player.bottomright[0]-xv,f(player.bottomright[0]))
            
            
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.draw.rect(screen,(0,0,0),player)
    pygame.draw.line(screen,(0,0,0),d1,d2)
    
    pygame.display.update()
    CLOCK.tick(60)

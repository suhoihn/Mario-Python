import pygame,sys
from math import *
pi = 3.14
screen = pygame.display.set_mode((1280,480))
class Player:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,10,10)
        self.angle = 1
        self.dx = cos(self.angle) * 5
        self.dy = sin(self.angle) * 5

p = Player(320,240)
CLOCK = pygame.time.Clock()

mapX,mapY,mapS = 8,8,64
Map =[1,1,1,1,1,1,1,1,
      1,0,1,0,0,0,0,1,
      1,0,1,0,0,0,0,1,
      1,0,1,0,0,0,0,1,
      1,0,0,0,0,0,0,1,
      1,0,1,0,1,1,0,1,
      1,0,0,0,0,0,0,1,
      1,1,1,1,1,1,1,1
    ]
def dist(ax,ay,bx,by,ang):
    return sqrt((bx - ax) ** 2 + (by - ay) ** 2)
def DrawRays3D(p):
    ra = p.angle#ra : Ray Angle
    rx,ry = 0,0
    xo,yo = 0,0
    mx,my,mp = 0,0,0
    distH,hx,hy = 1000000,p.rect.x,p.rect.y
    for r in range(1):
        dof = 0
        aTan = -1 / tan(ra)
##        aTan = min(10,aTan)
##        aTan = max(-10,aTan)
        if ra > pi:
            ry = ((int(p.rect.y) >> 6) << 6) - 0.0001
            rx = (p.rect.y - ry) * aTan + p.rect.x
            yo = -64
            xo = -yo * aTan
        if ra < pi:
            ry = ((int(p.rect.y) >> 6) << 6) + 64
            rx = (p.rect.y - ry) * aTan + p.rect.x
            yo = 64
            xo = -yo * aTan
        if abs(ra) < 0.001  or abs(ra - pi) < 0.001 :
            rx = p.rect.x
            ry = p.rect.y
            dof = 8
        while (dof < 8):
          
            mx = int(rx) >> 6
            my = int(ry) >> 6 
            mp = my * mapX + mx
            if mp > 0 and mp < mapX * mapY and Map[mp] == 1:
                hx = rx
                hy = ry
                distH = dist(p.rect.x,p.rect.y,hx,hy,ra)
                dof = 8
                
            else:
                rx += xo
                ry += yo
                dof += 1

        
        dof = 0
        distV,vx,vy = 1000000,p.rect.x,p.rect.y
        nTan = -tan(ra)
##        nTan = min(10,nTan)
##        nTan = max(-10,nTan)
        if pi / 2 < ra  and ra < pi/ 2 * 3 :
            rx = ((int(p.rect.x) >> 6) << 6) - 0.0001
            ry = (p.rect.x - rx) * nTan + p.rect.y
            xo = -64
            yo = -xo * nTan
        if ra < pi / 2 or ra > pi / 2 * 3:
            rx = ((int(p.rect.x) >> 6) << 6) + 64
            ry = (p.rect.x - rx) * nTan + p.rect.y
            xo = 64
            yo = -xo * nTan
        if abs(ra) < 0.001 or abs(ra - pi) < 0.001 :
            rx = p.rect.x
            ry = p.rect.y
            dof = 8
        while (dof < 8):
            mx = int(rx) >> 6
            my = int(ry) >> 6 
            
            mp = my * mapX + mx
            if mp > 0 and mp < mapX * mapY and Map[mp] == 1:
                dof = 8
                vx = rx
                vy = ry
                distV = dist(p.rect.x,p.rect.y,vx,vy,ra)

    
            else:
                rx += xo
                ry += yo
                dof += 1
        if distV < distH:
            rx = vx
            ry = vy
        if distH < distV:
            rx = hx
            ry = hy
        

        pygame.draw.line(screen,(0,255,0),p.rect.center,(rx,ry),5)
def DrawMap():
    for y in range(mapY):
        for x in range(mapX):
          if Map[y * mapX + x] == 1:
              pygame.draw.rect(screen,(255,255,255),(x * mapS,y * mapS,mapS,mapS))
while True:
    screen.fill((192,192,192))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        p.angle -= 0.1
        if p.angle < 0: p.angle += 2 * pi;
        p.dx = cos(p.angle) * 5; p.dy = sin(p.angle) * 5
    if key[pygame.K_RIGHT]:
        p.angle += 0.1
        if p.angle > 2 * pi: p.angle -= 2 * pi;
        p.dx = cos(p.angle) * 5; p.dy = sin(p.angle) * 5
    if key[pygame.K_UP]:
        p.rect.x += p.dx
        p.rect.y += p.dy
    if key[pygame.K_DOWN]:
        p.rect.x -= p.dx
        p.rect.y -= p.dy
    DrawRays3D(p)
    DrawMap()
    pygame.draw.rect(screen,(0,255,255),p.rect)
    pygame.draw.line(screen,(255,0,0),p.rect.center,(p.rect.centerx + p.dx * 5, p.rect.centery + p.dy * 5))
    pygame.display.update()
    CLOCK.tick(60)

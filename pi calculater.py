import pygame,sys,random
screen = pygame.display.set_mode((640,480))
incircle = 0
points = []
def dist(p1,p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
a = 0
while True:
    #screen.fill((0,0,0))
    a += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(len(points),incircle,incircle / len(points) * 4)
    #pygame.draw.rect(screen,(255,255,255),(160,80,320,320))
    #pygame.draw.circle(screen,(0,0,0),(320,240),160)
    if a <= 320 * 320:
        point = (160 + a % 320, 80 + (a // 320))
    #if not point in points:
        points.append(point)
        if dist((320,240),point) < 160:
            incircle += 1
##    for i in points:
##        pygame.draw.rect(screen,(255,0,0),(*i,1,1))
    #print(incircle / len(points) * 4)
    #pygame.display.update()
##    if 3.141591 < incircle / len(points) * 4 < 3.141593 or len(points) == 320 * 320:
##        print(incircle / len(points) * 4)

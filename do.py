import pygame,time
#screen = pygame.display.set_mode((640,480))
a = 0
for i in range(640):
    a += - (a + 7) /4
    print(a)
    time.sleep(0.1)
    #pygame.draw.line(screen,(255,255,255),(i,a[i] + 1000),(i,a[i] + 1000),5)


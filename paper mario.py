#Paper Mario
import pygame,sys
screen = pygame.display.set_mode((640,480))
og_img = pygame.image.load("Sprites/Mario/small_m_still.png")
ogw = og_img.get_width()
ogh = og_img.get_height()
Temp = False
img = og_img
heading = -1
idx = 0
CLOCK = pygame.time.Clock()
turnspd = 16
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if heading != -1:
                    Temp = True
                    Target = -1
                    idx = 2
            elif event.key == pygame.K_RIGHT:
                if heading != 1:
                    Temp = True
                    Target = 1
                    idx = 2
    if Temp:
        if idx == int(turnspd / 2):
            heading = Target

        if idx < turnspd:
            img = pygame.transform.scale(og_img,(int(ogw / (turnspd / 2) ** 2 * (idx - turnspd / 2) ** 2),ogh))
            idx += 1

        else:
            img = og_img
            idx = 0
            Temp = False

    k = ogw - img.get_width()
    screen.blit(pygame.transform.flip(img,heading == -1,False),(320 + k / 2,240))
    pygame.display.update()
    CLOCK.tick(60)

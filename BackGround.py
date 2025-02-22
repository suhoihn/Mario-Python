import pygame,os,Globals
from Globals import SW,SH
BackGrounds = []
class BackGround:
    def __init__(self,idx,theme = None):
        self.idx = idx
        file_list = os.listdir("./Pictures/BackGround/")
        self.images = []
        self.angry = False
##        for i in file_list:
##            if i != "desktop.ini":
##                self.images.append(pygame.transform.scale(pygame.image.load("Pictures/BackGround/"+i),(960,720)).convert_alpha())
        if theme == None:
            self.image = pygame.transform.scale(pygame.image.load("Pictures/BackGround/yoshiisland.gif").convert_alpha(),(SW,SH))
            Globals.BGM = "BGM/Overworld Theme.mp3"
        elif theme == "Athletic":
            Globals.BGM = "BGM/Athletic Theme.mp3"
            self.image = pygame.transform.scale(pygame.image.load("Pictures/BackGround/athletic.png").convert_alpha(),(SW,SH))

        elif theme == "Underground":
            Globals.BGM = "BGM/Super Mario Bros. 3 - Underworld Theme.mp3"
            self.image=pygame.transform.scale(pygame.image.load("Pictures/BackGround/BG3.png").convert_alpha(),(SW,SH))
        elif theme == "Underwater":
            Globals.BGM = "BGM/SNES Super Mario Bros. Theme.mp3"
            self.image=pygame.transform.scale(pygame.image.load("Pictures/BackGround/06907ae2f7211be479320792e44bc7a3.gif").convert_alpha(),(SW,SH))
        elif theme == "Night":
            Globals.BGM = "BGM/Bonus Screen - Super Mario World.mp3"#Sky Theme (Night) - Super Mario World - Super Mario Maker 2 Soundtrack.mp3"
            self.image = pygame.transform.scale(pygame.image.load("Pictures/BackGround/night.gif").convert_alpha(),(SW,SH))
        elif theme == "Castle":
            Globals.BGM = "BGM/Bowser's Castle (Second Time) - Super Mario RPG Legend of the Seven Stars Music Extended.mp3"
            self.image = pygame.transform.scale(pygame.image.load("Pictures/BackGround/Castle.jpeg").convert_alpha(),(SW,SH))

        self.width = self.image.get_width()
        if len(BackGrounds) == 0:
            BackGrounds.append(self)




idx=0
def loop(screen,mario):
    ScrollSpd = 2
    m = (-mario.scroll[0] / ScrollSpd) % (SW * 2) - SW#-SW안하면 왼쪽이 텅 빔(m의 값은 -SW부터 SW까지 다 커버됨 -> 화면을 완전히 매꿀 수 있음)
    n = (SW - mario.scroll[0] / ScrollSpd) % (SW * 2) - SW

    k = BackGrounds[0].image#bgs[(globals.GlobalTimer) // 100 % 4]
    screen.blit(k,(m,0))
    screen.blit(k,(n,0))

##    global idx
##    for i in BackGrounds:
##        if i.angry:
##           
##            idx+=0.001 *100
##            idx%=len(i.images)
##            i.image = i.images[int(idx)]
##        else:
##            pass#i.image = a
##        if -i.width <= i.width * i.idx - mario.scroll[0] / 2 <= 640:
##            screen.blit(i.image,(i.width*i.idx-mario.scroll[0]/2,0))

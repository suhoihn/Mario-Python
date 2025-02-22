#Auto Ground Generator
import pygame,sys
pygame.init()
screen = pygame.display.set_mode((1280,960))
Level = """00000000000000000000000000000000000000000
           00000000000000000000000000000000000000000
           00000000000001111111111110000000000000000
           00000001100000000000000000000000000000000
           00000011110000000000000000000000000000000
           00111111111110000000000000000000000000000
           00000000000000000000000000000000000000000
           00000000000000000000000000000000000000000"""


Slevel = Level.split("\n")
print(Slevel)
Ground = []
a = []
TM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top_middle.png")),(32,32))
TL=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top_left.png")),(32,32))
TR=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top_right.png")),(32,32))
LM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_left_middle.png")),(32,32))
MM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_middle_middle.png")),(32,32))
RM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_right_middle.png")),(32,32))
BM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_bottom_middle.png")),(32,32))
BL=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_bottom_left.png")),(32,32))
BR=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_bottom_right.png")),(32,32))
L=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_left.png")),(32,32))
M=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_middle.png")),(32,32))
R=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_right.png")),(32,32))
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    for i in range(len(Slevel)):
        for j in range(len(Slevel[i])):
            if Slevel[i][j] == "1":# and 0 < i < len(Slevel) - 1 and 0 < j < len(Slevel[i]) - 1 :
                
                
                try :
                    CheckList = {"LeftTop" : Slevel[i - 1][j - 1] == "1",
                                 "Left" : Slevel[i][j - 1] == "1",
                                 "LeftBottom" : Slevel[i + 1][j - 1] == "1",
                                 "Top" : Slevel[i - 1][j] == "1",
                                 "Bottom" : Slevel[i + 1][j] == "1",
                                 "RightTop" : Slevel[i - 1][j + 1] == "1",
                                 "Right" : Slevel[i][j + 1] == "1",
                                 "RightBottom" : Slevel[i + 1][j + 1] == "1"}
                except:
                    pass
                
                if CheckList['Left'] and CheckList['Right'] and CheckList['Bottom'] and CheckList['Top']:
                    screen.blit(MM,(j * 32,i * 32))

                
                if CheckList['Left'] and CheckList['Right'] and CheckList['Bottom'] and not CheckList['Top']:
                    screen.blit(TM,(j * 32,i * 32))
                    
                if CheckList['Left'] and CheckList['Right'] and not CheckList['Bottom'] and CheckList['Top']:
                    screen.blit(BM,(j * 32,i * 32))
                    
                if CheckList['Left'] and not CheckList['Right'] and CheckList['Bottom'] and CheckList['Top']:
                    screen.blit(RM,(j * 32,i * 32))
                    
                if not CheckList['Left'] and CheckList['Right'] and CheckList['Bottom'] and CheckList['Top']:
                    screen.blit(LM,(j * 32,i * 32))

                
                if not CheckList['Left'] and CheckList['Right'] and CheckList['Bottom'] and not CheckList['Top']:
                    screen.blit(TL,(j * 32,i * 32))
                    
                if CheckList['Left'] and not CheckList['Right'] and CheckList['Bottom'] and not CheckList['Top']:
                    screen.blit(TR,(j * 32,i * 32))
                    
                if not CheckList['Left'] and CheckList['Right'] and not CheckList['Bottom'] and CheckList['Top']:
                    screen.blit(BL,(j * 32,i * 32))
                    
                if CheckList['Left'] and not CheckList['Right'] and not CheckList['Bottom'] and CheckList['Top']:
                    screen.blit(BR,(j * 32,i * 32))
                    
                    
                if not CheckList['Left'] and CheckList['Right'] and not CheckList['Bottom'] and not CheckList['Top']:
                    screen.blit(L,(j * 32,i * 32))
                    
                if CheckList['Left'] and not CheckList['Right'] and not CheckList['Bottom'] and not CheckList['Top']:
                    screen.blit(R,(j * 32,i * 32))
                    
                if CheckList['Left'] and CheckList['Right'] and not CheckList['Bottom'] and not CheckList['Top']:
                    screen.blit(M,(j * 32,i * 32))


                if not CheckList['Left'] and not CheckList['Right'] and not CheckList['Bottom'] and not CheckList['Top']:
                   pass #ENTIRE # screen.blit(R,(j * 32,i * 32))
                 
                    
                    
                

    pygame.display.update()
            
            

import pygame,random,Goal
#from ROM import Map
import math
import Globals
pygame.display.init()

#============================
MainTileImg = pygame.image.load("Sprites/Ground/tileset.png").convert_alpha()
w,h = MainTileImg.get_width(), MainTileImg.get_height()

AllTiles = []
crop_region = [0,0,16,16]
for y in range(h // 16):
    for x in range(w // 16):
        newsurf = pygame.Surface((16,16))
        newsurf.fill((69,69,69))
        newsurf.set_colorkey((69,69,69))
        newsurf.blit(MainTileImg,(0,0),(x * 16,y * 16,16,16))
        AllTiles.append(pygame.transform.scale(newsurf,(32,32)))
##import sys
##print(sys.getsizeof(AllTiles))

#print(loadCSV("Sprites/Ground/test map.csv"))
#============================

class Slope:
    def __init__(self,x,y,heading,ceiling = False,image = None):
        self.rect = pygame.Rect(0,0,0,0)
        self.rect.x = x
        self.rect.y = y
        if heading == "NE":#대각선 위로 //왼쪽위
            self.image = SS
            self.angle = 45
        elif heading == "NW":#대각선 위로(역방향)
            self.image = SSF
            self.angle = 45 + 180
        elif heading == "ENE1":#대각선 반 위로 - 1
            self.image = GSP1
            self.angle = 30
            self.rect.y += 16
        elif heading == "ENE2":#대각선 반 위로 - 2
            self.image = GSP2
            self.angle = 30
        elif heading == "WNW1":#대각선 반 위로(역방향) - 1
            self.image = pygame.transform.flip(GSP1,True,False) #Gentle Slope Part 1 Flipped / GSP!F
            self.angle = 30 + 180
            self.rect.y += 16
        elif heading == "WNW2":#대각선 반 위로(역방향) - 2
            self.image = pygame.transform.flip(GSP2,True,False) #Gentle Slope Part 2 Flipped / GSP2F
            self.angle = 30 + 180

        #이 아래는 천장 취급
        elif heading == "SE":#대각선 아래
            self.angle = 45
            self.image = pygame.transform.flip(SS,False,True)

        elif heading == "SW":#대각선 아래(역방향)
            self.angle = 45 + 180
            self.image = pygame.transform.flip(SS,True,True)

##        elif heading == "ESE1":#대각선 반 아래로 - 1
##            pass
##        elif heading == "ESE2":#대각선 반 아래로 - 2
##            pass
##        elif heading == "WSW1":#대각선 반 아래로(역방향) - 1
##            pass
##        elif heading == "WSW2":#대각선 반 아래로(역방향) - 1
##            pass
##

        if image != None:
            self.image = image
            self.angle = 45
            
        self.ceiling = ceiling
        
        self.rect.width, self.rect.height = self.image.get_width(), self.image.get_height()#30s
                    
        self.heading = heading

        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

class Water:
    def __init__(self,x,y,IsSurface):
        self.x = x
        self.y = y
        self.IsSurface = IsSurface
        self.rect = pygame.Rect(x,y,32,32)

#내가 있는 타일 바로 옆 5칸 정도만 for문으로 돌려야 렉이 줄어듦(다른 것도 마찬가지)
#Map = ROM.Map

##global game_map,rangeX,rangeY,icy
def snow(m):
    for i in range(m.get_height()):
        for j in range(m.get_width()):
            if m.get_at((j,i)) == (0,0,0):
                m.set_at((j,i),(120,119,168))
                
            elif m.get_at((j,i)) == (0,200,0):
                m.set_at((j,i),(233,233,247))
                
            elif m.get_at((j,i)) == (0,120,72):
                m.set_at((j,i),(201,200,247))
                
            elif m.get_at((j,i)) == (120,104,24):
                m.set_at((j,i),(170,169,217))
                
            elif m.get_at((j,i)) == (200,152,88):
                m.set_at((j,i),(184,183,232))
                
            elif m.get_at((j,i)) == (224,192,80):
                m.set_at((j,i),(216,215,247))
    return m
def normal(m):
    for i in range(m.get_height()):
        for j in range(m.get_width()):
            if m.get_at((j,i)) == (120,119,168):
                m.set_at((j,i),(0,0,0))
                
            elif m.get_at((j,i)) == (233,233,247):
                m.set_at((j,i),(0,200,0))
                
            elif m.get_at((j,i)) == (201,200,247):
                m.set_at((j,i),(0,120,72))
                
            elif m.get_at((j,i)) == (170,169,217):
                m.set_at((j,i),(120,104,24))
                
            elif m.get_at((j,i)) == (184,183,232):
                m.set_at((j,i),(200,152,88))
                
            elif m.get_at((j,i)) == (216,215,247):
                m.set_at((j,i),(224,192,80))
#import sys
def initialize(Map):
    global game_map,rangeX,rangeY,icy,Waters,water_map
    game_map = []
    water_map = []
    for row in Map.split("\n"):
        if row == '':continue
        game_map.append(list(row))
        water_map.append(['0'] * len(row))
   #print(sys.getsizeof(water_map))
    for i in allstars:
        
        if Globals.SnowTheme:
            i = snow(i)
        else:
            i = normal(i)
    Grounds=[]
    Waters = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == 'G':
                Goal.Goal(x*32,y*32,True)
            elif tile == "g":
                Goal.Goal(x*32,y*32,False)
            elif tile == "c":
                Goal.CheckPoint(x * 32, y * 32)
            elif tile == "W" or tile == "w":
                if (y - 1) >= 0:IsSurface = game_map[y - 1][x] == '0'
                else: IsSurface = True
                    
                if IsSurface: add = "W"
                else: add = "w"
                
                if x - 1 >= 9 and (game_map[y][x - 1] in ["(",")","{","[","]","}","+","-"]):
                    water_map[y][x - 1] = add #Waters.append(Water((x - 1) * 32,y * 32,game_map[y - 1][x] == '0'))
                if x + 1 < len(game_map[y]) and (game_map[y][x + 1] in ["(",")","{","[","]","}","+","-"]):
                    water_map[y][x + 1] = add #Waters.append(Water((x + 1) * 32,y * 32,game_map[y - 1][x] == '0'))
                if (y - 1) >= 0: water_map[y][x] = add#Waters.append(Water(x * 32,y * 32,game_map[y - 1][x] == '0'))

            x += 1
        y += 1

    rangeX = [0,min([len(i) for i in game_map])]
    rangeY = [0,len(game_map)]
    Globals.rangeY = rangeY
SlopeTileNo = [112,113,114,115,164,165,117,118,119,120,171,172,895,900,324,325,376,327,328,380]
NonSolidTileNo = [158,525]

def loadCSV(filename):
    tileset = []
    game_map = []
    with open(filename,"r") as f:
        for line in f.readlines():
            line.replace("\n","")
            temp = []
            temp2 = []
            for tile in line.split(","):
                if tile == "-1" or int(tile) in NonSolidTileNo:
                    temp.append(-1)
                elif int(tile) in SlopeTileNo:
                    temp.append(int(tile))
                else:
                    temp.append(1)
                    
                temp2.append(int(tile))
            game_map.append(temp)
            tileset.append(temp2)
        f.close()
    return tileset,game_map

TM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top_middle.png")),(32,32)).convert_alpha()
TL=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top_left.png")),(32,32)).convert_alpha()
TR=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top_right.png")),(32,32)).convert_alpha()
LM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_left_middle.png")),(32,32)).convert_alpha()
MM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_middle_middle.png")),(32,32)).convert_alpha()
RM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_right_middle.png")),(32,32)).convert_alpha()
BM=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_bottom_middle.png")),(32,32)).convert_alpha()
BL=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_bottom_left.png")),(32,32)).convert_alpha()
BR=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_bottom_right.png")),(32,32)).convert_alpha()
L=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_left.png")),(32,32)).convert_alpha()
MH=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_middleH.png")),(32,32)).convert_alpha()
MV=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_middleV.png")),(32,32)).convert_alpha()
R=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_right.png")),(32,32)).convert_alpha()
B=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_bottom.png")),(32,32)).convert_alpha()
T=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_top.png")),(32,32)).convert_alpha()
A=pygame.transform.scale((pygame.image.load("Sprites/Ground/ground_all.png")),(32,32)).convert_alpha()

SS=pygame.transform.scale((pygame.image.load("Sprites/Ground/slope.png")),(32,32)).convert_alpha() #Steep Slope
SSF=pygame.transform.flip(SS,True,False) #Steep Slope Flipped
GSP1 = pygame.transform.scale((pygame.image.load("Sprites/Ground/slope2.png")),(32,16)).convert_alpha()#Gentle Slope Part 1
GSP2 = pygame.transform.scale((pygame.image.load("Sprites/Ground/slope3.png")),(32,32)).convert_alpha()#Gentle Slope Part 2

P1 = pygame.transform.scale((pygame.image.load("Sprites/Ground/Particle (1).png")),(32,32)).convert_alpha()
P2 = pygame.transform.scale((pygame.image.load("Sprites/Ground/Particle (2).png")),(32,32)).convert_alpha()
P3 = pygame.transform.scale((pygame.image.load("Sprites/Ground/Particle (3).png")),(32,32)).convert_alpha()
P4 = pygame.transform.scale((pygame.image.load("Sprites/Ground/Particle (4).png")),(32,32)).convert_alpha()
allstars = [TM,TL,TR,LM,MM,RM,BM,BL,BR,L,MH,MV,R,B,T,A,SS,SSF,GSP1,GSP2,P1,P2,P3,P4,A]
a = 0

SlopeData = {
    "(" : pygame.mask.from_surface(SS.convert_alpha()),
    ")" : pygame.mask.from_surface(pygame.transform.flip(SS,True,False).convert_alpha()),
    "{" : pygame.mask.from_surface(GSP1.convert_alpha()),
    "}" : pygame.mask.from_surface(pygame.transform.flip(GSP1,True,False)),
    "[" : pygame.mask.from_surface(GSP2),
    "]" : pygame.mask.from_surface(pygame.transform.flip(GSP2,True,False)),
    "-" : pygame.mask.from_surface(pygame.transform.flip(SS,False,True)),
    "+" : pygame.mask.from_surface(pygame.transform.flip(SS,True,True)),
    }

SlopeAngleData = {
    "(" : 45,
    ")" : 45 + 180,
    "{" : 30,
    "}" : 30 + 180,
    "[" : 30,
    "]" : 30 + 180,
    "+" : 0,
    "-" : 0,
    }


##tilemap,real_game_map = loadCSV("Sprites/Ground/test map..csv")
##rangeX = [0,min([len(i) for i in tilemap])]
##rangeY = [0,len(tilemap)]
##Globals.rangeY = rangeY
def loop(screen,mario):
    global game_map
    mario.rangeX = [(mario.rect.centerx // 32) - 18, (mario.rect.centerx // 32) + 18]#13,13
    mario.rangeY = [(mario.rect.centery // 32) - 13 - 10, (mario.rect.centery // 32) + 9 + 10]#-13,9
    game_map = real_game_map
    Grounds = []
    Slopes = []
    #print(rangeY[1],mario.rangeY[1],min(rangeY[1],mario.rangeY[1]))
    for y in range(max(0,mario.rangeY[0]),min(rangeY[1],mario.rangeY[1])):
        for x in range(max(0,mario.rangeX[0]),min(rangeX[1],mario.rangeX[1])):
            tileno = tilemap[y][x]
            
            if tileno == -1: continue
            if -32 <= x * 32 - mario.scroll[0] <= Globals.SW and -32 <= y * 32 - mario.scroll[1] <= Globals.SH:#화면 내에서만 그림 
                screen.blit(AllTiles[tileno],(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))

                    
            #slope의 경우 이미지 자체를 넘겨줌
            if tileno in SlopeTileNo:
                Slopes.append(Slope(x*32,y*32,"NOTHING",image = AllTiles[tileno]))
                continue
            
##            if not (tileno in [158,525]):
##                Grounds.append(pygame.Rect(x*32,y*32,32,32))
    return Grounds, Slopes, Waters
def loop(screen,mario):
    global sdf,CheckList,rangeX,rangeY,Waters,a
    Grounds = []
    Slopes = []
##  Waters = []
##    for y in range(len(game_map)):
##        for x in range(len(game_map[y])):
##            if x != 0 and y != 0:
##                if x == mario.rect.centerx // 32 and y == mario.rect.centery // 32:
##                
##                    #pygame.draw.rect(screen,(255,255,0),(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1]),32,32))
##                    rangeX = [max(0,x - 13), min(304,x + 13)]#13,13
##                    rangeY = [max(0,y - 13), min(17,y + 9)]#-13,9
##                    break
    mario.rangeX = [(mario.rect.centerx // 32) - 18, (mario.rect.centerx // 32) + 18]#13,13
    mario.rangeY = [(mario.rect.centery // 32) - 13 - 10, (mario.rect.centery // 32) + 9 + 10]#-13,9
##    if Globals.GlobalTimer % 400 == 0:
##        pygame.mixer.Sound("Sounds/기자양반.wav").play() 
##    elif Globals.GlobalTimer % 400 == 60:
##        a = 0
##    elif Globals.GlobalTimer % 400 == 90:
##        a = 1

    for y in range(max(0,mario.rangeY[0]),min(rangeY[1],mario.rangeY[1])):
        for x in range(max(0,mario.rangeX[0]),min(rangeX[1],mario.rangeX[1])):
            #print(y,x,len(game_map),len(game_map[y]))
            tile = game_map[y][x]
            water_tile = water_map[y][x]
            if water_tile == "W":#Surface
                screen.blit(WSs[(Globals.GlobalTimer // 6) % 4],(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
            elif water_tile == "w":
                screen.blit(WSs[-1],(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))

            if tile == "0":
                continue
            else:
                pass
##                if a == 0:
##                    tile = "0"
##                else:
##                    tile = "1"


            
            SP = False
            if -32 <= x * 32 - mario.scroll[0] <= Globals.SW and -32 <= y * 32 - mario.scroll[1] <= Globals.SH:#화면 내에서만 그림 

                #screen.blit(random.choice(allstars),(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                
                if tile == "1":
                    CheckList = {
                        "Left" : False,
                        "Top" : False,
                        "Bottom" : False,
                        "Right" : False}
                    if x == 0:
                        CheckList["Left"] = True
                    else:
                        CheckList["Left"] = game_map[y][x - 1] in ['1','(',')','{','}','[',']','+','-']

                    if y == 0:
                        CheckList["Top"] = True
                    else:
                        CheckList["Top"] = game_map[y - 1][x] in ['1','(',')','{','}','[',']','+','-']

                    if x == rangeX[1] - 1:
                        CheckList["Right"] = True
                    else:
                        CheckList["Right"] = game_map[y][x + 1] in ['1','(',')','{','}','[',']','+','-']

                    if y == rangeY[1] - 1:
                        CheckList["Bottom"] = True
                    else:
                        CheckList["Bottom"] = game_map[y + 1][x] in ['1','(',')','{','}','[',']','+','-']

                        
                    if CheckList['Left'] and CheckList['Right'] and CheckList['Bottom'] and CheckList['Top']:
                        screen.blit(MM,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        SP = True

                        
                    if CheckList['Left'] and CheckList['Right'] and CheckList['Bottom'] and not CheckList['Top']:
                        screen.blit(TM,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                    if CheckList['Left'] and CheckList['Right'] and not CheckList['Bottom'] and CheckList['Top']:
                        screen.blit(BM,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                    if CheckList['Left'] and not CheckList['Right'] and CheckList['Bottom'] and CheckList['Top']:
                        screen.blit(RM,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                    if not CheckList['Left'] and CheckList['Right'] and CheckList['Bottom'] and CheckList['Top']:
                        screen.blit(LM,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))

                    
                    if not CheckList['Left'] and CheckList['Right'] and CheckList['Bottom'] and not CheckList['Top']:
                        screen.blit(TL,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                    if CheckList['Left'] and not CheckList['Right'] and CheckList['Bottom'] and not CheckList['Top']:
                        screen.blit(TR,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                    if not CheckList['Left'] and CheckList['Right'] and not CheckList['Bottom'] and CheckList['Top']:
                        screen.blit(BL,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                    if CheckList['Left'] and not CheckList['Right'] and not CheckList['Bottom'] and CheckList['Top']:
                        screen.blit(BR,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                        
                    if not CheckList['Left'] and CheckList['Right'] and not CheckList['Bottom'] and not CheckList['Top']:
                        screen.blit(L,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                    if CheckList['Left'] and not CheckList['Right'] and not CheckList['Bottom'] and not CheckList['Top']:
                        screen.blit(R,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                        
                    if not CheckList['Left'] and not CheckList['Right'] and CheckList['Bottom'] and not CheckList['Top']:
                        screen.blit(T,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))

                    if not CheckList['Left'] and not CheckList['Right'] and not CheckList['Bottom'] and CheckList['Top']:
                        screen.blit(B,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                    if CheckList['Left'] and CheckList['Right'] and not CheckList['Bottom'] and not CheckList['Top']:
                        screen.blit(MH,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
                        
                    if not CheckList['Left'] and not CheckList['Right'] and CheckList['Bottom'] and CheckList['Top']:
                        screen.blit(MV,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))


                    if not CheckList['Left'] and not CheckList['Right'] and not CheckList['Bottom'] and not CheckList['Top']:
                        screen.blit(A,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1])))
    #pass #ENTIRE # screen.blit(R,(x * 32 - int(mario.scroll[0]),y * 32 - int(mario.scroll[1]))

                elif tile == '(':
                    screen.blit(SS,(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
                elif tile == ')':
                    screen.blit(SSF,(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
                elif tile =='{':
                    screen.blit(GSP1,(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1]) + 16))
                elif tile =='}':
                    screen.blit(pygame.transform.flip(GSP1,True,False),(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1]) + 16))
                elif tile =='[':
                    screen.blit(GSP2,(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
                elif tile ==']':
                    screen.blit(pygame.transform.flip(GSP2,True,False),(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
                elif tile =='q':
                    screen.blit(P1,(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
##                elif tile =='w':
##                    screen.blit(P2,(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
                elif tile =='e':
                    screen.blit(P3,(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
                elif tile =='r':
                    screen.blit(P4,(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
                elif tile == '-':
                    screen.blit(pygame.transform.flip(SS,False,True),(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))
                elif tile == '+':
                    screen.blit(pygame.transform.flip(SS,True,True),(x*32-int(mario.scroll[0]),y*32-int(mario.scroll[1])))


                    
##            if tile =='(':
##                Slopes.append(Slope(x*32,y*32,"NE"))
##            elif tile ==')':
##                Slopes.append(Slope(x*32,y*32,"NW"))
##              
##            elif tile =='{':
##                Slopes.append(Slope(x*32,y*32,"ENE1"))
##
##            elif tile =='}':
##                Slopes.append(Slope(x*32,y*32,"WNW1"))
##               
##            elif tile =='[':
##                Slopes.append(Slope(x*32,y*32,"ENE2"))
##               
##            elif tile ==']':
##                Slopes.append(Slope(x*32,y*32,"WNW2"))
##            elif tile == '-':
##                Slopes.append(Slope(x*32,y*32,"SE",True))
##
##            elif tile == '+':
##                Slopes.append(Slope(x*32,y*32,"SW",True))
##            

##            elif tile != '0' and tile !='G' and tile != "g" and tile != 'q' and tile !='w' and tile != 'e' and tile != 'r'and tile != "W" and tile != "c" and not SP:
##                Grounds.append(pygame.Rect(x*32,y*32,32,32))



    
    
    return Grounds,Slopes,Waters
WSs = [pygame.image.load("Sprites/Water/water_surface1.png").convert_alpha(),
       pygame.image.load("Sprites/Water/water_surface2.png").convert_alpha(),
       pygame.image.load("Sprites/Water/water_surface3.png").convert_alpha(),
       pygame.image.load("Sprites/Water/water_surface4.png").convert_alpha(),
       pygame.image.load("Sprites/Water/water_inside.png").convert_alpha()]#Water Surfaces
def Waterloop(screen,mario):        
    for w in Waters:
        if w.IsSurface and Globals.IsRectOnScreen(w.rect,mario):
            screen.blit(WSs[(Globals.GlobalTimer // 6) % 4],(w.x-int(mario.scroll[0]),w.y-int(mario.scroll[1])))
        else:
            screen.blit(WSs[-1],(w.x-int(mario.scroll[0]),w.y-int(mario.scroll[1])))
    #return Waters

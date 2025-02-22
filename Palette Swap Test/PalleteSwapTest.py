#Pallete Swap Test
import pygame,sys,copy
screen = pygame.display.set_mode((640,480))
img = pygame.image.load("reimu_weapon4.png")#.convert_alpha()
img2 = pygame.image.load("reimu.png")
a = img.get_palette()
a = [tuple(i) for i in a]
print(set(a))

def trans_img_size(img,size,alpha = True):#size: float(0 ~ 1)
    w,h = img.get_size()
    if alpha: targ = pygame.transform.scale(img,(int(w * size), int(h * size))).convert_alpha()
    else: targ = pygame.transform.scale(img,(int(w * size), int(h * size)))
    
    return targ

#img.set_palette([(0,0,0),(255,0,0),(0,255,0),(255,255,0)])
#cirno1 - ???
#cirno2 - black
#cirno3 - darkblue(리본색)
#cirno4 - lightblue(머리색)
#cirno5 - peach(피부색)
#cirno6 - white(옷 색)
#cirno7 - ???(아마 얼굴 왼쪽 이마에 있는 오류)
#cirno8 - red(신발&리본색)
#cirno9 - darkerblue(명암)
ColorTable = {
    "Normal":[(0,232,216),(0,112,236)],
    "Fire":[(240,188,60),(216,40,0)],
    "Mario":[(248,64,112),(128,216,200)][::-1],
    "Toadette":[(248,248,248),(255,100,180)],
    "Mysterious":[(150,150,150),(0,0,0)],
    "Bomb":[(0,204,0),(0,110,0)],
    "Purple":[(248,184,248),(136,0,112)],
    "Rumia":[(255,255,255),(165,148,0)],
    "Mystia":[(77,0,134),(250,184,241)][::-1],
    "Wriggle":[(21,151,0),(69,69,69)],
    "Utsuho":[(240,188,60),(255,123,0)][::-1],
    "Youmu":[(0,132,69),(255,255,255)][::-1],
    "Reimu":[(255,255,255),(255,0,0)]}


palette = [(0,0,0),#unknown(아마 투명)
           (0,0,0),#black,테두리
           (0,110,255),#darkblue, 리본색
           (0,231,235),#lightblue,머리색
           (248,236,199),#peach, 피부색
           (255,255,255),#white, 옷 색
           (248,236,199),#오류이지만 피부색과 같은 색으로 변경
           (207,0,0),#red, 신발 & 리본색
           (0,66,153)]#darkerblue, 명암


OGpalette = copy.deepcopy(palette)
##palette[3],palette[2] = ColorTable["Purple"]
##palette[8] = (0,0,0)
#print(OGpalette)
#img.set_palette(palette)


#1 - nothing(투명?)
#2 - 테두리
#3 - 흰색
#4 - 빨간색
#5 - 머리색
#6 - 피부색
#7 - 눈매(살짝 다른 검은색)
#8 - 흰자(살짝 다른 흰색)
#9 - 눈에 있는 회색

#1 - nothing
#2 - 테두리
#3 - 빨간색
#4 - 흰색
#5 - 머리색
#6 - 피부색
#7 - 피부색 명암
#8 - 눈매
#9 - 흰자
#10 - 눈에 있는 회색

p = [(0,0,0),(0,0,0),(255,255,255),(210, 34, 99),(65, 51, 87),(246, 225, 204),(10,10,10),(250,250,250),(73, 73, 73)]
p2 = [(0,0,0),(0,0,0),(210, 34, 99),(255,255,255),(65, 51, 87),(246, 225, 204),(250,203,157),(10,10,10),(250,250,250),(73,73,73)]

#p[4] = (0,0,0)#(177,0,215)

#img.set_palette(p)#,(255,0,0),(0,255,0),(0,0,255),(255,0,0)])

import random
def make_8bit(p):
    p[1] = p[2] #테두리를 진한색으로
    p[5] = p[4] #옷색을 피부색으로
    p[7] = p[2] #리본색을 진한색으로

    p[8] = p[2] #명암을 진한 색으로


    return p

def random_set():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
#img.set_palette([(0,0,0,255),random_set(),random_set(),random_set()])
img = trans_img_size(img,1,alpha = False)
img2 = trans_img_size(img2,1,alpha = False)
#img = img.convert_alpha()
#print(img.get_palette())

CLOCK = pygame.time.Clock()
f = 0
idx = 0
NESmode = False
while True:
    f+=1
    screen.fill((128,128,128))
    pygame.display.set_caption("FPS: " + str(CLOCK.get_fps()))
    #if f % 1 ==0:idx = (idx + 1)%len(ColorTable)
    p[2],p[3]= ColorTable[list(ColorTable.keys())[idx]]

    temp = copy.deepcopy(palette)
    if NESmode: final = make_8bit(temp)
    else: final = temp

##    if f % 8 == 0:p[1] = (0,0,0)
##    if f% 8 == 4:p[1] = (255,0,0)
    
    img.set_palette(p2)

    p2[3],p2[2]= ColorTable[list(ColorTable.keys())[idx]]

    img2.set_palette(p)
    #img.set_palette([(0,0,0,255),(0,0,0),random_set(),random_set()])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: idx = (idx - 1)%len(ColorTable)
            if event.key == pygame.K_RIGHT: idx = (idx + 1)%len(ColorTable)
            if event.key == pygame.K_SPACE: NESmode = not NESmode

    screen.blit(img,(50,0))
    screen.blit(img2,(400,0))
    pygame.display.update()
    CLOCK.tick(60)
    #print(CLOCK.get_fps())

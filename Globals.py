import pygame
SW,SH = 640,480

GlobalTimer = 0
Lvidx = 0
WaterTheme = False
SnowTheme = False
AutoScroll = False
ScrollLimit = [[0,None],[None,85]]
CurrentPipes = []
BGM = "BGM/Athletic Theme.mp3"
MarioAt = 0#main/sub/other
LevelCount = 2#총 한 맵에 연결된 레벨 개수
AutoScrollVector = (2,0)
StartPoint = (0,0)
StartLvlIdx = 0#죽고 다시 시작할때 어떤 레벨에서 다시 시작하는지(기본 0)

RegisteredCPidx = -1#-1이면 체크포인트가 안찍혔다는 뜻
def loop(mario):
    global GlobalTimer
    if not mario.GamePause and not mario.pause:
        GlobalTimer += 1

def IsRectOnScreen(rect,mario): 
    return -rect.width <= rect.x - mario.scroll[0] <= SW and -rect.height <= rect.y - mario.scroll[1] <= SH

def trans_img_size(img,size,alpha = True):#size: float(0 ~ 1)
    w,h = img.get_size()
    if alpha: targ = pygame.transform.scale(img,(int(w * size), int(h * size))).convert_alpha()
    else: targ = pygame.transform.scale(img,(int(w * size), int(h * size)))
    
    return targ

import Ground

rangeY = [0,0]

GRAVITY = 1
def binarySearch(rect,tiles):
    start = 0
    end = len(tiles) - 1
##    if tiles == []: return []
##    if rect.x < tiles[start].x: return []
##    if rect.x > tiles[end - 1].x: return []

    
    while start + 1 < end:
        mid = int((start + end) / 2)
        if tiles[mid].left <= rect.left: start = mid
        else: end = mid
    tiles = sorted(tiles, key = lambda r:r.right)
    start2 = 0
    end2 = len(tiles) - 1
    while start2 + 1 < end2:
        mid = int((start2 + end2) / 2)
        if tiles[mid].right <= rect.right: start2 = mid
        else: end2 = mid

    a = start
    while a > 0 and tiles[a].left == tiles[a - 1].left:
        a -= 1
    b = end2
    while b < len(tiles) - 1 and tiles[b].right == tiles[b + 1].right:
        b += 1

    a = max(a,1)
    #print(tiles[a-5:b + 5],rect)
    return tiles[a-1:b+1]

def collision_test(rect,Grounds,slopeReturn = False):#호환성을 위해 잠시 남겨둠(hit_slope return 안함)
    l,r = rect.left // 32, (rect.right - 1) // 32
    t,b = rect.top // 32, (rect.bottom - 1) // 32
    hit_list = []
    hit_slope = []
    for y in range(t,b + 1):
        for x in range(l,r + 1):
            if x >= 0 and y >= 0 and y < Ground.rangeY[1] and x < Ground.rangeX[1]:
                t = Ground.game_map[y][x]
                
                if t == 1 or t == "1":
                    hit_list.append(pygame.Rect(x * 32, y * 32, 32, 32))
                elif t in Ground.SlopeData:
##                    extra = 0
##                    if t in ["{","}"]: extra = 16
                    hit_slope.append((t,pygame.Rect(x * 32, y * 32, 32, 32)))
    #print("call colcheck ->",end='')

    hit_list += [Grounds[i] for i in rect.collidelistall(Grounds)]#rect와 충돌하는 모든 rect의 index반환                   
##    for tile in binarySearch(rect,Grounds):#for tile in Grounds:
##        if rect.colliderect(tile):
##            hit_list.append(tile)
    #binary search는 다음에 연구하는걸로...

    if slopeReturn: return hit_list,hit_slope
    else: return hit_list#,hit_slope
    
def slope_collision_test(rect):
    l,r = rect.left // 32, (rect.right - 1) // 32
    t,b = rect.top // 32, (rect.bottom - 1) // 32
    FinalPos = None#아무것도 collide 안함
    for y in range(t,b + 1):
        for x in range(l,r + 1):
            if x >= 0 and y >= 0 and y < Ground.rangeY[1] and x < Ground.rangeX[1]:
                t = Ground.game_map[y][x]
                if t in Ground.SlopeData:
                    slopetype = t
                    hitbox = pygame.Rect(x * 32, y * 32, 32, 32)
                    rel_x = rect.x - hitbox.x
                    if slopetype == "(":
                        pos_height = rel_x + rect.width  
                    elif slopetype == ")":
                        pos_height = 32 - rel_x
                    elif slopetype == "{" or slopetype == "[":
                        pos_height = 0.5 * (rel_x + rect.width)
                        if slopetype == "[": pos_height += 16
                        
                    elif slopetype == "}" or slopetype == "]":
                        pos_height = 0.5 * (32 - rel_x)
                        if slopetype == "]": pos_height += 16
                    else:
                        pos_height = 69
                        
                    pos_height = min(pos_height, 32)
                    pos_height = max(pos_height, 0)
                    target_y = hitbox.bottom - pos_height
                    
                    if rect.bottom >= target_y:
                        FinalPos = target_y
                        #print(FinalPos)
    return FinalPos
def test_collision_test(rect,Grounds):
    l,r = rect.left // 32, (rect.right - 1) // 32
    t,b = rect.top // 32, (rect.bottom - 1) // 32
    hit_list = []
    hit_slope = []
    for y in range(t,b + 1):
        for x in range(l,r + 1):
            if x >= 0 and y >= 0 and y < Ground.rangeY[1] and x < Ground.rangeX[1]:
                t = Ground.game_map[y][x]
                
                if t == 1 or t == "1":
                    hit_list.append(pygame.Rect(x * 32, y * 32, 32, 32))
                elif t in Ground.SlopeData:
                    extra = 0
                    if t in ["{","}"]: extra = 16
                    hit_slope.append((t,(x * 32, y * 32 + extra)))

    #hit_list += [Grounds[i] for i in rect.collidelistall(Grounds)]#rect와 충돌하는 모든 rect의 index반환            
    for tile in binarySearch(rect,Grounds):#for tile in Grounds:
        if rect.colliderect(tile):
            hit_list.append(tile)

    return hit_list,hit_slope

def water_collision_test(rect):
    l,r = rect.left // 32, (rect.right - 1) // 32
    t,b = rect.top // 32, (rect.bottom - 1) // 32
    hit_surfaceWater = []
    hit_normalWater = []


    for y in range(t,b + 1):
        for x in range(l,r + 1):
            if x >= 0 and y >= 0 and y < Ground.rangeY[1] and x < Ground.rangeX[1]:
                t = Ground.water_map[y][x]
                
                if t == "W": hit_surfaceWater.append(pygame.Rect(x * 32, y * 32, 32, 32))
                elif t == "w": hit_normalWater.append(pygame.Rect(x * 32, y * 32, 32, 32))
                

    return  hit_surfaceWater, hit_normalWater




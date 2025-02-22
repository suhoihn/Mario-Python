#slope test
import pygame,sys,random
screen=pygame.display.set_mode((640,480))
x,y=0,0
sx,sy=200,400
slopeYs=[pygame.Rect(i,-3*i+1000,1,1) for i in range(sx,480)]#y=1/2x+350
yv=0
playerRect=pygame.Rect(x,y,30,30)
CLOCK=pygame.time.Clock()
idx=0
onslope=False
triggered=False
acc,sub=0,0
while True:
  
    key=pygame.key.get_pressed()
    
    screen.fill((0,0,0))
    if not onslope:
        yv+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

##        if event.type ==pygame.KEYDOWN and not onslope:
##            if event.key==pygame.K_LEFT:
##                x-=5
##            if event.key==pygame.K_RIGHT:
##                x+=5
                
    if playerRect.colliderect(pygame.Rect(0,480-30,640,30)):
        yv=0
        if not(playerRect.bottom == pygame.Rect(0,480-30,640,30).top):
            y-=1
            
    else:
        if playerRect.bottom == pygame.Rect(0,480-30,640,30).top:
            y+=1
            if key[pygame.K_UP]:
                yv=-20


    #i=i%len(slopeYs)
    onslope=False
    for i in slopeYs:
        pygame.draw.rect(screen,(255,255,255),i)
        #playerRect.y+=1
        if playerRect.colliderect(i):
            idx=slopeYs.index(i)
            onslope=True
            yv=0
            if key[pygame.K_UP]:
                yv=-20
            if key[pygame.K_LEFT] or triggered:
                try:
                    triggered=True
                    x,y=slopeYs[idx-3].x-30,slopeYs[idx-3].y-30
                except:
                    triggered=False
                    onslope=False
                    x+=1
                    yv-10
            if key[pygame.K_RIGHT]:
                try:
                    x,y=slopeYs[idx+3].x-30,slopeYs[idx+3].y-30
                except:
                    triggered=False
                    onslope=False
                    
        #playerRect.y-=1
    
    idx=0
    y+=yv
    playerRect=pygame.Rect(x,y,30,30)
    #playerRect.bottomright=slopeYs[i]
    print(onslope)
    if not onslope:
        triggered=False
        #triggered=False
        if key[pygame.K_LEFT]:
            x-=3
        if key[pygame.K_RIGHT]:
            x+=3
    else:
        if triggered:
            if acc<=10:
                acc+=0.1
                sub+=int(acc)
        else:
            acc=0
            sub=1
    
        
    pygame.draw.rect(screen,(0,255,255),playerRect)
        
    pygame.draw.rect(screen,(0,255,128),pygame.Rect(0,480-30,640,30))

    pygame.display.update()
    CLOCK.tick(60)

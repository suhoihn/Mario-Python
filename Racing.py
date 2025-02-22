import pygame,sys,time
from math import *
pygame.init()
sw,sh = 400,400


screen = pygame.display.set_mode((sw,sh))
fDistance = 0
fSpeed = 0
fCurvature = 0

vecTrack = []

vecTrack.append([0,10])
vecTrack.append([0,200])
vecTrack.append([10,200])
vecTrack.append([0,400])
vecTrack.append([-10,100])
vecTrack.append([0,200])
vecTrack.append([-10,200])
vecTrack.append([10,200])
vecTrack.append([0,200])
vecTrack.append([0.2,200])
vecTrack.append([0,200])

CLOCK = pygame.time.Clock()


class Car(object):
    def Physics(self,dt):
        global fDistance,fCurvature,fSpeed
        k = CLOCK.get_fps()
        if k == 0: k = 0.1
        
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            fSpeed += 2
        else:
            fSpeed -= 1

        if fSpeed < 0 : fSpeed = 0
        if fSpeed > 1 : fSpeed = 1

        fDistance += (70 * fSpeed)

        fOffset = 0
        nTrackSection = 0
        while (nTrackSection < len(vecTrack) and fOffset <= fDistance):
            fOffset += vecTrack[nTrackSection][1]
            nTrackSection += 1

        fTargetCurvature = vecTrack[nTrackSection-1][0]
    
        fTrackCurveDiff = (fTargetCurvature - fCurvature) * dt / k * fSpeed
    
        fCurvature += fTrackCurveDiff
        
        for y in range(0,int(sh/2),2):
            for x in range(0,sw,2):
                fPerspective = y / (sh/2)

                fMiddlePoint = 0.5 + fCurvature * ((1 -fPerspective) ** 3)
                fRoadWidth =   fPerspective * 0.8 + 0.1
                fClipWidth = fRoadWidth * 0.15

                fRoadWidth *= 0.5

                nLeftGrass = int((fMiddlePoint - fRoadWidth - fClipWidth) * sw)
                nLeftClip = int((fMiddlePoint - fRoadWidth) * sw)
                nRightGrass = int((fMiddlePoint + fRoadWidth + fClipWidth) * sw)
                nRightClip = int((fMiddlePoint + fRoadWidth) * sw)

                nRow = int(sh /2 + y)

                if sin(radians(2000 * ((1-fPerspective)**3) + fDistance * 0.1)) > 0 : nGrassColor = pygame.Color(0,255,0)
                else: nGrassColor = pygame.Color(0,128,0)

                if sin(radians(8000 * ((1-fPerspective)**2) + fDistance)) > 0 : nClipColor = pygame.Color(255,0,0)
                else: nClipColor = pygame.Color(255,255,255)

                
                if (0 <= x <= nLeftGrass):
                    pygame.draw.rect(screen,nGrassColor,(x,nRow,1,1))
                if (nLeftGrass <= x <= nLeftClip):
                    pygame.draw.rect(screen,nClipColor,(x,nRow,1,1))
                if (nLeftClip <= x <= nRightClip):
                    pygame.draw.rect(screen,(128,128,128),(x,nRow,1,1))
                if (nRightClip <= x <= nRightGrass):
                    pygame.draw.rect(screen,nClipColor,(x,nRow,1,1))
                if (nRightGrass <= x <= sw):
                    pygame.draw.rect(screen,nGrassColor,(x,nRow,1,1))


car = Car()
a=time.time()
while True:
    a=time.time()
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    car.Physics(time.time()-a)

    pygame.display.update()

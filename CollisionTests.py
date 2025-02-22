#Collision Theroms
from math import *
import pygame,sys,copy
screen = pygame.display.set_mode((640,480))

class vec2D:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class polygon:
    def __init__(self,pos,angle):
        self.p = []#vec2D, transformed points
        self.pos = pos#vec2D, position of shape
        self.angle = angle#float, direction of shape
        self.o = []#vec2D, original model of shape
        self.overlap = False#flag
        
vecShapes = []

fTheta = pi * 2/5
s1 = polygon([100,100],0)
for i in range(5):
    s1.o.append((30 * cos(fTheta * i), 30 * sin(fTheta * i)))
    s1.p.append((30 * cos(fTheta * i), 30 * sin(fTheta * i)))

fTheta = pi * 2/3
s2 = polygon([200,150],0)
for i in range(3):
    s2.o.append((20 * cos(fTheta * i), 20 * sin(fTheta * i)))
    s2.p.append((20 * cos(fTheta * i), 20 * sin(fTheta * i)))

s3 = polygon([50,200],0)
s3.o.append((-30,-30))
s3.o.append((-30,+30))
s3.o.append((+30,+30))
s3.o.append((+30,-30))

s3.p = copy.deepcopy(s3.o)

vecShapes.append(s1)
vecShapes.append(s2)
vecShapes.append(s3)
def ShapeOverlap_DIAGS(r1,r2):
    poly1 = r1
    poly2 = r2
    for shape in range(2):
        if shape == 1:
            poly1 = copy.deepcopy(r2)
            poly2 = copy.deepcopy(r1)
        for p in range(len(poly1.p)):
            line_r1s = poly1.pos
            line_r1e = poly1.p[p]
            
            for q in range(len(poly2.p)):
                line_r2s = poly2.p[q]
                line_r2e = poly2.p[(q + 1) % len(poly2.p)]
               
                h = (line_r2e[0] - line_r2s[0]) * (line_r1s[1] - line_r1e[1]) - (line_r1s[0] - line_r1e[0]) * (line_r2e[1] - line_r2s[1]);
                if h == 0:
                    continue
                t1 = ((line_r2s[1] - line_r2e[1]) * (line_r1s[0] - line_r2s[0]) + (line_r2e[0] - line_r2s[0]) * (line_r1s[1] - line_r2s[1])) / h;
                t2 = ((line_r1s[1] - line_r1e[1]) * (line_r1s[0] - line_r2s[0]) + (line_r1e[0] - line_r1s[0]) * (line_r1s[1] - line_r2s[1])) / h;

                if t1 >= 0 and t1 < 1 and t2 >= 0 and t2 < 1:
                    return True
    return False

def ShapeOverlap_SAT(r1,r2):
    poly1 = r1
    poly2 = r2
    for shape in range(2):
        if shape == 1:
            poly1 = copy.deepcopy(r2)
            poly2 = copy.deepcopy(r1)
        for a in range(len(poly1.p)):
            b = (a + 1) % len(poly1.p)
            #The axis vector between two points
            axisProj = (-(poly1.p[b][1] - poly1.p[a][1]), poly1.p[b][0] - poly1.p[a][0])
            min_r1 = 999999
            max_r1 = -999999
            for p in range(len(poly1.p)):
                q = poly1.p[p][0] * axisProj[0] + poly1.p[p][1] * axisProj[1]
                min_r1 = min(min_r1,q)
                max_r1 = max(max_r1,q)
                
            min_r2 = 999999
            max_r2 = -999999
            for p in range(len(poly2.p)):
                q = poly2.p[p][0] * axisProj[0] + poly2.p[p][1] * axisProj[1]
                min_r2 = min(min_r2,q)
                max_r2 = max(max_r2,q)

            if not (max_r2 >= min_r1 and max_r1 >= min_r2):#if lines intersect
                return False

    return True
                
spd = 5
CLOCK = pygame.time.Clock()
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    key = pygame.key.get_pressed()

    if key[pygame.K_UP]: vecShapes[0].pos[0] += cos(vecShapes[0].angle) * spd; vecShapes[0].pos[1] += sin(vecShapes[0].angle) * spd
    if key[pygame.K_DOWN]:vecShapes[0].pos[0] -= cos(vecShapes[0].angle) * spd; vecShapes[0].pos[1] -= sin(vecShapes[0].angle) * spd
    if key[pygame.K_LEFT]:vecShapes[0].angle -= 0.1
    if key[pygame.K_RIGHT]:vecShapes[0].angle += 0.1
    if key[pygame.K_w]:vecShapes[1].pos[0] += cos(vecShapes[1].angle) * spd; vecShapes[1].pos[1] += sin(vecShapes[1].angle) * spd
    if key[pygame.K_a]:vecShapes[1].angle -= 0.1
    if key[pygame.K_s]:vecShapes[1].pos[0] -= cos(vecShapes[1].angle) * spd; vecShapes[1].pos[1] -= sin(vecShapes[1].angle) * spd
    if key[pygame.K_d]:vecShapes[1].angle += 0.1
    for r in vecShapes:
        for i in range(len(r.o)):
            r.p[i] = [
                r.o[i][0] * cos(r.angle) - r.o[i][1] * sin(r.angle) + r.pos[0],
                r.o[i][0] * sin(r.angle) + r.o[i][1] * cos(r.angle) + r.pos[1]
                ]
        r.overlap = False
    for m in range(len(vecShapes)):
        for n in range(m + 1,len(vecShapes)):
            vecShapes[m].overlap |= ShapeOverlap_DIAGS(vecShapes[m], vecShapes[n])
    for r in vecShapes:
        if r.overlap: color = (255,0,0)
        else: color = (255,255,255)
        
        for i in range(len(r.p)):
            pygame.draw.line(screen,color,(r.p[i][0],r.p[i][1]),(r.p[(i + 1) % len(r.p)][0], r.p[(i + 1) % len(r.p)][1]))
        pygame.draw.line(screen,color,(r.p[0][0],r.p[0][1]),r.pos)

    pygame.display.update()
    CLOCK.tick(60)

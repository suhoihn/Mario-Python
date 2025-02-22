#움직이는 플랫폼에 대한 연구
import pygame,sys,math,copy,random
screen = pygame.display.set_mode((640,480))
ground = []

def true_ceil(n):
    if n == 0:
        return 0
    return math.ceil(abs(n)) * int(abs(n) / n)
class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,32,32)
        self.xv = 0
        self.yv = 0
        self.movement = [0,0]
        
        self.actualYspd = 0
        
        self.standingplatform = None
        self.collision = {"top":False,"bottom":False}
    
    
    def collision_check(self):

        self.collision = {"top":False,"bottom":False}



        

        if self.standingplatform != None:
            self.movement[0] += self.standingplatform.vec[0]
          
        self.rect.x += math.ceil(self.movement[0])
        hit_list = []
        for i in ground:
            if self.rect.colliderect(i):# and not i.SemiSolid:
                hit_list.append(i)
                
##        for i in hit_list:
##            if not i.SemiSolid:
##                for j in range(abs(math.ceil(self.movement[0]))):
##                    if self.rect.colliderect(i.rect):
##                        self.rect.x += abs(self.movement[0])/self.movement[0] * -1
                    
        

        

        
            #print("spc")
##        if self.movement[1] == 0:
##            self.movement[1] = 1
        #self.actualYsped = 0
        
            
        
            
            
        

        if self.standingplatform != None:
            
            if self.movement[1] >= 0:
                self.collision["bottom"] = True
            
            self.rect.y += self.standingplatform.vec[1]
            self.rect.y += true_ceil(self.movement[1])
            for j in range(abs(true_ceil(self.movement[1]))):
                
                if self.rect.colliderect(self.standingplatform.rect):
                    self.rect.y += abs(self.movement[1])/self.movement[1] * -1
                    #self.yv = 0
            self.rect.y -= self.standingplatform.vec[1]
            self.rect.y -= true_ceil(self.movement[1])

            self.movement[1] += self.standingplatform.vec[1]
            self.actualYsped = self.standingplatform.vec[1]
            if self.actualYsped == 0:
                self.actualYsped = self.movement[1]
                
        else:
            self.actualYsped = self.movement[1]
            
            
            
        hit_list = []
        
        if abs(self.movement[1]) != 0:
            self.rect.y += true_ceil(self.movement[1])
        #prevStanding = self.standingplatform
        self.standingplatform = None
        for i in ground:
            if self.rect.colliderect(i.rect):#and i != prevStanding:
                hit_list.append(i)
                #if self.movement[1] > 0:
                self.standingplatform = i
        
                
            
##                self.rect.y += math.ceil(self.standingplatform.vec[1])
##                self.movement[1] += self.standingplatform.vec[1]

        

##        for i in hit_list:
##            if self.movement[1] > 0:
##                #if self.rect.bottom <= i.top + 15:
##                    self.rect.bottom = i.top
##                    self.collision["bottom"] = True
##            elif self.movement[1] < 0:
##                self.rect.top = i.bottom
##                self.collision["top"] = True
        print(self.movement[1],self.actualYsped,end = " ")    
        for i in hit_list:
            if i.SemiSolid:
                #self.rect.y += i.vec[1]
                if self.standingplatform != None:
                    if self.movement[1] - self.standingplatform.vec[1] >= 0:# and self.rect.bottom <= i.rect.top + 10:
                        self.collision["bottom"] = True
                else:
                    if self.movement[1] >= 0:# and self.rect.bottom <= i.rect.top + 10:
                        self.collision["bottom"] = True

            
                #self.movement[1] += i.vec[1]
                #print(abs(true_ceil(self.movement[1])))
                for j in range(abs(true_ceil(self.actualYsped))):
                    if self.rect.colliderect(i.rect):
                        self.rect.y += abs(self.actualYsped)/self.actualYsped * -1
                self.yv = 0
            else:
                if self.movement[1] > 0:
                    self.collision["bottom"] = True
                elif self.movement[1] < 0:
                    self.collision["top"] = True
                    
                for j in range(abs(math.ceil(self.movement[1]))):
                    if self.rect.colliderect(i.rect):
                        self.rect.y += abs(self.movement[1])/self.movement[1] * -1
                self.yv = 0
                
        #print(self.collision["bottom"])

    def collision_check2(self):
        self.collision = {"top":False,"bottom":False}
        
        self.rect.x += math.ceil(self.movement[0])
        hit_list = []
        for i in ground:
            if self.rect.colliderect(i):# and not i.SemiSolid:
                hit_list.append(i)
                
        for i in hit_list:
           
            if self.movement[0] >= 0:
                self.rect.right = i.rect.left
            elif self.movement[0] <= 0:
                self.rect.left = i.rect.right


        self.rect.y += math.ceil(self.movement[1])
        hit_list = []
        for i in ground:
            if self.rect.colliderect(i):# and not i.SemiSolid:
                hit_list.append(i)
                
        for i in hit_list:
            
            if self.movement[1] < 0:
                self.rect.top = i.rect.bottom
                self.collision["top"] = True
            elif self.movement[1] > 0:
                self.rect.bottom = i.rect.top
                self.collision["bottom"] = True

    def collision_check3(self):
        

        self.collision = {"top":False,"bottom":False}
        if self.standingplatform != None:
            self.movement[0] += self.standingplatform.vec[0]
          
        self.rect.x += math.ceil(self.movement[0])
        hit_list = []
        for i in ground:
            if self.rect.colliderect(i):# and not i.SemiSolid:
                hit_list.append(i)
                
        for i in hit_list:
            for j in range(abs(math.ceil(self.movement[0]))):
                if self.rect.colliderect(i.rect):
                    self.rect.x += abs(self.movement[0])/self.movement[0] * -1



        if self.standingplatform != None:
            #self.rect.y += self.standingplatform.vec[1] --> y를 직접 이동하면 내가 천장에 닿았을 때 플랫폼에 서있는것까지 계산되므로 같이 올라가서 껴짐 --> 효과는 눈에 바로 보이더라도 쓰지 말자!
            self.rect.bottom = self.standingplatform.rect.top#이것도 별로 좋지 않은 생각인게 천장에 닿으면 그냥 뚫고 가버림
            #self.movement[1] += self.standingplatform.vec[1]

            #자자 이렇게 합시다
            #player가 뛰지 않는한 계속 플랫폼에 붙어있는다
            #그동안 movement[1]은 변경된다
            #OK?(마리오에서 구현했던것과 같은거임)
        self.rect.y += math.ceil(self.movement[1])
        

        prev = self.standingplatform
        self.standingplatform = None
        for i in platforms:
            if prev != i:
                self.rect.y += i.vec[1]
            if self.rect.colliderect(i.rect):
                self.standingplatform = i
                self.rect.bottom = self.standingplatform.rect.top
                #self.rect.y += i.vec[1]
                #self.movement[1] += i.vec[1]
                #print("GOGO")
            if prev != i:
                self.rect.y -= i.vec[1]
        
        hit_list = []   
        for i in ground:
            if self.rect.colliderect(i.rect):
                hit_list.append(i)



##        if self.standingplatform != None:
##            self.movement[1] += self.standingplatform.vec[1]

        print(self.standingplatform)# in hit_list)
        for i in hit_list:#Push Priority: moving platform < normal platform
            if self.movement[1] >= 0:# and self.rect.bottom <= i.rect.top + 10:
                self.collision["bottom"] = True
            if i == self.standingplatform or self.standingplatform == None:
                k = self.movement[1]# + i.vec[1]
            else:
                k = self.movement[1] + self.standingplatform.vec[1]
                print(k)
            for j in range(abs(math.ceil(k))):
                if self.rect.colliderect(i.rect):
                    self.rect.y += abs(k)/k * -1

            

            self.yv = 0
##        if self.standingplatform != None:
##            print(self.rect.bottom - self.standingplatform.rect.top)
##            print(self.rect.colliderect(self.standingplatform.rect))

            

        
        if None != self.standingplatform:
             pass#print(self.standingplatform.rect.top - self.rect.bottom)

        
    def loop(self):
        global FPS
        self.movement = [0,0]
        self.yv += 0.5
        
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.xv = 5
        elif key[pygame.K_LEFT]:
            self.xv = -5

        if key[pygame.K_SPACE]:
            FPS = 1
        else:
            FPS = 60
            
        
        if abs(self.xv) < 1:
            self.xv = 0

        self.xv *= 0.7

        
        
        #print(self.yv)

        if self.yv > 15:
            self.yv = 15


        
                
                
        
        
        

##        self.standingplatform = None
##        for i in ground:
##            old = copy.deepcopy(self.rect.y)
##            self.rect.y += i.vec[1]
##            for j in range(abs(math.ceil(self.yv))):
##                self.rect.y += 1
##                if self.rect.colliderect(i.rect) and i.rect.top + 15 >= self.rect.bottom >= i.rect.top and self.yv > 0:
##                    self.yv = 0
##                    self.movement[0] += i.vec[0]
##                    self.movement[1] += i.vec[1]
##                    print("ang")
##                    #self.collision["bottom"] = True
##                    self.standingplatform = i
##                    break
##            
##            self.rect.y = old
##        
            
        
        
               
        self.movement[0] += self.xv
        self.movement[1] += self.yv
##        if self.collision["top"]:
##            self.yv = 0
##        if self.collision["bottom"]:
##            
##    
##            if key[pygame.K_UP]:
##                self.yv = -15



       
        

        #print(self.movement[1],self.actualYspd)

        self.collision_check2()
        if self.collision["top"]:
            self.yv = 0
        if self.collision["bottom"]:
            
            #self.yv = 0
            if key[pygame.K_UP]:
                self.yv = -15
        
        #print(self.yv,self.movement[1],self.collision["bottom"])
        #self.collision_check()
       # print(self.xv)
        
        
        
player = Player(0,0)
platforms = []
class moving_platform:
    def __init__(self,x,y,w,h,vec,semisolid = False):
        self.SemiSolid = semisolid
        self.vec = vec
        self.timer = 0
        self.rect = pygame.Rect(x,y,w,h)
        ground.append(self)
        platforms.append(self)

    def loop(self):
        self.timer += 1
        #self.vec[1] = 3 * math.sin(math.radians(self.timer))
        #self.vec[1] = self.rect.y
        self.rect.x += self.vec[0]
        self.rect.y += self.vec[1]
        #self.rect.y = 100 * math.sin(10 * math.radians(self.timer)) + 180
        if self.rect.right > 640 or self.rect.left < 0:
            self.vec[0] *= -1
        if self.rect.bottom > 480 or self.rect.top < 0:
            self.vec[1] *= -1

        #self.vec[1] = self.rect.y - self.vec[1]

class platform:
    def __init__(self,x,y,w,h):#,vec,semisolid = False):
        self.rect = pygame.Rect(x,y,w,h)
        ground.append(self)
        

platform(0,180,100,30)#,[5,0],True)
platform(0,380,640,10)#,[0,0],False)
moving_platform(0,180,500,30,[0,15],True)

#platform(0,80,100,30)#,[0,0],False)
#platform(0,350,100,30,[3,0],False)
#platform(300,100,50,300,[0,0],False)



CLOCK = pygame.time.Clock()
FPS = 60
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #player.loop()
    for i in platforms:
        i.loop()
    for i in ground:
        pygame.draw.rect(screen,(255,0,0),i.rect)
    
    player.loop()
    pygame.draw.rect(screen,(0,0,255),player.rect)
    
    pygame.display.update()
    CLOCK.tick(FPS)

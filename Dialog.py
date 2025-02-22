#Dialog
import pygame,sys
pygame.init()
screen=pygame.display.set_mode((640,480))
CLOCK = pygame.time.Clock()

def text_objects(text,color):
    textSurface=pygame.font.Font('freesansbold.ttf',25).render(text,True,color)
    return textSurface,textSurface.get_rect()

class DialogBox(object):
    def __init__(self,message):
        self.message=message
        self.frame = pygame.Surface((620,150))
        self.timer=0
        
        self.page=0
        self.lettercnt=-1

        self.letterX=0
        self.letterY=0

        self.ready=False
        self.commandWord=False
        self.command=''
        self.color=(255,255,255)

        self.TempLetterList=[]

    def draw(self,screen):
        #print(CLOCK.get_fps())
        if self.timer+20 < pygame.time.get_ticks():
            self.timer = pygame.time.get_ticks()
            if len(self.message[self.page]) > self.lettercnt+1:
                self.lettercnt+=1
            
                    
            if self.message[self.page][self.lettercnt] == "\\" or self.commandWord:
                self.commandWord=True
                for i in self.message[self.page][self.lettercnt:]:
                    if i == ']':
                        break
                    else:
                        self.command+=i
                        self.lettercnt+=1
                

                self.command=self.command.split('/')

                print(self.command)
                if self.command[0] == "\clr":
                    if self.command[1] == "red":
                        self.color = (255,0,0)
                    elif self.command[1] == "orange":
                        self.color = (255,62,0)
                    elif self.command[1] == "yellow":
                        self.color = (255,255,0)
                    elif self.command[1] == "green":
                        self.color = (0,255,0)
                    elif self.command[1] == "blue":
                        self.color = (0,0,255)
                    elif self.command[1] == "indigo":
                        self.color = (75,0,130)
                    elif self.command[1] == "purple":
                        self.color = (128,0,128)
                    elif self.command[1] == "white":
                        self.color = (255,255,255)
                    elif self.command[1] == "black":
                        self.color = (0,0,0)
                        
                    
                self.command=''
                self.commandWord=False

            else:
                TS,TR = text_objects(self.message[self.page][self.lettercnt],self.color)
                if not self.ready and not self.commandWord:
                    TR.x = self.letterX
                    TR.y = self.letterY
                    self.letterX+=TR.width
                    if self.letterX > self.frame.get_width() - 20:
                        self.letterX = 0
                        self.letterY += 40

                    if not(len(self.message[self.page]) > self.lettercnt+1):
                        self.ready=True
                        
                    self.TempLetterList.append([TS,TR])

                for i in self.TempLetterList:
                    self.frame.blit(*i)
            
        screen.blit(self.frame,(10,320))

    def eventloop(self,event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                if self.ready:
                    self.letterX=0
                    self.letterY=0
                    self.TempLetterList=[]
                    self.lettercnt=-1
                    self.page+=1
                    self.ready = False
                    self.frame.fill((0,0,0))
                else:
                    print("성격이 급하시군")

            

DB = DialogBox(["Hello","This is Test","...","What do you want more?","Ok, this is very long message just for \clr/red]you! \clr/indigo]LOL"])

while True:
    
    screen.fill((255,255,255))
    for event in pygame.event.get():
        DB.eventloop(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    DB.draw(screen)
    
    pygame.display.update()
    CLOCK.tick(60)

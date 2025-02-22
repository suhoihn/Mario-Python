#Spike
import pygame
import Globals
Spikes = []
SpikeImages = [pygame.transform.scale(pygame.image.load("Sprites/Spike/Spike1.png"),(32,32)).convert_alpha(),
               pygame.transform.scale(pygame.image.load("Sprites/Spike/Spike2.png"),(32,32)).convert_alpha()]
#[pygame.transform.scale(pygame.image.load("Sprites/muncher/muncher1.png"),(32,32)).convert_alpha(),pygame.transform.scale(pygame.image.load("Sprites/muncher/muncher2.png"),(32,32)).convert_alpha()]
class Spike:
    def __init__(self,x,y):
        self.rect = SpikeImages[0].get_rect()
        self.rect.x, self.rect.y = x,y
        Spikes.append(self)

    def Physics(self,mario):
        #self.image = self.images[(Globals.GlobalTimer // 6) % 2]
        if self.rect in mario.hitlistsV * (not mario.RidingYoshi) + mario.hitlistsH:
            mario.Death()


def loop(screen,mario):
    for i in Spikes:
        if Globals.IsRectOnScreen(i.rect,mario):
            i.Physics(mario)#이게 여기 들어가야 되나?
            screen.blit(SpikeImages[(Globals.GlobalTimer // 6) % 2],(i.rect.x - mario.scroll[0],i.rect.y - mario.scroll[1]))



        

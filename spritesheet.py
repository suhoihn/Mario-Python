import pygame,sys
class SpriteSheet:
    def __init__(self,image):
        self.spritesheet = pygame.image.load(image),convert()

    def get_sprite(self,x,y,w,h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0,0)),(x,y,w,h))
        return sprite




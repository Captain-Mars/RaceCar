import pygame
from pygame.sprite import Sprite
import numpy as np


class MapDot(Sprite):

    def __init__(self,game):
        super().__init__()
        self.width = 10
        self.height =10
        self.screen = game.screen
        #self.screen_rect = game.screen.get_rect()
        self.rect = pygame.Rect(0,0,self.width,self.height) 
        self.color = (150,200,220)
        self.rect.x = 0
        self.rect.y = 0

    def blitme(self):
        pygame.draw.rect(self.screen,self.color,self.rect)

class CarDot():
    def __init__(self,game):
        self.width = 10
        self.height =10
        self.screen = game.screen
            #self.screen_rect = game.screen.get_rect()
        self.rect = pygame.Rect(0,0,self.width,self.height) 
        self.color = (220,100,100)
        self.rect.x = 0
        self.rect.y = 0

    def update(self,car_pos):
        self.rect.x , self.rect.y= (car_pos[0]/50)+7,(car_pos[1]/50)+690

    def blitme(self):
        #self.screen.blit(self.image,self.rect)
        pygame.draw.rect(self.screen,self.color,self.rect)

        
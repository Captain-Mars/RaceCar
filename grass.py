import pygame
from pygame.sprite import Sprite
import numpy as np


class Grass(Sprite):

    def __init__(self,game):
        super().__init__()
        self.width = 5
        self.height =5
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        #self.image = pygame.image.load("other_image/road.bmp")
        #self.image = pygame.transform.scale(self.image,(self.width,self.height))
        #self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0,0,self.width,self.height)     ####
        #self.rect.x = 0
        #self.rect.y = 0
        self.x = self.screen_rect.width/2
        self.y = self.screen_rect.height/2

        self.y += self.height/2

        self.color = (50,50,50)

        self.rotate_follow = game.rotate_follow
        self._in_sight = False


    def update(self,car,theta):
        self.relative_y = self.y - car.y
        self.relative_x = self.x - car.x
        relative_vector = np.array([self.relative_x,self.relative_y])
        if np.linalg.norm(relative_vector)<1000:
            self._in_sight = True
            #进入视线范围
            if not self.rotate_follow:
                self.rect.x = (car.rect.x + (car.rect.width/2)) + self.relative_x - (self.width/2)
                self.rect.y = (car.rect.y + (car.rect.height/2)) + self.relative_y - (self.height/2)
            else:
                relative_vector = self.rotate_vector(relative_vector,theta)
                self.rect.x = (car.rect.center[0] ) + relative_vector[0]
                self.rect.y = (car.rect.center[1] ) + relative_vector[1]
        else:
            self._in_sight = 0
        

    def rotate_vector(self,v,theta):
        """旋转向量"""
        rotation_matrix = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
        return np.dot(rotation_matrix,v)

    def blitme(self):
        #self.screen.blit(self.image,self.rect)
        pygame.draw.rect(self.screen,self.color,self.rect)
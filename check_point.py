import pygame
import numpy as np


class CheckPoint():

    def __init__(self,game):
        self.width = 20
        self.height =20
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        #self.image = pygame.image.load("other_image/road.bmp")
        #self.image = pygame.transform.scale(self.image,(self.width,self.height))
        #self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0,0,self.width,self.height)     ####
        #self.rect.x = 0
        #self.rect.y = 0
        #self.x = self.screen_rect.width/2
        #self.y = self.screen_rect.height/2

        #self.y += self.height/2

        self.color = (200,200,200)

        self.rotate_follow = game.rotate_follow


    def update(self,x,y):
        
        self.rect.x = x - (self.width/2)
        self.rect.y = y - (self.height/2)

    def rotate_vector(self,v,theta):
        """旋转向量"""
        rotation_matrix = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
        return np.dot(rotation_matrix,v)

    def blitme(self):
        #self.screen.blit(self.image,self.rect)
        pygame.draw.rect(self.screen,self.color,self.rect)
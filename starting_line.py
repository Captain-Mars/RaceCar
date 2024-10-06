import pygame
#from pygame.sprite import Sprite
import numpy as np
import math

class StartingLine():

    def __init__(self,game):
        self.width = 300
        self.height =50
        self.color = (0,0,0)
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        #self.image = pygame.image.load("other_image/road.bmp")
        #self.image = pygame.transform.scale(self.image,(self.width,self.height))
        #self.rect = self.image.get_rect()
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        pygame.draw.rect(self.image,self.color,(0,0,self.width,self.height))
        self.original_image = self.image
        self.rect = self.image.get_rect()    ####
        #self.rect.x = 0
        #self.rect.y = 0
        self.x = self.screen_rect.width/2
        self.y = self.screen_rect.height/2

        self.y += self.height/2 -300
        self.x += 20


        self.rotate_follow = game.rotate_follow


    def update(self,car,theta):
        self.relative_y = self.y - car.y
        self.relative_x = self.x - car.x
        relative_vector = np.array([self.relative_x,self.relative_y])
        if not self.rotate_follow:
            
                self.rect.x = (car.rect.x + (car.rect.width/2)) + self.relative_x - (self.width/2)
                self.rect.y = (car.rect.y + (car.rect.height/2)) + self.relative_y - (self.height/2)
        else:
        #旋转跟随
            
            relative_vector = self.rotate_vector(relative_vector,theta)
            self.display_x = (car.rect.center[0] ) + relative_vector[0]
            self.display_y = (car.rect.center[1] ) + relative_vector[1]
            self.center = self.display_x,self.display_y
            self.rotate_image(theta)

    def rotate_vector(self,v,theta):
        """旋转向量"""
        rotation_matrix = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
        return np.dot(rotation_matrix,v)
    
    def rotate_image(self,theta):
        angle = math.degrees(theta)
        self.image = pygame.transform.rotate(self.original_image,-angle)
        self.rect = self.image.get_rect(center = self.center)

    def blitme(self):
        self.screen.blit(self.image,self.rect)
        #pygame.draw.rect(self.screen,self.color,self.rect)
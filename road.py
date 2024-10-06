import pygame
from pygame.sprite import Sprite
from check_point import CheckPoint
import numpy as np
import math

class Road(Sprite):

    def __init__(self,game):
        super().__init__()
        self.width = 300
        self.height =300
        self.color = (100,100,100)
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        #self.image = pygame.image.load("other_image/road.bmp")
        #self.image = pygame.transform.scale(self.image,(self.width,self.height))
        #self.rect = self.image.get_rect()
        #self.rect = pygame.Rect(0,0,self.width,self.height)     ####
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        pygame.draw.rect(self.image,self.color,(0,0,self.width,self.height))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        #self.rect.x = 0
        #self.rect.y = 0
        self.x = self.screen_rect.width/2
        self.y = self.screen_rect.height/2

        self.y += self.height/2

        self.has_been_passed = False
        self.point = CheckPoint(game)
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
                if self.rect.colliderect(car):
                    self.has_been_passed = True
                if self.has_been_passed:        #检查点check
                    self.color = (100,100,100)
                    self.point.color = (120,120,120)
                else:
                    self.color = (100,100,100)
                    self.point.color = (200,200,200)
                point_x = self.rect.x + (self.width/2)
                point_y = self.rect.y + (self.height/2)
                self.point.update(point_x,point_y)
            else:
            #旋转跟随
                
                relative_vector = self.rotate_vector(relative_vector,theta)
                self.display_x = (car.rect.center[0] ) + relative_vector[0]
                self.display_y = (car.rect.center[1] ) + relative_vector[1]
                self.center = self.display_x,self.display_y
                if self.rect.colliderect(car):
                    self.has_been_passed = True
                if self.has_been_passed:        #检查点check
                    self.color = (100,100,100)
                    self.point.color = (120,120,120)
                else:
                    self.color = (100,100,100)
                    self.point.color = (200,200,200)
                point_x = self.display_x
                point_y = self.display_y
                self.point.update(point_x,point_y)
                self.rotate_image(theta)
        else:
            self._in_sight =False



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
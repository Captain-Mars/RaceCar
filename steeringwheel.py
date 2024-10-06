import pygame


class SteeringWheel():

    def __init__(self,game):
        self.width = 200
        self.height =200
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.original_image = pygame.image.load("other_image/steeringwheel.bmp")
        self.original_image = pygame.transform.scale(self.original_image,(self.width,self.height))
        self.image = pygame.transform.rotate(self.original_image,0)
        self.rect = self.image.get_rect()
        self.x = self.screen_rect.width/2
        self.y = self.screen_rect.height/2


    def update(self,wheel_angle):
        self.image = pygame.transform.rotate(self.original_image,wheel_angle*2)
        self.rect = self.image.get_rect(center = self.screen_rect.center)
        self.rect.y += 250
        self.rect.x += 400
        
        

    def blitme(self):
        self.screen.blit(self.image,self.rect)
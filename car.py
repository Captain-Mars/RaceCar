import pygame
import numpy as np
import math
class Car:

    def __init__(self,game):
        self.rotate_follow = game.rotate_follow
        self.image_width = 100
        self.image_height = 50
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.original_image = pygame.image.load('car_image/greycar.bmp')
        self.original_image = pygame.transform.scale(self.original_image,(self.image_width,self.image_height))
        self.angle = 90 +180
        self.theta = np.deg2rad(self.angle)
        self.direction = np.array([np.cos(self.theta),np.sin(self.theta)])
        self.image = pygame.transform.rotate(self.original_image,self.angle - 180)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.x = float(self.rect.x + (self.image_width/2))
        self.y = float(self.rect.y + (self.image_height/2))

        self.y = float(self.rect.y + (self.image_height/2)) - 400

        self.mass = 1
        #self.accelerated_velocity = np.array([0,0],dtype=np.float64)
        self.wheel = 0     #方向盘
        self.acc_pedal = bool(0)      #油门
        self.break_pedal = bool(0)    #刹车
        self.velocity = np.array([0,0],dtype=np.float64)
        self.velocity_theta = np.pi/2 - np.pi
        self.delta_v = np.array([0,0],dtype=np.float64)
        self.delta_v_norm = 0
        self.speed = np.linalg.norm(self.velocity)
        self.position_vector = np.array([self.direction[1],-self.direction[0]],dtype=np.float64)    #指向圆心的单位向量
        self.power = 0.3
        if  not self.speed == 0:
            self.accelerator = (self.power/self.speed)/self.mass
        else:
            self.accelerator = 0.5
        self.breaking = 0.1
        self.turning_radius = self.wheel*5
        self.angular_v = 1
        self.centripetal_force = np.array([0,0],dtype=np.float64)
        self.force_magnitude = 0

        self.roads = game.roads
        

        self.slip = bool(0)


        self.c_force_limit = 8
        self.slip_f = self.c_force_limit/12      #滑动摩擦力
        self.slip_theta = 0

        self.air_resist = 0.01
        self.grass_resist = 0.07
        self.gear = 1

        self.wheel_right_active = bool(0)
        self.wheel_left_active = bool(0)

        self.mouse_active = game.mouse_active
        if self.rotate_follow:
            self.init_pos_x = self.screen_rect.width/2
            self.init_pos_y = self.screen_rect.height/2 + 200
            self.init_pos = (self.init_pos_x,self.init_pos_y)
        else:
            self.init_pos_x = self.screen_rect.width/2
            self.init_pos_y = self.screen_rect.height/2
            self.init_pos = (self.init_pos_x,self.init_pos_y)
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect(center = self.init_pos)



    def update(self):
        before_velocity = np.array(self.velocity.copy())
        self.steering_wheel()
        self.pedal()
        self.c_force()
        self.resist()
        self.rotate()
        self.accelerate()

        after_velocity = np.array(self.velocity.copy())
        if not self.speed == 0:
            self.velocity_theta = math.atan2(self.velocity[1],self.velocity[0])
        self.delta_v = (after_velocity - before_velocity)
        self.delta_v_norm = np.linalg.norm(self.delta_v)
        #print(self.theta)
        


    def steering_wheel(self):
        if not self.mouse_active:
            if self.wheel_right_active and self.wheel <= 100:
                self.wheel += 2
            elif self.wheel_left_active and self.wheel >= -100:
                self.wheel -= 2
            else:
                if self.wheel > 0:
                    self.wheel -= 2
                elif self.wheel < 0:
                    self.wheel += 2

        if not self.wheel == 0 :
            self.turning_radius = 200/self.wheel
        else:
            self.turning_radius = 0
        self.position_vector = np.array([self.direction[1],-self.direction[0]])    #指向圆心的单位向量

    def pedal(self):
        if  not self.speed == 0:
            self.accelerator = (self.power/self.speed)/self.mass
        else:
            self.accelerator = 0.5
        if not self.slip:
            if self.acc_pedal:
                if self.gear == 1:
                    self.velocity += self.direction * self.accelerator * self.gear
                elif self.gear == -1:
                    self.velocity += self.direction * self.accelerator * self.gear
            if self.break_pedal:
                if self.speed > 0.5:
                    self.velocity -= self.direction * self.breaking * self.gear
        else:
            self.accelerator = (self.power/self.speed)/self.mass
            if self.acc_pedal:
                if self.gear == 1:
                    self.velocity += self.direction * self.accelerator * self.gear
                elif self.gear == -1:
                    if self.speed <= 3:
                        self.velocity += self.direction * self.accelerator * self.gear
            if self.break_pedal:
                if self.speed > 0.5:
                    pass                                                           



    def accelerate(self):          
        self.speed = np.linalg.norm(self.velocity)
        self.x += 2*self.velocity[0]       ###乘2为了适配帧率
        self.y -= 2*self.velocity[1]        ###乘2为了适配帧率

    def is_on_road(self):
        collisions = pygame.sprite.spritecollideany(self , self.roads)
            
        if  not collisions:
            return False
        else:
            return True


    def resist(self):
        if self.is_on_road():
            if not self.slip:
                if self.speed >= 0.05:
                    self.velocity -= (self.velocity/np.linalg.norm(self.velocity))*self.air_resist
                elif not self.acc_pedal:
                    self.velocity = [0,0]
                    self.speed = 0
            else:
                if self.speed >= 0.05:
                    self.velocity -= (self.velocity/np.linalg.norm(self.velocity))*self.air_resist
                elif not self.acc_pedal:
                    self.velocity = [0,0]
                    self.speed = 0
        else:
            if not self.slip:
                if self.speed >= 0.05:
                    self.velocity -= (self.velocity/np.linalg.norm(self.velocity))*self.grass_resist
                elif not self.acc_pedal:
                    self.velocity = [0,0]
                    self.speed = 0
            else:
                if self.speed >= 0.05:
                    self.velocity -= (self.velocity/np.linalg.norm(self.velocity))*self.grass_resist
                elif not self.acc_pedal:
                    self.velocity = [0,0]
                    self.speed = 0



    def c_force(self):
        if not self.slip:
            if not self.turning_radius == 0:
                self.force_magnitude = (self.mass * self.speed**2) / self.turning_radius
            else:
                self.force_magnitude = 0

            if abs(self.force_magnitude) > self.c_force_limit:      #检查是否打滑
                self.slip = 1
                if not self.wheel == 0:
                    self.angle -= (self.wheel/abs(self.wheel)) * 6 * self.gear
                #self.sliping()
                return

            self.centripetal_force = self.force_magnitude * (self.position_vector) * 0.05 
            self.speed = np.linalg.norm(self.velocity)
            self.velocity += self.centripetal_force * (1/self.mass)
            #校准向心力作用后的速度
            if  self.speed > 3 and self.turning_radius != 0:
                self.velocity  *= (self.speed)/np.linalg.norm(self.velocity)
            else:
                pass
        else:
            #打滑情况
            self.sliping()

    def sliping(self):
        """打滑"""
        #计算打滑角度
        dot_product = np.dot(self.velocity,self.direction*self.gear)
        norm_v = np.linalg.norm(self.velocity)
        norm_d = np.linalg.norm(self.direction*self.gear)
        cos_theta = dot_product / (norm_v * norm_d)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        self.slip_theta = np.arccos(cos_theta)
        #计算打滑方向
            #先算sin值
        cross_product = np.cross(self.velocity,self.direction*self.gear)
        norm_cross = np.linalg.norm(cross_product)
        sin_theta = norm_cross / (norm_v * norm_d)
        sin_theta = np.clip(sin_theta, -1.0, 1.0)
            #通过叉乘正负判断方向
        if  cross_product > 0:
            force_direction = -1
        elif cross_product < 0:
            force_direction = +1
        else:
            force_direction = 0
        #计算v在direction上的投影向量
        norm_d_squared = np.dot(self.direction*self.gear,self.direction*self.gear)
        projection = (dot_product / norm_d_squared) * self.direction*self.gear
        projection_norm = np.linalg.norm(projection)
        #计算向心力
        self.position_vector = projection - self.velocity
        #max_force_norm = np.linalg.norm(self.velocity)*abs(sin_theta)
        if not self.wheel == 0:
            self.force_magnitude = (self.slip_f)#*self.gear#*force_direction
        else:
            self.force_magnitude = 0
        self.centripetal_force = self.force_magnitude * (self.position_vector) * 0.05
        centripetal_force_norm = np.linalg.norm(self.centripetal_force)
        self.velocity += self.centripetal_force * (1/self.mass)
        #漂移时踩刹车情况
        if self.break_pedal and projection_norm != 0:
            breaking_force = -1*projection*((self.slip_f)/projection_norm)*0.05
            self.velocity += breaking_force * (1/self.mass)

            
            

        if abs(self.slip_theta) < 0.1:
            self.slip = 0
        


    def rotate(self):
        if not self.slip:
            if not self.speed == 0:
                self.angle = np.rad2deg(np.arctan2(self.velocity[1]*self.gear,self.velocity[0]*self.gear))
        elif not self.speed == 0:
            self.angle -= (self.wheel/8)*self.gear  
        else:
            self.slip = 0 
        self.theta = np.deg2rad(self.angle)
        self.direction = np.array([np.cos(self.theta),np.sin(self.theta)])
        if not self.rotate_follow:
            self.rotate_image(self.angle)
        else:
            self.rotate_image(90 + self.angle - math.degrees(self.velocity_theta))

    def rotate_image(self,angle):
        self.image = pygame.transform.rotate(self.original_image,angle)
        self.rect = self.image.get_rect(center = self.init_pos)

        

    def blitme(self):
        self.screen.blit(self.image,self.rect)

import pygame
import sys
from car import Car
from road import Road
import math
from grass import Grass
from starting_line import StartingLine
from steeringwheel import SteeringWheel
from random import randint
from time import time       #仅用于赛车跑圈计时
import numpy as np
from map_dot import MapDot , CarDot

class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.default = 0
        if not self.default:
            print('鼠标控制:右键油门,左键刹车,滚轮键或shift按下换挡。    键盘控制：使用方向键。。。      退出:Esc   ')
            reply = input("是否开启鼠标控制？（是请输入'yes',否输入任意)")
            if reply == 'yes':
                self.mouse_active = bool(1)#鼠标控制模式
            else:
                self.mouse_active = bool(0)#鼠标控制模式off
            reply = input("是否开启屏幕车头追踪？（是请输入'yes',否输入任意)")
            if reply == 'yes':
                self.rotate_follow = 1
            else:
                self.rotate_follow = 0
            reply = input("是否开启全屏？（是请输入'yes',否输入任意)")
            if reply == 'yes':
                self.screen = pygame.display.set_mode((1200,800),pygame.FULLSCREEN)   #,pygame.FULLSCREEN
            else:
                self.screen = pygame.display.set_mode((1200,800))
        else:
            self.mouse_active = bool(1)#鼠标控制模式
            self.rotate_follow = 1
            self.screen = pygame.display.set_mode((1200,800))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Car Simulator')
        self.roads = pygame.sprite.Group()
        self._create_roads()
        self.grass_group = pygame.sprite.Group()
        self._create_grass_group()
        self.map = pygame.sprite.Group()
        self._create_map()
        self.startingline =  StartingLine(self)
        self.steeringwheel = SteeringWheel(self)
        self.greycar = Car(self)
        self.fps = 30
        self.start_time = 0
        self.finish_time = 0
        self.timing = False
        self.lap_finished = False
        self.screen_theta = self.greycar.theta
        self.current_fps = 0
        self.greycar_pos = (self.greycar.x,self.greycar.y,self.greycar.theta)
        self.greycardot = CarDot(self)


    def run_game(self):
        """运行模拟器"""
        self._reset_data()
        while True:
            self._check_event()
            if self.mouse_active:
                self._mouse_control()
            self.greycar.update()
            self.greycar_pos = (self.greycar.x,self.greycar.y,self.greycar.theta)
            self.greycardot.update(self.greycar_pos)
            self.screen_follow()
            self._check_starting_line()
            self.steeringwheel.update(-self.greycar.wheel*2)
            self.update_screen()
            self.clock.tick(self.fps)
            self.current_fps = self.clock.get_fps()


    def _reset_data(self):
        """重置数据"""
        self.startingline.update(self.greycar,np.pi)
        for road in self.roads.sprites():
            road.has_been_passed = False

    def _check_event(self):
        """侦测键盘"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.greycar.acc_pedal = 1
                if event.button == 1 :
                    self.greycar.break_pedal = 1
                if event.button == 2:
                    if self.greycar.speed == 0:
                        self.greycar.gear *= -1

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.greycar.acc_pedal = 0
                if event.button == 1 :
                    self.greycar.break_pedal = 0


    def _mouse_control(self):
        """用鼠标控制ship"""
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos_x = mouse_pos[0]
        self.mouse_pos_y = mouse_pos[1]
        self.greycar.wheel = (self.mouse_pos_x - (self.screen_rect.width/2))*(35/(self.screen_rect.width/2))


    def _check_keydown(self,event):
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        
        if event.key == pygame.K_RIGHT:

            self.greycar.wheel_right_active = 1
            self.greycar.wheel_left_active = 0
 
        elif event.key == pygame.K_LEFT:
            
            self.greycar.wheel_right_active = 0
            self.greycar.wheel_left_active = 1
                
        if event.key == pygame.K_UP:
            self.greycar.acc_pedal = 1
        if event.key == pygame.K_DOWN :
            self.greycar.break_pedal = 1
        if event.key == pygame.K_LSHIFT:
            if self.greycar.speed == 0:
                self.greycar.gear *= -1
        elif event.key == pygame.K_RSHIFT:
            if self.greycar.speed == 0:
                self.greycar.gear *= -1


    def _check_keyup(self,event):
        if event.key == pygame.K_RIGHT:
            self.greycar.wheel_right_active = 0
        elif event.key == pygame.K_LEFT:
            self.greycar.wheel_left_active = 0

        if event.key == pygame.K_UP:
            self.greycar.acc_pedal = 0
        elif event.key == pygame.K_DOWN:
            self.greycar.break_pedal = 0

    def screen_follow(self):
        """屏幕跟随汽车"""
        rotate_theta = self.greycar.velocity_theta - self.screen_theta - np.pi
        for road in self.roads.sprites():
            road.update(self.greycar,rotate_theta)
        for grass in self.grass_group.sprites():
            grass.update(self.greycar,rotate_theta)
        self.startingline.update(self.greycar,rotate_theta)


    def rotate_vector(self,v,theta):
        """旋转向量"""
        rotation_matrix = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
        return np.dot(rotation_matrix,v)



    def update_screen(self):
        """屏幕刷新"""
        self.screen.fill((10,80,30))
        for road in self.roads.sprites():
            if road._in_sight:
                road.blitme()
        for grass in self.grass_group.sprites():
            if grass._in_sight:
                grass.blitme()
        for road in self.roads.sprites():
            if road._in_sight:
                road.point.blitme()
        self.startingline.blitme()
        for dot in self.map.sprites():
            dot.blitme()
        self.greycardot.blitme()
        self._show_gear()
        self._show_pedal()
        self._show_speed()
        self._show_delta_v()
        self._show_warning()
        self._show_time()
        self._show_fps()
        self.steeringwheel.blitme()
        self.greycar.blitme()

        pygame.display.flip()

    def _create_roads(self):
        road = Road(self)
        self.roads.add(road)
        road_width , road_height = road.rect.size
        a=0
        current_x , current_y =  self.track(road.x,road.y,a)
        while a<5*math.pi-1.6 :
            current_x , current_y =  self.track(road.x,road.y,a)
            self.create_road(current_x , current_y)
            a+=0.015

    def _create_map(self):
        dot = MapDot(self)
        self.map.add(dot)
        a=0
        current_x , current_y =  self.track(0,0,a)
        while a<5*math.pi-1.6 :
            current_x , current_y =  self.track(0,0,a)
        
            self.create_mapdot((current_x/50)+20,(current_y/50)+700)
            a+=0.01

    def create_mapdot(self,x , y):
        new_dot = MapDot(self)
        new_dot.rect.x = int(x)
        new_dot.rect.y = int(y)
        self.map.add(new_dot)

    def create_road(self,x , y):
        new_road = Road(self)
        new_road.x = x
        new_road.y = y
        self.roads.add(new_road)

    def _create_grass_group(self):
        grass = Grass(self)
        self.grass_group.add(grass)
        road_width , road_height = grass.rect.size
        a=0
        current_x , current_y =  self.track(grass.x,grass.y,a)
        current_x += randint(-4000,4000)
        current_y += randint(-4000,4000)
        while a<5*math.pi-1.6 :
            current_x , current_y =  self.track(grass.x,grass.y,a)
            current_x += randint(-4000,4000)
            current_y += randint(-4000,4000)
            self.create_grass(current_x , current_y)
            a+=0.005

    def create_grass(self,x , y):
        new_grass = Grass(self)
        new_grass.x = x
        new_grass.y = y
        self.grass_group.add(new_grass)



    def track(self,x,y,a):
        """
        计算赛道轨迹；
        x:初始x坐标
        y:初始y坐标
        a:自变量
        """
        pi = math.pi
        if a < pi/2:
            current_x , current_y =  x + 5000*(1-math.cos(a)) , y - 5000*(math.sin(a))
        elif a < pi*5/8:
            current_x , current_y = x + 5000 * ((1-math.cos(pi/2)) ), y - 5000*(math.sin(pi/2)) -  5000*(a - (pi/2))
        elif a < pi*6/8:
            current_x , current_y = x + 5000 * ((1-math.cos(pi/2)) ) + 5000*(a - (pi*5/8)), y - 5000*(math.sin(pi/2)) -  5000*(pi*5/8 - (pi/2))
        elif a < pi*7/8:
            current_x , current_y = x + 5000 * ((1-math.cos(pi/2)) ) + 5000*(pi*6/8 - (pi*5/8)) +  10000*(a - (pi*6/8)), y - 5000*(math.sin(pi/2)) -  5000*(pi*5/8 - (pi/2)) + 5000*(a - (pi*6/8))
        elif a < pi:
            current_x , current_y = x + 5000 * ((1-math.cos(pi/2)) ) + 5000*(a - (pi/2)), y - 5000*(math.sin(pi/2))
        elif a < 2*pi:
            current_x , current_y = x + 5000 * ((1-math.cos(pi/2)) ) + 5000*(pi/2) + 2500*(math.sin(a-pi)) , y - 5000*(math.sin(pi/2)) + 2500*(1-math.cos(a-pi))

        elif a < 4*pi:
            current_x , current_y = x + 5000 * ((1-math.cos(pi/2)) ) + 5000*(pi/2) + 2500*(math.sin(pi)) -1250*(a-(2*pi)) , y - 5000*(math.sin(pi/2)) + 2500*(1-math.cos(pi)) - 2500*math.sin(a-(2*pi))
        elif a < (9/2)*pi:
            current_x , current_y = x + 5000 * ((1-math.cos(pi/2)) ) + 5000*(pi/2) + 2500*(math.sin(pi)) -1250*(2*pi) - pi*1000*(a - (4*pi)), y - 5000*(math.sin(pi/2)) + 2500*(1-math.cos(pi)) - 2500*math.sin(2*pi)
        else:
            current_x , current_y = 600 , 400

        return (current_x , current_y)


    def _show_gear(self):
        self.font = pygame.font.SysFont('arial',50)
        if self.greycar.gear == 1:
            image = self.font.render("D",True,(255,255,255))
        elif self.greycar.gear == -1:
            image = self.font.render("R",True,(255,255,255))
        image_rect = image.get_rect()
        image_rect.center = self.screen_rect.center
        image_rect.y -= 350
        image_rect.x -= 550
        self.screen.blit(image,image_rect)

    def _show_speed(self):
        self.font = pygame.font.SysFont('arial',50)
        speed = round(self.greycar.speed*10)
        image = self.font.render(f"{speed}kph",True,(255,255,255))
        image_rect = image.get_rect()
        image_rect.center = self.screen_rect.center
        image_rect.y -= 350
        image_rect.x += 500
        self.screen.blit(image,image_rect)

    def _show_fps(self):
        self.font = pygame.font.SysFont('arial',20)
        fps = round(self.current_fps)
        image = self.font.render(f"{fps}fps",True,(255,255,255))
        image_rect = image.get_rect()
        image_rect.center = self.screen_rect.center
        image_rect.y -= 250
        image_rect.x -= 500
        self.screen.blit(image,image_rect)


    def _show_delta_v(self):
        self.font = pygame.font.SysFont('arial',30)
        a = round((((self.greycar.delta_v_norm*self.fps*10)/3.6)/9.8),1)
        image = self.font.render(f"a:{a}g",True,(255,255,255))
        image_rect = image.get_rect()
        image_rect.center = self.screen_rect.center
        image_rect.y -= 300
        image_rect.x += 500
        self.screen.blit(image,image_rect)

    def _show_pedal(self):
        self.font = pygame.font.SysFont('arial',50)
        if self.greycar.acc_pedal == 1:
            image = self.font.render("accelerating",True,(255,255,255))
        elif self.greycar.break_pedal == 1:
            image = self.font.render("breaking",True,(255,255,255))
        else:
            image = self.font.render("---",True,(255,255,255))
        image_rect = image.get_rect()
        image_rect.center = self.screen_rect.center
        image_rect.y -= 350
        self.screen.blit(image,image_rect)

    def _show_warning(self):
        self.font = pygame.font.SysFont('arial',50)
        speed = round(self.greycar.speed*10)
        if self.greycar.slip:
            image = self.font.render(f"sliping!",True,(255,255,255))
        else:
            image = self.font.render(f"-",True,(255,255,255))
        image_rect = image.get_rect()
        image_rect.center = self.screen_rect.center
        image_rect.y -= 200
        image_rect.x += 500
        self.screen.blit(image,image_rect)

    def _show_time(self):
        self.font = pygame.font.SysFont('arial',50)
        collision = self.startingline.rect.colliderect(self.greycar)
        if not collision:           #修复起点处奇怪时间的bug
            lap_time = round(self.finish_time - self.start_time,1)
        else:
            lap_time = '-'
        image = self.font.render(f"{lap_time}s",True,(255,255,255))
        image_rect = image.get_rect()
        image_rect.center = self.screen_rect.center
        image_rect.y -= 300
        image_rect.x -= 500
        self.screen.blit(image,image_rect)

    def _check_starting_line(self):
        collision = self.startingline.rect.colliderect(self.greycar)
        if collision and self.timing == False and time()>self.finish_time + 3:
            self.timing = True
            self._reset_data()
            self.start_time = time()
        elif collision and self.timing == True:
            if self._lap_finished():
                self.timing = False
                self.finish_time = time()
        elif self.timing:
            self.finish_time = time()
    def _lap_finished(self):
        for road in self.roads.sprites():
            if not road.has_been_passed:
                return False
        return True
    





if __name__ == "__main__":
    try:
        """报错侦测"""
        game = Game()
        game.run_game()

    except Exception as e:
        print(f"Error:{e}")
    finally:
        """强制退出"""
        pygame.quit()
        sys.exit()
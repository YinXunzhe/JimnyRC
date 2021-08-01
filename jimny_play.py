import sys
import pygame
import RPi.GPIO as GPIO                  # 引入GPIO模块

from settings import Settings
from jimny import Jimny

class JimnyPlay:
    """控制吉姆尼小车的类"""

    def __init__(self,play_mode='keyboard'):
        """"初始化设置
        args:
            play_mode： 控制模式，‘keyboard’ or ‘controller’
        """

        self.play_mode=play_mode
        self.settings=Settings()
        self.jimny=Jimny(self)

        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        # TODO
        # 增加小车可视化界面

        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def play(self):
        """开始控制小车"""
        self.jimny.initialize()
        while True:
            if self.play_mode == 'keyboard':
                self._check_key_events()
            elif self.play_mode == 'controller':
                self._check_controller_events()
            self.jimny.update()

    def _check_key_events(self):
        # 监视键盘
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.jimny.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.jimny.moving_left = True
        elif event.key == pygame.K_UP:
            self.jimny.moving_stop=False
            self.jimny.moving_forward = True
        elif event.key == pygame.K_DOWN:
            self.jimny.moving_stop=False
            self.jimny.moving_back = True
        elif event.key == pygame.K_SPACE:
            self.jimny.moving_stop = not self.jimny.moving_stop
        elif event.key == pygame.K_w:
            self.jimny.speed_up = True
        elif event.key == pygame.K_s:
            self.jimny.slow_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.jimny.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.jimny.moving_left = False
        elif event.key == pygame.K_UP:
            self.jimny.moving_forward = False
        elif event.key == pygame.K_DOWN:
            self.jimny.moving_back = False
        elif event.key == pygame.K_w:
            self.jimny.speed_up = False
        elif event.key == pygame.K_s:
            self.jimny.slow_down = False

    def _check_controller_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.JOYBUTTONDOWN:
                self._check_joy_button_down(event)
            elif event.type == pygame.JOYBUTTONUP:
                self._check_joy_button_down(event)
            elif event.type == pygame.JOYAXISMOTION:
                self._check_joy_axis_motion(event)

    def _check_joy_button_down(self,event):
        # A0 B1 X3 Y4
        button_B = self.joystick.get_button(1)
        if button_B:
            sys.exit()
        # button_X = self.joystick.get_button(3)
    def _check_joy_button_up(self,event):
        pass
    def _check_joy_axis_motion(self,event):
        # 控件与axis序号的对应关系：
        # LS 0（左-1,右1）,1（上-1,下1）；RS 2（左-1,右1） 3（上-1,下1）；
        # LT 5（顶-1,底1）, RT 4（顶-1,底1）,按下扳机前读到的初始值为0，之后为-1
        # 左扳机控制速度大小
        # 按下扳机前会读到0,而非-1,导致马达转动，所以把0忽略掉
        if self.joystick.get_axis(5) != 0:
            self.settings.speed_axis_pos= self.joystick.get_axis(5)
            print(f'speed_axis_pos:{self.settings.speed_axis_pos}\n')
        # 左摇杆控制转向和前进方向
        left_stick_x=self.joystick.get_axis(0)
        # left_stick_x=round(self.joystick.get_axis(0),1)
        left_stick_y=self.joystick.get_axis(1)
        # 左转右转
        # FIXME
        # 摇杆的移动大于一定阈值时才进行转向控制
        # if (abs(left_stick_x - self.settings.steer_axis_pos) > self.settings.steer_axis_delta):
        if True:
            self.settings.steer_axis_flag = True
            self.settings.steer_axis_pos = left_stick_x
            print(f'steer_axis_pos:{self.settings.steer_axis_pos}\n')
        else:
            self.settings.steer_axis_flag = False

        # 前进后退
        if left_stick_y > 0.5:
            self.jimny.moving_back = True
        elif left_stick_y < -0.5:
            self.jimny.moving_forward = True
        else:
            self.jimny.moving_back = False
            self.jimny.moving_forward = False

if __name__ == '__main__':

    # my_jimny=JimnyPlay()
    my_jimny=JimnyPlay(play_mode='controller')
    my_jimny.play()

    GPIO.cleanup()  # 清理释放GPIO资源，将GPIO复位


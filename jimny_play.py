import sys
import pygame
import RPi.GPIO as GPIO                  # 引入GPIO模块

from settings import Settings
from jimny import Jimny

class JimnyPlay:
    """控制吉姆尼小车的类"""

    def __init__(self):
        """"初始化小车的设置"""

        self.settings=Settings()
        self.jimny=Jimny(self)

        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))


    def play(self):
        """开始控制小车"""
        self.jimny.initialize()
        while True:
            self._check_events()
            self.jimny.update()

    def _check_events(self):
        # 监视鼠标和键盘
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
            self.jimny.moving_forward = True
        elif event.key == pygame.K_DOWN:
            self.jimny.moving_back = True
        elif event.key == pygame.K_SPACE:
            self.jimny.moving_stop = True
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
        elif event.key == pygame.K_SPACE:
            self.jimny.moving_stop = False

if __name__ == '__main__':

    my_jimny=JimnyPlay()
    my_jimny.play()

    GPIO.cleanup()  # 清理释放GPIO资源，将GPIO复位


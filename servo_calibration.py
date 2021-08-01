# 寻找车轮转动角度和舵机占空比关系
# 7.5约为正前，向左最大到9，向右最大到6
import sys

import RPi.GPIO as GPIO
from settings import Settings
from jimny import Jimny
from jimny_play import JimnyPlay

class JimnyCal(JimnyPlay):
    """进行校正的类"""

    def __init__(self):
        super().__init__()

    def calibration(self):
        self.jimny.initialize()
        try:
            while True:
                # 输入不同的占空比，观察小车车轮角度
                dc = float(input("Please input the duty cycle(0-100): "))  # 等待输入新PWM占空比
                self.jimny.pwm_steer.ChangeDutyCycle(dc)  # 改变PWM占空比
        finally:
            self.jimny.pwm_steer.stop()  # 停止PWM
            self.jimny.pwm_motor.stop()  # 停止PWM
            sys.exit()

if __name__ == '__main__':
    jimny_cal=JimnyCal()
    jimny_cal.calibration()

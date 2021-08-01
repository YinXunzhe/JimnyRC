import RPi.GPIO as GPIO
import time


class Jimny:
    """吉姆尼小车"""
    def __init__(self, jimny_play):

        self.settings = jimny_play.settings
        self.steer_wait = 1 / self.settings.steer_sens
        self.play_mode = jimny_play.play_mode

        self.moving_right = False
        self.moving_left = False
        self.moving_forward = False
        self.moving_back = False
        self.moving_stop = False
        self.speed_up = False
        self.slow_down = False
        self.speed_axis = 0

        self.pwm_steer = GPIO.PWM(self.settings.steer_pin, self.settings.steer_freq)  # 创建PWM对象，并指定初始频率
        self.pwm_motor = GPIO.PWM(self.settings.motor_pin, self.settings.motor_freq)  # 创建PWM对象，并指定初始频率

    def initialize(self):
        self.pwm_steer.start(self.settings.steer_dc)  # 启动PWM，并指定初始占空比
        time.sleep(0.04)    # 等待控制周期结束
        self.pwm_steer.ChangeDutyCycle(0) # 清空占空比，防止抖动
        self.pwm_motor.start(self.settings.motor_dc)  # 启动PWM，并指定初始占空比
        GPIO.output(self.settings.motor_dir_pin, GPIO.HIGH)     # 设定行驶方向向前

    def update(self):
        """控制程序"""
        # 转向控制
        if self.moving_right and not self.moving_left:
            self.settings.steer_dc -= self.settings.steer_step
            if self.settings.steer_dc < 6:  # 限制在车轮最大右转角度对应的占空比范围内
                self.settings.steer_dc = 6
            self.pwm_steer.ChangeDutyCycle(self.settings.steer_dc)
            time.sleep(self.steer_wait)  # 加入延时，防止瞬间打死方向
            self.pwm_steer.ChangeDutyCycle(0)   # 清空占空比，防止抖动
        if self.moving_left and not self.moving_right:
            self.settings.steer_dc += self.settings.steer_step
            if self.settings.steer_dc > 9:  # 限制在车轮最大左转角度对应的占空比范围内
                self.settings.steer_dc = 9
            self.pwm_steer.ChangeDutyCycle(self.settings.steer_dc)
            time.sleep(self.steer_wait)  # 加入延时，防止瞬间打死方向
            self.pwm_steer.ChangeDutyCycle(0)   # 清空占空比，防止抖动

        # 前进方向和速度控制
        if self.slow_down:
            self.settings.motor_dc -= 5
            if self.settings.motor_dc < 0:  # 电机最小占空比
                self.settings.motor_dc = 0
            time.sleep(0.2)
            self.pwm_motor.ChangeDutyCycle(self.settings.motor_dc)
        if self.speed_up:
            self.settings.motor_dc += 5
            if self.settings.motor_dc > 80:  # 电机最大占空比
                self.settings.motor_dc = 80
            time.sleep(0.2)
            self.pwm_motor.ChangeDutyCycle(self.settings.motor_dc)
        if not self.moving_stop:
            self.pwm_motor.start(self.settings.motor_dc)  # 防止之前已经关闭电机PWM
            if self.moving_forward:
                GPIO.output(self.settings.motor_dir_pin, GPIO.HIGH)
            elif self.moving_back:
                GPIO.output(self.settings.motor_dir_pin, GPIO.LOW)
        else:
            self.pwm_motor.stop()
            self.moving_forward = False
            self.moving_back = False
            if self.settings.motor_dc >30:    # 防止下次重新启动时速度过大
                self.settings.motor_dc =30

        if self.play_mode == 'controller':
            self.settings.motor_dc = 30*self.speed_axis   # speed： 0-2 ，dc：0-60
            self.pwm_motor.ChangeDutyCycle(self.settings.motor_dc)

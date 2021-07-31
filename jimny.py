import RPi.GPIO as GPIO
class Jimny:
    """吉姆尼小车"""

    def __init__(self,jimny_play):

        self.settings=jimny_play.settings

        self.moving_right=False
        self.moving_left = False
        self.moving_forward=False
        self.moving_back = False
        self.moving_stop = False

        self.pwm_steer = GPIO.PWM(self.settings.steer_pin, self.settings.steer_freq)  # 创建PWM对象，并指定初始频率
        self.pwm_motor = GPIO.PWM(self.settings.motor_pin, self.settings.motor_freq)  # 创建PWM对象，并指定初始频率

    def initialize(self):

        self.pwm_steer.start(self.settings.steer_dc)  # 启动PWM，并指定初始占空比
        self.pwm_motor.start(self.settings.motor_dc)  # 启动PWM，并指定初始占空比

    def update(self):

        if self.moving_right:
            self.settings.steer_dc=2
            self.pwm_steer.ChangeDutyCycle(self.settings.steer_dc)
        elif self.moving_left:
            self.settings.steer_dc=10
            self.pwm_steer.ChangeDutyCycle(self.settings.steer_dc)
        elif self.moving_forward:
            GPIO.output(self.settings.motor_dir_pin, GPIO.HIGH)
        elif self.moving_back:
            GPIO.output(self.settings.motor_dir_pin, GPIO.LOW)
        elif self.moving_stop:
            self.pwm_motor.stop()
            # TODO
            GPIO.cleanup()  # 清理释放GPIO资源，将GPIO复位

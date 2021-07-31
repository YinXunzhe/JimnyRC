import RPi.GPIO as GPIO                  # 引入GPIO模块

class Settings:
    """存储小车设置的类"""

    def __init__(self):
        """初始化静态设置"""
        self.screen_width=1200
        self.screen_height=800

        self.steer_pin = 6  # 转向舵机PWM引脚
        self.motor_pin = 26  # 驱动电机PWM引脚
        self.motor_dir_pin=19 # 驱动电机方向控制引脚

        GPIO.setmode(GPIO.BCM)  # 使用BCM编号方式
        GPIO.setup(self.steer_pin, GPIO.OUT)  # 将GPIO设置为输出模式
        GPIO.setup(self.motor_pin, GPIO.OUT)  # 将GPIO设置为输出模式
        GPIO.setup(self.motor_dir_pin, GPIO.OUT)  # 将GPIO设置为输出模式

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """初始化动态设置"""
        self.steer_freq = 50  # 舵机PWM频率
        self.steer_dc = 0  # 舵机PWM占空比
        self.motor_freq = 1000  # 电机PWM频率
        self.motor_dc = 30  # 电机PWM占空比

        self.pwm_steer = GPIO.PWM(self.steer_pin, self.steer_freq)  # 创建PWM对象，并指定初始频率
        self.pwm_steer.start(self.steer_dc)  # 启动PWM，并指定初始占空比
        self.pwm_motor = GPIO.PWM(self.motor_pin, self.motor_freq)  # 创建PWM对象，并指定初始频率
        self.pwm_motor.start(self.motor_dc)  # 启动PWM，并指定初始占空比
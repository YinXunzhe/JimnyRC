import RPi.GPIO as GPIO                  # 引入GPIO模块

class Settings:
    """存储设置的类"""

    def __init__(self):
        """初始化静态设置"""
        self.screen_width=1200
        self.screen_height=800

        self.steer_pin = 6  # 转向舵机PWM引脚
        self.motor_pin = 26  # 驱动电机PWM引脚
        self.motor_dir_pin=19 # 驱动电机方向控制引脚
        self.steer_freq = 50  # 舵机PWM频率
        self.motor_freq = 1000  # 电机PWM频率

        GPIO.setmode(GPIO.BCM)  # 使用BCM编号方式
        GPIO.setup(self.steer_pin, GPIO.OUT)  # 将GPIO设置为输出模式
        GPIO.setup(self.motor_pin, GPIO.OUT)  # 将GPIO设置为输出模式
        GPIO.setup(self.motor_dir_pin, GPIO.OUT)  # 将GPIO设置为输出模式

        """初始化动态设置"""
        self.steer_dc = 7.5  # 舵机PWM占空比
        self.steer_step=0.25  # 键盘控制时的转向步长
        self.steer_sens_keyboard=10   # 键盘控制的转向灵敏度 1-10
        self.motor_dc = 0  # 电机PWM占空比

        # 用于手柄控制的变量
        self.speed_axis_pos = -1    # 控制速度的轴读数
        # self.steer_axis_pos_last = 0 # 上次控制方向的轴读数，左负右正
        # self.steer_axis_pos = 0     # 本次控制方向的轴读数，左负右正
        # self.steer_axis_flag = False
        self.steer_dc_last=7.5  # 记录的上一次转向占空比
        self.steer_finish_flag = True  # 完成一次转向控制的标志
        self.steer_sens_joystick=5  # 手柄控制的转向灵敏度
        self.steer_dc_delta=1 / self.steer_sens_joystick

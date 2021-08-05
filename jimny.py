import RPi.GPIO as GPIO
import time


class Jimny:
    """吉姆尼小车"""
    def __init__(self, jimny_play):

        self.settings = jimny_play.settings
        self.play_mode = jimny_play.play_mode

        self.steer_angle = 0    # 车轮转向角度，0度为正前，左负右正
        self.steer_wait = 1 / self.settings.steer_sens_keyboard # 转向变化时的等待时间，防止过快打死

        self.moving_right = False
        self.moving_left = False
        self.moving_forward = False
        self.moving_back = False
        self.moving_stop = False
        self.speed_up = False
        self.slow_down = False

        self.pwm_steer = GPIO.PWM(self.settings.steer_pin, self.settings.steer_freq)  # 创建PWM对象，并指定初始频率
        self.pwm_motor = GPIO.PWM(self.settings.motor_pin, self.settings.motor_freq)  # 创建PWM对象，并指定初始频率

    def initialize(self):
        self.pwm_steer.start(self.settings.steer_dc)  # 启动PWM，并指定初始占空比
        time.sleep(0.04)    # 等待控制周期结束
        self.pwm_steer.ChangeDutyCycle(0) # 清空占空比，防止抖动
        self.pwm_motor.start(self.settings.motor_dc)  # 启动PWM，并指定初始占空比
        GPIO.output(self.settings.motor_dir_pin, GPIO.HIGH)     # 设定行驶方向向前

    def update(self):
        """根据不同的控制模式进行控制"""
        if self.play_mode == 'keyboard':
            self._update_keyboard()
        if self.play_mode == 'controller':
            self._update_controller()

    def _update_keyboard(self):
        """对键盘输入的响应"""
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

    def _update_controller(self):
        """对手柄控制器输入的响应"""
        # 变速  axis value: -1 -> 1 turn to 0->2   # speed： 0-2 ，dc：0-60
        self.settings.motor_dc = 30 * (self.settings.speed_axis_pos + 1)
        self.pwm_motor.ChangeDutyCycle(self.settings.motor_dc)
        #  前进 后退
        if self.moving_forward:
            GPIO.output(self.settings.motor_dir_pin, GPIO.HIGH)
        elif self.moving_back:
            GPIO.output(self.settings.motor_dir_pin, GPIO.LOW)

    def steer(self):
        # 转向
        self.settings.steer_dc = round(-1.5 * self.settings.steer_axis_pos + 7.5,1)  # 占空比与轴读数的关系式
        print(f"compare  (steer_dc):{self.settings.steer_dc}")
        print(f"compare  (steer_dc_last):{self.settings.steer_dc_last}\n")
        # 超过上次的转向占空比一定阈值时才调整
        if abs(self.settings.steer_dc-self.settings.steer_dc_last) > self.settings.steer_dc_step:
            # 开始调整前将转向完成标志置零
            self.settings.steer_finish_flag = False
            print(f"let's change dc to {self.settings.steer_dc}")
            # 按0.1的步长进行调整，使转向平稳
            while abs(self.settings.steer_dc-self.settings.steer_dc_last) > self.settings.steer_dc_step:
                if self.settings.steer_dc>self.settings.steer_dc_last:
                    self.settings.steer_dc_last += self.settings.steer_dc_step
                else:
                    self.settings.steer_dc_last -= self.settings.steer_dc_step
                self._steer_step(self.settings.steer_dc_last)

            self.settings.steer_dc_last=self.settings.steer_dc # 更新记录的占空比
            self.settings.steer_finish_flag = True  # 此次转向调整完成

    def _steer_step(self,step):
        # 按特定角度步进
        self.pwm_steer.ChangeDutyCycle(step)
        time.sleep(0.04)  # 等待控制周期
        self.pwm_steer.ChangeDutyCycle(0)  # 清空占空比，防止抖动



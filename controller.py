# coding:utf-8
import pygame

# 模块初始化
pygame.init()
pygame.joystick.init()

# 若只连接了一个手柄，此处带入的参数一般都是0
joystick = pygame.joystick.Joystick(0)
# 手柄对象初始化
joystick.init()

done = False

clock = pygame.time.Clock()

while not done:
    for event_ in pygame.event.get():
        # 退出事件
        if event_.type == pygame.QUIT:
            done = True
        # 按键按下或弹起事件
        elif event_.type == pygame.JOYBUTTONDOWN or event_.type == pygame.JOYBUTTONUP:
            buttons = joystick.get_numbuttons()
            # 获取所有按键状态信息
            for i in range(buttons):
                button = joystick.get_button(i)
                print("button " + str(i) + ": " + str(button))
        # 轴转动事件
        elif event_.type == pygame.JOYAXISMOTION:
            axes = joystick.get_numaxes()
            # 获取所有轴状态信息
            for i in range(axes):
                axis = joystick.get_axis(i)
                print("axis " + str(i) + ": " + str(axis))
        # 方向键改变事件
        elif event_.type == pygame.JOYHATMOTION:
            hats = joystick.get_numhats()
            # 获取所有方向键状态信息
            for i in range(hats):
                hat = joystick.get_hat(i)
                print("hat " + str(i) + ": " + str(hat))

    joystick_count = pygame.joystick.get_count()

pygame.quit()
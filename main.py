import pygame
from ugot import ugot
import time


got = ugot.UGOT()
# 初始化设备
got.initialize('192.168.50.45')

# 初始化Pygame
pygame.init()

# 获取手柄数量
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joysticks found.")
    quit()

print(f"Number of joysticks found: {joystick_count}")

# 获取第一个手柄对象
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick Name: {joystick.get_name()}")
print(f"Number of Axes: {joystick.get_numaxes()}")
print(f"Number of Buttons: {joystick.get_numbuttons()}")
print(f"Number of Balls: {joystick.get_numballs()}")
print(f"Number of Hats: {joystick.get_numhats()}")

# 防抖函数
def debounce(delay):
    def decorator(func):
        last_call = time.time()

        def debounced(*args, **kwargs):
            nonlocal last_call
            now = time.time()
            elapsed = now - last_call

            if elapsed >= delay:
                last_call = now
                return func(*args, **kwargs)
        return debounced
    return decorator


@debounce(0.5)
def Move(axes,buttons):    
    if buttons[0] == 0:         
        forwardValue = round(axes[1]*150)
        trunValue = round(axes[2]*150) 
        driftValue = round(axes[0]*150)
        # print('forwardValue:',forwardValue)
        # print('trunValue:',trunValue)
        # print('driftValue:',driftValue)
        if abs(forwardValue) > 5 and abs(forwardValue) > abs(trunValue) and abs(forwardValue) > abs(driftValue):
            got.mecanum_motor_control(-forwardValue, -forwardValue, -forwardValue, -forwardValue)
        elif abs(trunValue) > 5 and abs(trunValue) > abs(forwardValue) and abs(trunValue) > abs(driftValue):
            got.mecanum_motor_control(trunValue, -trunValue, trunValue, -trunValue) 
        elif abs(driftValue) > 5 and abs(driftValue) > abs(forwardValue) and abs(driftValue) > abs(trunValue):
            got.mecanum_motor_control(driftValue, -driftValue, -driftValue, driftValue)
            
def MoveArm(axes,buttons):
    if buttons[0] == 1:
        forwardValue = round(axes[1]*85)
        trunValue = round(axes[2]*85) 
        
        # print('forwardValue:',forwardValue)
        # print('trunValue:',trunValue)
        
        if abs(forwardValue) > 5 and abs(forwardValue) > abs(trunValue):
            got.mechanical_single_joint_control(2,forwardValue,20)
        elif abs(trunValue) > 5 and abs(trunValue) > abs(forwardValue):
            got.mechanical_single_joint_control(1,-trunValue,20)        
    armValue = round(axes[3]*90)
    # print('armValue:',armValue)
    if abs(armValue) > 5:
            got.mechanical_single_joint_control(3,armValue,20)
# 打印手柄状态
def print_joypad_state():
    axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    balls = [joystick.get_ball(i) for i in range(joystick.get_numballs())]
    hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]
    
    print("Axis values:", axes)
    print("Button values:", buttons)
    print("Ball values:", balls)
    print("Hat values:", hats)
    if buttons[1] == 1:
        # 机械臂复位
        got.mechanical_arms_restory() 
    if buttons[2] == 1:
        # 闭合夹手
        got.mechanical_clamp_close()
        
    if buttons[3] == 1:
        # 打开夹手
        got.mechanical_clamp_release()
    MoveArm(axes,buttons)
    Move(axes,buttons)
    if abs(round(axes[1]*100)) < 5 and abs(round(axes[2]*360)) < 5 and abs(round(axes[0]*360)) < 5:        
        got.mecanum_stop()    

# 实时监控手柄状态
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
            print_joypad_state()           

# 清理并退出Pygame
pygame.quit()


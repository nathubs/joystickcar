# 超越遥控，进入驾驶席：感受直升飞机操纵杆带来的驾驶乐趣

![](https://aiclassroom.ubtrobot.com/aiengine/resources/cover.png)

​        今天我将向大家展示一个令人兴奋的项目：如何开发一个可以通过直升飞机操纵杆来控制UGOT小车的实现教程。可以自定义控制小车运动及控制机械臂抓取东西，包括但不限于前进、后退、左平移、右平移、左转、右转、抬起或放下机械臂，机械臂左右旋转，张开或夹紧夹子做这个项目将让你的驾驶体验达到一个新的高度。让我们一起开始吧！

## 步骤1：准备所需材料

首先，让我们确保我们准备齐全的材料和工具：

- 优必选可编程UGOT机器人1个
- 飞行游戏摇杆1个
- 一台可以执行python程序的主控（电脑、笔记本、树莓派等）
- ![](https://aiclassroom.ubtrobot.com/aiengine/resources/joystick.jpg)

## 步骤2：连接硬件

接下来，我们将连接硬件以实现操纵杆控制UGOT。

1. 将UGOT按照官方的搭建教程或自行创意搭建好，并将UGOT连接到无线网络。

2. 在UGOT设置界面查看系统信息中的本机IP。确保正确连接，IP信息供主控连接。

3. 将主控制器连接到网络。确保主控可以访问到UGOT机器人。

4. 将游戏摇杆连接主控USB接口。

   

   

## 步骤3：编写代码

现在，让我们编写代码来实现操纵杆控制UGOT的功能。

1. 在你选择的开发环境中打开一个新的项目。

2. 导入UGOT python SDK。

3. 导入pygame 操纵杆控制模块。

4. 编写代码来读取操纵杆的输入，并将其映射到UGOT的运动方向和速度控制以及机械臂控制。

   ```python
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
   
   
   ```
   
   

## 步骤4：测试和调试

一切准备就绪后，我们来测试和调试我们的系统。

1. 打开操纵杆和UGOT的电源。

2. 通过操纵杆的控制杆来控制UGOT运动。尝试前进、后退、转弯和停止等功能，确保一切正常运作。

3. 如果有任何问题，检查代码的逻辑及UGOT模块设置。

   ![](https://aiclassroom.ubtrobot.com/aiengine/resources/control.gif)

## 步骤5：享受驾驶乐趣

恭喜你！你已经成功地开发了一个可以通过飞行操纵杆来控制UGOT小车的系统。

现在，将你的UGOT小车放到一个安全的空间，开始感受驾驶的乐趣吧！通过操纵杆的灵敏度和精确性，你可以体验到更加逼真的驾驶感觉。

记得在合适的环境和遵守当地驾驶规则来使用你的小车，确保安全并尊重他人，安全驾驶。

![](https://aiclassroom.ubtrobot.com/aiengine/resources/fly.gif)



## 步骤6：进一步改进与扩展

你已经成功地实现了通过直升飞机操纵杆来控制UGOT小车了，但这只是一个开始。以下是一些扩展的想法：

1. 添加传感器：通过添加距离传感器、障碍物检测传感器或摄像头等，使你的UGOT小车具备避障功能。
2. 自动驾驶模式：通过编写更复杂的代码及深度学习算法，实现UGOT的自动驾驶功能。例如，根据预设路径或避开障碍物行驶。
3. 远程控制：将无线通信协议升级为能够通过互联网进行远程操控，让你可以在任何地方控制你的UGOT
4. 增加音效和灯光：通过添加声音发生器和LED灯，增强驾驶乐趣和视觉效果。
5. 通过接入UGOT机器人身上的摄像头，接入物体识别算法或其他计算机视觉算法，实现更高端玩法。

记住，不断挑战自己，尝试新的创意和改进，以提升这个项目的乐趣和功能。

## 结论

通过本教程，你学会了如何开发一个可以通过飞行操纵杆来控制你的UGOT小车。从硬件连接到编写代码，再到测试和调试，你迈出了一步步实现这个有趣项目的关键步骤。

希望这个教程能够激发你的创造力，并带给你在驾驶玩具小车时仿佛成为真正驾驶员的紧张刺激感。记得始终保持安全，并享受这个令人兴奋的驾驶乐趣！


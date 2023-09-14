# Beyond Remote Control, Enter the Driver's Seat: Experience the Joy of Driving with a Helicopter Joystick

![](https://aiclassroom.ubtrobot.com/aiengine/resources/cover.png)

​        Today, I'm going to show you an exciting project: a tutorial on how to develop a control system for the UGOT car using a helicopter joystick. You can customize the control of the car's movements and the manipulation of its robotic arm, including but not limited to forward, backward, left translation, right translation, left turn, right turn, raising or lowering the arm, rotating the arm left or right, opening or closing the gripper. This project will take your driving experience to new heights. Let's get started!

## Step 1: Gather the Materials

First, let's make sure we have all the necessary materials and tools:

- 1 programmable UGOT robot by UBTech
- 1 flight game joystick
- A main controller that can execute Python programs (computer, laptop, Raspberry Pi, etc.)
- ![](https://aiclassroom.ubtrobot.com/aiengine/resources/joystick.jpg)

## Step 2: Connect the Hardware

Next, we'll connect the hardware to enable control of the UGOT car with the joystick.

- 1. Assemble the UGOT according to the official build tutorial or your own creative ideas, and connect it to a wireless network.

- 2. Check the local IP address in the UGOT settings interface. Make sure it is connected correctly, as the IP information is needed for the main controller to connect.

- 3. Connect the main controller to the network. Ensure that the main controller can access the UGOT robot.

- 4. Connect the game joystick to the USB port of the main controller.
 

## Step 3: Write the Code

Now, let's write the code to implement joystick control of the UGOT car.

- 1. Open a new project in your chosen development environment.

- 2. Import the UGOT Python SDK.

- 3. Import the pygame joystick control module.

- 4. Write the code to read the joystick input and map it to control the UGOT's motion direction, speed, and robotic arm.

   ```python
   import pygame
   from ugot import ugot
   import time
   
   
   got = ugot.UGOT()
   # Init Device
   got.initialize('192.168.50.45')
   
   # Init Pygame
   pygame.init()
   
   # Get joystick numbers
   joystick_count = pygame.joystick.get_count()
   if joystick_count == 0:
       print("No joysticks found.")
       quit()
   
   print(f"Number of joysticks found: {joystick_count}")
   
   # Get first joystick
   joystick = pygame.joystick.Joystick(0)
   joystick.init()
   
   print(f"Joystick Name: {joystick.get_name()}")
   print(f"Number of Axes: {joystick.get_numaxes()}")
   print(f"Number of Buttons: {joystick.get_numbuttons()}")
   print(f"Number of Balls: {joystick.get_numballs()}")
   print(f"Number of Hats: {joystick.get_numhats()}")
   
   # debounce function
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
   #  joystick state
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
           # arms restory 
           got.mechanical_arms_restory() 
       if buttons[2] == 1:
           # clamp close 
           got.mechanical_clamp_close()
           
       if buttons[3] == 1:
           # clamp release
           got.mechanical_clamp_release()
       MoveArm(axes,buttons)
       Move(axes,buttons)
       if abs(round(axes[1]*100)) < 5 and abs(round(axes[2]*360)) < 5 and abs(round(axes[0]*360)) < 5:        
           got.mecanum_stop()    
   
   
   running = True
   while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
               print_joypad_state()           
   
   # clean and quit
   pygame.quit()
   
   
   ```
   
   

## Step 4: Test and Debug

Once everything is set up, let's test and debug our system.

- 1. Power on the joystick and the UGOT car.

- 2. Use the control stick on the joystick to maneuver the UGOT car. Try functionalities such as forward, backward, turning, and stopping to ensure everything is working properly.

- 3. If you encounter any issues, check the logic of your code and the settings of the UGOT module.

   ![](https://aiclassroom.ubtrobot.com/aiengine/resources/control.gif)

## Step 5: Enjoy the Joy of Driving

Congratulations! You have successfully developed a system that allows you to control the UGOT car using a flight joystick.

Now, place your UGOT car in a safe space and start enjoying the thrill of driving! With the sensitivity and precision of the joystick, you can experience a more immersive driving experience.

Remember to use your car in appropriate environments and follow local driving regulations to ensure safety and respect for others. Drive safely and responsibly.

Feel free to reach out if you need any further assistance.

![](https://aiclassroom.ubtrobot.com/aiengine/resources/fly.gif)



## Step 6: Further Improvements and Extensions

You have successfully implemented control of the UGOT car using a helicopter joystick, but this is just the beginning. Here are some ideas for further improvements and extensions:

- 1.Add Sensors: Enhance your UGOT car's capabilities by adding sensors such as distance sensors, obstacle detection sensors, or cameras for obstacle avoidance.
- 2.Autonomous Driving Mode: Implement autonomous driving functionality for the UGOT car by writing more complex code and utilizing deep learning algorithms. For example, navigate based on predefined paths or avoid obstacles.
- 3.Remote Control: Upgrade the wireless communication protocol to enable remote control of your UGOT car over the internet, allowing you to operate it from anywhere.
- 4.Sound Effects and Lights: Enhance the driving experience and visual effects by adding sound generators and LED lights.
- 5.Computer Vision Integration: Connect a camera to the UGOT robot and integrate object recognition algorithms or other computer vision techniques for advanced gameplay.
Remember to challenge yourself, explore new ideas, and make improvements to enhance the fun and functionality of this project.

## Conclusion

Through this tutorial, you have learned how to develop a control system for the UGOT car using a helicopter joystick. From hardware connections to coding, testing, and debugging, you have taken the crucial steps to bring this exciting project to life.

We hope this tutorial sparks your creativity and provides you with an exhilarating driving experience that makes you feel like a true driver. Remember to always prioritize safety and enjoy the thrilling joy of driving!


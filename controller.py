# This script is called by the controller.service

# This program will let you control your ESC and brushless motor over WebRTC data channels
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?

import os     #importing os library so as to communicate with the system
from timeit import default_timer as timer   #importing time library to make Rpi wait because its too impatient 

import time
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error

# The getch module does single-char input by providing wrappers for the conio.h library functions getch() 
# import getch

# Import of the Adafruit PCA9685 library for the
# PCA9685 servo controller.
import Adafruit_PCA9685

# Set channels to the number of servo channels on your kit.
# 16 for Shield/HAT/Bonnet.

# Controlling servos
from adafruit_servokit import ServoKit


import json
import socket
import os
import RPi.GPIO as GPIO
import pigpio

socket_path = '/tmp/uv4l.socket'

try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise

s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)


# print'socket_path: %s' % socket_path
s.bind(socket_path)
s.listen(1)


def cleanup():
    pass

def speed_decrease(motor_speed):
    motor_speed -= 2
    return motor_speed
        
MAX_MESSAGE_SIZE = 4096


if __name__ == "__main__":
    while True:
        # Turningy Plush 60A ESC PWM working frequency
        # In case of using other ESC adjust ESC_FREQ, MIN_WIDTH, MAX_WIDTH
        
        # Default ESC Frequency for turningy in HZ
        ESC_FREQ = 50
            
        # 1ms MIN width
        
        # Turningy
        # MIN_WIDTH = 4*ESC_FREQ
        # 2 ms MAX width
        # Turningy 
        #MAX_WIDTH = 8*ESC_FREQ
        
        # Maverick testing ESC parameters:
        
        MIN_WIDTH = 280
        MAX_WIDTH = 350
        NEUTRAL_WIDTH = 300

        ESC=14 #Connect the ESC in this GPIO pin 

        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(ESC_FREQ)

      
        # print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
        time.sleep(1)
        
        # this is speed for turningy ESC
        # speed = MIN_WIDTH  + 1
        
        # MAVERICK ESC Neutral speed
        speed = NEUTRAL_WIDTH 
        
        # define number of channels supported   
        kit = ServoKit(channels=16)
        
        # initial angle of servo
        angle_init = 90
        angle = angle_init
        
        # center servo
        kit.servo[15].angle = angle_init
        
        
   
        inp = "skip"
        print('awaiting connection...')
        os.system("echo awaiting connection...| wall")
        
        connection, client_address = s.accept()
        print('client_address %s' % client_address)
        p= "echo client_address %s | wall" % client_address
        os.system(p)
        
        try:
            print('established connection with', client_address)
            
            # if not receiving messages decrease speed and servo angle
            timeout = 1
            start = timer()
            p = "echo start = %d | wall" % start
            os.system(p)
            
            # ESC Speed Increment/Decrement
            speed_inc_dec = 4
            
            # Servo Angle Increment/Decrement
            angle_inc_dec = 30
            
            while True:
                if ((speed >= MIN_WIDTH) or (speed <= MAX_WIDTH)):
                    message = connection.recv(MAX_MESSAGE_SIZE)
                    # print('message: {}'.format(message))
                    
                    if not message:
                        # if there are no messages shutdown engine
                        pwm.set_pwm(ESC,0,NEUTRAL_WIDTH)
                        message = " echo Emergency STOP Engaged - no messages | wall"      
                        os.system(message)
                         
                        break
                
                        
                    data = json.loads(message.decode('utf-8'))

                    if 'commands' in data:
                        if 'FORDWARD' in data['commands']:
                            speed += speed_inc_dec     # incrementing the speed 
                            print ("forward speed = %d" % speed)
                            p = "echo Forward speed = %d | wall" % speed
                            os.system(p)
                            
                        elif 'BACKWARD' in data['commands']:
                            speed -= speed_inc_dec     # decrementing the speed
                            print ("backward speed = %d" % speed)
                            p = "echo Backward speed = %d | wall" % speed
                            os.system(p)
                        
                        elif 'RIGHT' in data['commands']:
                            # increase angle of servo to rigth
                            # Max Servo angles depend on servo model and vehicle (for every different type this should e checked)
                            if angle > 50 :
                                angle -= angle_inc_dec
                                kit.servo[15].angle = angle
                                kit.continuous_servo[1].throttle = 1
                                print ("turn rigth = %d" % angle)
                                rigth = "echo Rigth angle = %d | wall" % angle
                                os.system(rigth)
                                
                            else:
                                print (" Maximum turning angle")
                                angle_alert = "echo Maximum turning angle | wall"
                                os.system(angle_alert)
                            
                        elif 'LEFT' in data['commands']:
                            # increase angle to left
                            # Max Servo angles depend on servo model and vehicle (for every different type this should e checked)
                            if angle < 130 :
                                angle += angle_inc_dec
                                kit.servo[15].angle = angle
                                kit.continuous_servo[1].throttle = -1
                                print ("turn LEFT = %d" %angle)
                                left = "echo LEFT angle = %d | wall" % angle
                                os.system(left)
                            
                            else :
                                print (" Maximum turning angle")
                                angle_alert = "echo Maximum turning angle | wall"
                                os.system(angle_alert)
                                
                        # Engage emergency stop
                        elif 'STOP' in data['commands']:
                            speed = NEUTRAL_WIDTH
                            emergency_alert = " echo Emergency STOP Engaged | wall"
                            os.system(emergency_alert)
                            
                    
                            
                    pwm.set_pwm(ESC,0,speed)
                        
                    
                else:
                    print ("Speed range exceeded")
                        
                    # descreese speed if no keyboard pressed
                    # WORK IN PROGRESS
                    """
                    time.sleep(3)
                    if speed >= MIN_WIDTH:
                        speed = speed_decrease(speed)
                        print ("no gas - speed = %d" % speed)
                    """
                stop = timer()
                p = "echo stop = %d | wall" % stop
                os.system(p) 
                
                if (stop - start) > 5:
                    if speed > NEUTRAL_WIDTH:
                        speed -= 1
                        pwm.set_pwm(ESC,0,speed)
                        p = "echo SPEED decreasing = %d | wall" % speed
                        os.system(p)
                    if speed < NEUTRAL_WIDTH:
                        speed += 1
                        pwm.set_pwm(ESC,0,speed)
                        p = "echo SPEED decreasing = %d | wall" % speed
                        os.system(p)
                    if angle > angle_init:
                        angle -= angle_inc_dec
                        kit.servo[15].angle = angle
                        kit.continuous_servo[1].throttle = -1
                        p = "echo ANGLE decreasing = %d | wall" % angle
                        os.system(p)
                    if angle < angle_init:
                        angle += angle_inc_dec
                        kit.servo[15].angle = angle
                        kit.continuous_servo[1].throttle = 1
                        p = "echo ANGLE decreasing = %d | wall" % angle
                        os.system(p)    
                
            pwm.set_pwm(ESC,0,NEUTRAL_WIDTH)
            message = " echo Emergency STOP Engaged | wall"      
            os.system(message)
            
            print('connection closed')
        

        finally:
            # Clean up the connection
            cleanup()
            connection.close()
            
        

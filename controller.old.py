# This script is called by the controller.service

# This program will let you control your ESC and brushless motor over WebRTC data channels
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?

import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 

time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error

# The getch module does single-char input by providing wrappers for the conio.h library functions getch() 
# import getch

# Import of the Adafruit PCA9685 library for the
# PCA9685 servo controller.
import Adafruit_PCA9685

# Set channels to the number of servo channels on your kit.
# 16 for Shield/HAT/Bonnet.
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
        ESC_FREQ = 50

        ## YMMV
        #MIN_WIDTH = 210
        #MIN_WIDTH = 150
        MIN_WIDTH = 4*ESC_FREQ
        # Note that some batteries, 12 volt PSUs, etc. might only be capable of far less than this (e.g. 1350)
        # However, the controllers range should still be set to max for finest full-scale resolution.
      

        MAX_WIDTH = 8*ESC_FREQ

        ESC=14 #Connect the ESC in this GPIO pin 

        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(ESC_FREQ)

      
        print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
        time.sleep(1)
        speed = MIN_WIDTH  
        
    
        # define number of channels supported   
        kit = ServoKit(channels=16)
        
        # center servo
        kit.servo[15].angle = 90
        # initial angle of servo
        angle = 90
   
        inp = "skip"
        print('awaiting connection...')
        connection, client_address = s.accept()
        print('client_address %s' % client_address)
        try:
            print('established connection with', client_address)

            while True:
                if ((speed >= MIN_WIDTH) or (speed <= MAX_WIDTH)):
                    message = connection.recv(MAX_MESSAGE_SIZE)
                    # print('message: {}'.format(message))
                    if not message:
                        break
                    data = json.loads(message.decode('utf-8'))

                    if 'commands' in data:
                        if 'FORDWARD' in data['commands']:
                            speed += 2     # incrementing the speed 
                            print ("forward speed = %d" % speed)
                            p = "echo Forward speed = %d | wall"
                            os.system(p %speed)
                            
                        elif 'BACKWARD' in data['commands']:
                            speed -= 2     # decrementing the speed
                            print ("backward speed = %d" % speed)
                            # p = "echo Backward | wall"
                            # os.system(p)
                        
                        elif 'RIGHT' in data['commands']:
                            # increase angle of servo to rigth
                            angle +=10
                            print ("turn rigth = %d" % angle)
                            kit.servo[15].angle = angle
                            kit.continuous_servo[1].throttle = -1
                            
                        elif 'LEFT' in data['commands']:
                            # increase angle to left
                            angle -=10
                            kit.servo[15].angle = angle
                            kit.continuous_servo[1].throttle = 1
                            print ("turn rigth = %d" % angle)
                            
                            
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
                    
                
                    

            print('connection closed')
        

        finally:
            # Clean up the connection
            cleanup()
            connection.close()
            
        

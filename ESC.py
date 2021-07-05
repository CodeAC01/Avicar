# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?

import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 

time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error

#The getch module does single-char input by providing wrappers for the conio.h library functions getch() 
import getch

# Import of the Adafruit PCA9685 library for the
# PCA9685 servo controller.

import Adafruit_PCA9685

# Turningy Plush 60A ESC PWM working frequency
# In case of using other ESC adjust ESC_FREQ, MIN_WIDTH, MAX_WIDTH
ESC_FREQ = 50

## YMMV
#MIN_WIDTH = 210
#MIN_WIDTH = 150
MIN_WIDTH = 4*ESC_FREQ
# Note that some batteries, 12 volt PSUs, etc. might only be capable of far less than this (e.g. 1350)
# However, the controllers range should still be set to max for finest full-scale resolution.
#MAX_WIDTH = 420
#MAX_WIDTH = 600

MAX_WIDTH = 8*ESC_FREQ

##
#  pwm.set_pwm(14,1,210)
#>>> pwm.set_pwm(14,1,210)
#>>> pwm.set_pwm(14,1,230)
#>>> pwm.set_pwm(14,1,210)
#>>> pwm.set_pwm(14,1,230)
#>> pwm.set_pwm(14,1,210)
# pwm.set_pwm_freq(45)



ESC=14 #Connect the ESC in this GPIO pin 

pwm = Adafruit_PCA9685.PCA9685()

print ("For first time launch, select calibrate")
print ("Type the exact word for the function you want")
print ("calibrate OR manual OR control OR arm OR stop")

"""
def manual_drive(): #You will use this function to program your ESC if required
    print ("You have selected manual option so give a value between 0 and you max value")
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
		elif inp == "control":
			control()
			break
		elif inp == "arm":
			arm()
        else:
            pi.set_servo_pulsewidth(ESC,inp)
"""

def calibrate():   #This is the auto calibration procedure of a normal ESC
    
    pwm.set_pwm_freq(ESC_FREQ)
    pwm.set_pwm(ESC,0,MIN_WIDTH)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        #pi.set_servo_pulsewidth(ESC, max_value)
        pwm.set_pwm(ESC,0,MAX_WIDTH)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':            
            #pi.set_servo_pulsewidth(ESC, min_value)
            pwm.set_pwm(ESC,0,MIN_WIDTH)
            print ("Wierd eh! Special tone")
            time.sleep(7)
            print ("Wait for it ....")
            time.sleep (5)
            print ("Im working on it, DONT WORRY JUST WAIT.....")
            #pi.set_servo_pulsewidth(ESC, 0)
            pwm.set_pwm(ESC,0,MIN_WIDTH)
            time.sleep(2)
            print ("Arming ESC now...")
            #pi.set_servo_pulsewidth(ESC, min_value)
            pwm.set_pwm(ESC,0,MIN_WIDTH)
            time.sleep(1)
            print ("See.... uhhhhh")
            control() # You can change this to any other function you want
            
def control(input_speed): 
    print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
    time.sleep(1)
    speed = MIN_WIDTH  
    print ("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    #while True:
    #pi.set_servo_pulsewidth(ESC, speed)
    inp = "skip"
    if ((speed >= MIN_WIDTH) or (speed < MAX_WIDTH)):
        #inp = getch.getch()
        inp = input_speed
    else:
        print("Exceeding motor range")
        
    if inp == "w":
        speed += 2     # incrementing the speed 
        print ("speed = %d" % speed)
    elif inp == "s":
        speed -= 2     # decrementing the speed
        print ("speed = %d" % speed)
    elif inp == "q":
        stop()          #going for the stop function
    elif inp == "skip":
        return
    else:
        print ("WHAT DID I SAID!! Press a,q,d or e")
    pwm.set_pwm(ESC,0,speed)
            
def arm(): #This is the arming procedure of an ESC 
    print ("Connect the battery and press Enter")
    inp = input()    
    if inp == '':
        #pi.set_servo_pulsewidth(ESC, 0)
        pwm.set_pwm(ESC,0,MIN_WIDTH)
        time.sleep(1)
        #pi.set_servo_pulsewidth(ESC, max_value)
        pwm.set_pwm(ESC,0,MAX_WIDTH)
        time.sleep(1)
        #pi.set_servo_pulsewidth(ESC, min_value)
        pwm.set_pwm(ESC,0,MIN_WIDTH)
        time.sleep(1)
        control() 
        
def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    #pi.set_servo_pulsewidth(ESC, 0)
    pwm.set_pwm(ESC,0,MIN_WIDTH)
    #pi.stop()

#This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.    
inp = input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else :
    print ("Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!")

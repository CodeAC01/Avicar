import Adafruit_PCA9685
import keyboard
import time

ESC_FREQ = 50
ESC=14
            
# 1ms MIN width

MIN_WIDTH = 4*ESC_FREQ
# 2 ms MAX width

MAX_WIDTH = 8*ESC_FREQ
NEUTRAL_WIDTH = 6*ESC_FREQ

ESC=14 #Connect the ESC in this GPIO pin 

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(ESC_FREQ)


print("Press ESC to start")

input("Press Enter to continue...")

#keyboard.wait('esc')
print("Calibration has started")
time.sleep(1)

#
# Initiating calibration process
#

print("Hold down the setup button while turning on the ESC")
time.sleep(1)
print("Release the setup button once the Red LED starts to flash")
time.sleep(1)

#
# Calibration of neutral position
#
input("Press Enter to continue...")

print("Now calibrating neutral position. Press the setup button on ESC")
time.sleep(3)
pwm.set_pwm(ESC,0,NEUTRAL_WIDTH)
print("Green button flashes and a Beep sound comes from the motor")

#
# Calibrating Full throtle
#
input("Press Enter to continue...")
print("Now we are calibrating full throttle. Press the setup button")
time.sleep(3)
pwm.set_pwm(ESC,0,MAX_WIDTH)

print("Green button flashes twice. Beeps twice from the motor ")

#
# Calibrating full brake
#
input("Press Enter to continue...")
print("Now we are calibrating full brake. Press the setup button")
time.sleep(3)
pwm.set_pwm(ESC,0,MIN_WIDTH)
print("Green button flashes three times. Beeps three time from the motor ")

#
# When the process has finished, motor control will be activated in 3 seconds
#
pwm.set_pwm(ESC,0,NEUTRAL_WIDTH)

print("There should be no LED lighting")





        
        
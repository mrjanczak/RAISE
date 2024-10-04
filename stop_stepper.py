import RPi.GPIO as GPIO
import time
from HR8825 import HR8825

try:
	Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
	Motor1.SetMicroStep('softward','fullstep')
	Motor1.Stop()
    
except:
    # GPIO.cleanup()
    print("\nMotor stop")
    Motor1.Stop()
    exit()

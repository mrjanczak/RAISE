# efynJtMHaNWXNjl4bunDNJl1VnHDlDwhZ4SNIt6jIJkuR3lEdpmiVlsNbG3GBTl0cjigIXsNIUkkxepUY22oViuxci2ZVAJ3RZCZI86hMATVcQxEMfjTIT2dNmzdk91YMkiSwViMTvGVlfjXZxWy5GzfZmUBRelPcXGEx4veeQWH17ltbuneR3WiZiXGJdzBa1WO9uuVIfjko3xmLjClJeOAYJWp1Ul9Rwmflgy9cr3lQCi0OxidJANuaVWdNxoxY1cyW6C9I9iMw4iITbm2F4t2ZxUexoh3cW3ZQ6i1OsiRJRKAYSWQ57jxeSmtFQr5Inicw3iiQ52c9wt0csGjF3ufejSCI66BI4igIlsGIGksNF15cY3SRovnbGW6VlyKSTUhQTiROxiEI0xoMHz5QbxrMCyhIBs0I9kIRShLdAGAV2JEcH3MNu1ZZ2WYQFiDOti1IfwXNrC08bwpNrSn8tyQM6DeIq0IIuiuw9izRLGeFT0GZ3UxVF46c2G3lNygZmXtMKiuOGiLITwxNaCI8Iw2NSSc80yrMwDMIB1sIWi1wRiDRFWz1Ph7aTWTxKBEZFGHR1yLZ6XmNuzcIXjco8iGb1XjJGqEYuWm5pjye4mpFOrdQzGKd0t2YKWilgsTLGmkNsvjbaSeIIsoIQkXlVQBQMW5RCkNctmfVEzBc6ywIk6TIyjpITxyM8y74hxuMWzDQFuBMpTDYF5eLSjPUbiTfNQH=D=x463b2396012041fa97ae082e4d90b2bfc49201899b15ecec18fd7da256912930b01d7234c7ee218a437b22e8d93854dbef2553cdee1b088e59d9cce5e69ad8aece63956d067ab7371abd26b09c9e947d808280d810ac67cdcc74cb9b32239f0b466a75a343def740d790eaaab9abb0c583a36eaefceb05cba90536f50b9b0b2143eb81e696e5f6d1d96ee9d6f3e9c11210e7acfc1bc5dd0cf3d1efeb4006d414922217ce2bd9cd57c4de752d0e49ad90b2413f12f3249768be546982fd825558a4f69e42300f603095f0160d82fa9b62ecae3cdd9f039eef50b5adcacce350542d724e65b6442554635d7647ee43f6772f6658c8c03ddaf8098a2261344485cff4c1955b0f3a1ca26010029cc81a7f68b3369e527a26f25f23626fa0eeb41fbe43ea73c11c9d07725e244fd639c5830a3ddf90b8b2ff1063e9eed00a52bfa32a9da56fc5b7b92cc62a3bb89b8420c56b2354e23537f5459983940b9ea61fa9e69448645f493e3466989b5bf46548e4fdd4bbc5a80ba48a6b883bb3dcfb814e9a10d42a13368caf8bdcf4febec52f1e97342a794143def90583ec31d99b918c38f520dabf9cc73fb5c83901c2e13ccea5e6479aca5f5e8b8fbf19aeb3142be8f9602d0d93a7bdd931a5ed898810257694510a50fdd6762e53bc8990a0c8c2de208df903a4e820a06a279b706b5d617e0e34dc515fc06523f663dc83d88bb669f0

import PySimpleGUI as sg
from login import check_login
import sys

# if not check_login('061023'):
#     sys.exit()

"""
sudo raspi-config > Interface options > I2C > Yes

"""

from buildhat import Motor
from time import sleep
import math
import sys    
sys.path.append('./keyboard')

import keyboard

fuel_pump = Motor('A') 
ogv_servo = Motor('B')
lp_rotor = Motor('C')
hp_rotor = Motor('D')

motors = [fuel_pump, ogv_servo, lp_rotor, hp_rotor]
ratios = [1, 24*20/12, 1, 1]
direction = [1,1,-1,1]
angle = [0,360*2,0,0]

deg = 360*20
speed_max = [100,50,30,50]
speed_min = [20,20,20,20]
time_sec = 60

# Valves
PCLM = False
FPAS = False

VBV = False
VSV = False
ACCR = False
ACCS = False

def start_stop_motor(motor_i, mode, speed):
    if speed:

        if abs(speed) < speed_min[motor_i]:
            speed = math.sign(speed)*speed_min[motor_i]
        if abs(speed) > speed_max[motor_i]:
            speed = math.sign(speed)*speed_max[motor_i]

        for s in range(1, int(speed[motor_i]/10)):
            motors[motor_i].start(speed = s*10*direction[motor_i])
            sleep(.5)
        motors[motor_i].start(speed = speed*direction[motor_i])

    else:
        for s in range(int(speed_min[motor_i]/10), 1):
            motors[motor_i].start(speed = s*10*direction[motor_i])
            sleep(.5)
        motors[motor_i].stop()

def rotate_motor(motor_i, direction):
    ogv_servo.run_for_degrees(degrees = angle[motor_i]*direction)

def stop_all():
    fuel_pump.stop()
    ogv_servo.stop()
    lp_rotor.stop()
    hp_rotor.stop()

sliders = ['-PUMP-', '-OGV-', '-N1-', '-N2-']
BLUE_BUTTON_COLOR = '#FFFFFF on #2196f2'
GREEN_BUTTON_COLOR ='#FFFFFF on #00c851'
RED_BUTTON_COLOR ='#FFFFFF on #990000'
sg.theme('light grey')

layout = [  [
             sg.Text('N1', justification='center', size=(6,1)), 
             sg.Text('N2', justification='center', size=(6,1)), 
             sg.Text('OGV', justification='center', size=(6,1)),
             sg.Text('PUMP', justification='center', size=(6,1)) 
             ],

            [sg.Slider((0, 100), size=(8,20), key='-N1-'), 
             sg.Slider((0, 100), size=(8,20), key='-N2-'),
             sg.Slider((-50, 50), default_value = 0, size=(8,20), key='-OGV-'),
             sg.Slider((0, 100), size=(8,20), key='-PUMP-')],

            [sg.Button('PCLM',  button_color = BLUE_BUTTON_COLOR), 
             sg.Button('FPAS',  button_color = BLUE_BUTTON_COLOR)],

            [sg.Button('VBV',  button_color = BLUE_BUTTON_COLOR), 
             sg.Button('VSV',  button_color = BLUE_BUTTON_COLOR), 
             sg.Button('ACCR', button_color = BLUE_BUTTON_COLOR), 
             sg.Button('ACCS', button_color = BLUE_BUTTON_COLOR),

            sg.Button('STOP', button_color = RED_BUTTON_COLOR, bind_return_key=True), 
            #  sg.Button('Exit')
            ]]

window = sg.Window('Window Title', layout)

while True:             # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break

    if event == 'PCLM':
        PCLM = not PCLM
        if not PCLM:
            window['PCLM'].update(button_color = BLUE_BUTTON_COLOR)
        else:
            window['PCLM'].update(button_color = GREEN_BUTTON_COLOR)

    if event == 'FPAS':
        if PCLM:
            FPAS = not FPAS
        if not FPAS:
            window['FPAS'].update(button_color = BLUE_BUTTON_COLOR)
        else:
            window['FPAS'].update(button_color = GREEN_BUTTON_COLOR)


    if event == 'VBV':
        VBV = not VBV
        if not VBV:
            window['VBV'].update(button_color = BLUE_BUTTON_COLOR)
        else:
            window['VBV'].update(button_color = GREEN_BUTTON_COLOR)

    if event == 'VSV':
        VSV = not VSV
        if not VSV:
            window['VSV'].update(button_color = BLUE_BUTTON_COLOR)
        else:
            window['VSV'].update(button_color = GREEN_BUTTON_COLOR)

    if event == 'ACCR':
        ACCR = not ACCR
        if not ACCR:
            window['ACCR'].update(button_color = BLUE_BUTTON_COLOR)
        else:
            window['ACCR'].update(button_color = GREEN_BUTTON_COLOR)

    if event == 'ACCS':
        ACCS = not ACCS
        if not ACCS:
            window['ACCS'].update(button_color = BLUE_BUTTON_COLOR)
        else:
            window['ACCS'].update(button_color = GREEN_BUTTON_COLOR)            

    
    if event in sliders:
        motor_i = sliders.index(event)
        speed = values[event]
        start_stop_motor(motor_i, True, speed)

    if event == 'STOP':
        window['-N1-'].update(0)
        window['-N2-'].update(0)
        window['-OGV-'].update(0)
        window['-PUMP-'].update(0)

        stop_all()
    
window.close()
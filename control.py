# importing pyglet module 
import pyglet 
import pyglet.window.key 

import RPi.GPIO as GPIO
import time
from HR8825 import HR8825


Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor1.SetMicroStep('softward','fullstep')

# width of window 
width = 500

# height of window 
height = 300

# caption i.e title of the window 
title = "RISE control"

# creating a window 
window = pyglet.window.Window(width, height, title) 

# text 
text = "SPACE to STOP"

# creating a label with font = times roman 
# font size = 36 
# aligning it to the centre 
label = pyglet.text.Label(text, 
						font_name ='Times New Roman', 
						font_size = 36, 
						x = window.width//2, y = window.height//2, 
						anchor_x ='center', anchor_y ='center') 

# on draw event 
@window.event 
def on_draw():	 

	
	# clearing the window 
	window.clear() 
	
	# drawing the label on the window 
	label.draw() 
	
# key press event	 
@window.event 
def on_key_press(symbol, modifier): 
	 
	if symbol == pyglet.window.key.RIGHT: 
		
		print("Key C is pressed") 

        for i in range(1,10):
            stepdelay = 1/(i*10)
            Motor1.TurnStep(Dir='forward', steps=10, stepdelay = stepdelay)

        Motor1.TurnStep(Dir='forward', steps=600, stepdelay = stepdelay)

        for i in range(10,1,-1):
            stepdelay = 1/(i*10)
            Motor1.TurnStep(Dir='forward', steps=10, stepdelay = stepdelay)
        
        Motor1.Stop()

    if symbol == pyglet.window.key.SPACE:
        Motor1.Stop()

pyglet.app.run()

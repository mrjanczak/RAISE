import math
import pyglet
from pyglet import shapes
 
width = 500
height = 800 
title = "ENG Display Panel"   
window = pyglet.window.Window(width, height, title) 
batch = pyglet.graphics.Batch()

bk =   (0,0,0)
wh =   (255, 255, 255)
wh_a = (255, 255, 255, 255)
gray = (145, 146, 150)
red =  (235, 50, 40)
yel =  (247,173,1)
bl =   (0,255,255)
bl_a = (0,255,255, 255)

N1 = 83.5
EGT = 766
N2 = 100.0
FF = 1.16
OP = 61
OT = 83
OQ = 87
VIB = 0.3

thrust_modes =['TO', 'CLB', 'CRZ', 'GA', 'CON']

panels = [  {'title':'N1',         'val':N1, 'type':'gauge', 'scale':.5, 'NOR':(0, 200), 'ULT':210, 'div':20}, 
            {'title':'EGT',        'val':EGT,'type':'gauge', 'scale':4.5,'NOR':(0, 195), 'LIM':(200, 210), 'ULT':210}, 
            {'title':'N2',         'val':N2, 'type':'gauge', 'scale':.5, 'NOR':(0, 200), 'ULT':210}, 
            {'title':'FF',         'val':FF, 'type':'value', 'scale':1}, 
            {'title':'OIL\nPRESS', 'val':OP, 'type':'level', 'scale':1, },
            {'title':'OIL\nTEMP',  'val':OT, 'type':'level', 'scale':1, }, 
            {'title':'OIL QTY %',  'val':OQ, 'type':'value', 'scale':1, },
            {'title':'VIB',        'val':VIB,'type':'level', 'scale':1, 'div':4},
            ]
values = [N1, EGT, N2, OP, OT, OQ, VIB]
shape = []

x0 = 0
y0 = height 
for p, panel in enumerate(panels):
    type_ = panel['type']
    val = panel['val']

    if type_ == 'gauge':
        y0 -= 140
        xt, yt = 250, y0 + 10
        xc, yc, r0 = x0 + 150, y0 + 70, 70
        xb, yb, w, h, thc  = xc, yc + 10, 90, 35, 3   
        xv, yv, size = xb + w - 2 - thc, yb -2 + thc, 22
    elif type_ == 'value':
        y0 -= 50
        xt, yt = 250, y0 + 20
        xb, yb, w, h, thc  = x0 + 120, yt - 15, 60, 30, 3   
        xv, yv, size = xb + w - 2 - thc, yb -2 + thc, 18     
    elif type_ == 'level':
        y0 -= 90
        xt, yt = 250, y0 + 40
        xb, yb, w, h, thc  = x0 + 120, yt - 15, 60, 30, 3   
        xv, yv, size = xb + w - 2 - thc, yb -2 + thc, 18

    # title
    title = panel['title']
    shape.append(pyglet.text.Label(title, x = xt, y = yt, font_name = 'Arial', font_size = 12, bold = True, color = bl_a, batch = batch,
                                align = 'center', anchor_x = 'center', anchor_y = 'center', multiline = True, width = 100))

    # box w/ value
    shape.append(shapes.Rectangle(xb, yb, w, h, color = wh, batch = batch))
    shape.append(shapes.Rectangle(xb+thc, yb+thc, w-thc*2, h-thc*2, color = bk, batch = batch))   
    shape.append(pyglet.text.Label(str(val), x = xv, y = yv, font_name = 'Arial', font_size = size, bold = True, color = wh_a, batch = batch,
                                align = 'right', anchor_x = 'right', anchor_y = 'bottom', multiline = False))

    if type_ == 'gauge':
        rad = -math.pi/180
        a0 = 0
        da =   ref_scale * val/panel['scale']*rad
        a1 = a0 + da

        # arrow & sector
        shape.append(shapes.Sector(xc, yc, r0,   segments = 20, start_angle = a0, angle = da, color = gray, batch = batch))
        r2 = r0 + 10
        x1, y1 = xc, yc
        x2, y2 = r2*math.cos(a1)+xc, r2*math.sin(a1)+yc
        shape.append(shapes.Line(x1, y1, x2, y2, width = 3, color = wh, batch = batch))    

        # Normal scale
        shape.append(shapes.Arc(   xc, yc, r0,   segments = 20, angle = scale_deg, color = wh, batch = batch))
        shape.append(shapes.Arc(   xc, yc, r0-1, segments = 20, angle = scale_deg, color = wh, batch = batch))

        # Scale division
        if 'div' in panel:
            for div in range(11): 
                a = -math.pi/180 * div * panel['div']
                r1, r2 = r0-10, r0
                color = wh
                x1, y1 = r1*math.cos(a) + xc, r1 * math.sin(a) + yc
                x2, y2 = r2*math.cos(a) + xc, r2 * math.sin(a) + yc
                shape.append(shapes.Line(x1, y1, x2, y2, width = 2, color = color, batch = batch))

                if div % 2 == 0:
                    r1 = r0-20
                    x1, y1 = r1*math.cos(a) + xc, r1 * math.sin(a) + yc
                    shape.append(pyglet.text.Label(str(div), x = x1, y = y1, font_name = 'Arial', font_size = 15, color = wh_a, batch = batch,
                                                align = 'center', anchor_x = 'center', anchor_y = 'center', multiline = False))
                    
        if 'LIM' in panel:
                a = ref_scale * panel['LIM']/panel['ref']
                r1 = r0-2
                r2 = r0+10d
                x1, y1 = r1*math.cos(a) + xc, r1 * math.sin(a)+yc
                x2, y2 = r2*math.cos(a) + xc, r2 * math.sin(a)+yc
                shape.append(shapes.Line(x1, y1, x2, y2, width = 2, color = yel, batch = batch))

        if 'RL' in panel:
                a = ref_scale * panel['RL']/panel['ref']
                r1 = r0-2
                r2 = r0+10
                x1, y1 = r1*math.cos(a) + xc, r1 * math.sin(a)+yc
                x2, y2 = r2*math.cos(a) + xc, r2 * math.sin(a)+yc
                shape.append(shapes.Line(x1, y1, x2, y2, width = 2, color = red, batch = batch))



    elif type_ == 'level':
        x1, y1 = x0 + 200, y0
        x2, y2 = x1, y1 + 60
        shape.append(shapes.Line(x1, y1, x2, y2, width = 3, color = wh, batch = batch))        

        if 'LIM' in panel:
                color = yel
                x1, y1 = 
                x2, y2 = 
                shape.append(shapes.Line(x1, y1, x2, y2, width = 2, color = yel, batch = batch))

# window draw event
@window.event
def on_draw():
     
    # clear the window
    window.clear()
     
    # draw the batch
    batch.draw()
 
# run the pyglet application
pyglet.app.run()


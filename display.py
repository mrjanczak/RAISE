# Script to draw engine panel from 737 MAX and read values from throttle quadrant

import math
import numpy as np
import pyglet
from pyglet.window import mouse, key

width = 500
height = 900 
title = "ENG Display Panel"   
window = pyglet.window.Window(width, height, title) 
batch = pyglet.graphics.Batch()
verbose = False

# colors
bk =   (0,0,0)
wh =   (255, 255, 255)
gray = (145, 146, 150)
red =  (235, 50, 40)
yel =  (247,173,1)
bl =   (0,255,255)
gr =   (0,255,0)
rad = -math.pi/180

# Joystick control
control_map = {'master_eng':2, 'crank_mode':6, 'start_mode':7, 'normal_mode':'6|7', 
               'thr':'x', 'thr1': 10, 'thr2': 9, 'thr3': 8}
control = {}
for key_ in control_map:
    control[key_] = False
control['thr'] = 0

# Default values
N1, GI_N1, REV_N1, CRZ_N1, CL_N1, TOGA_N1 = 0.0, 20.0, 60.0, 90.0, 95.0, 100.
EGT = 0.0
N2 = 0.0
FF = 0
OP = 60
OT = 70
OQ = 90
VIB = 0.0

FPAS, FPAS_MAX = 30, 30
OGV, OGV_MAX = 30, 30
VBV = 0.0
VSV = 0.0
ACC = 0.0

TAT = 20

# Definition of panels
panels = [[
            {'title':'N/1',        'type':'gauge', 'scale':.5,   'NOR':(0, 103), 'ULT':[105], 'div':(20,2), 'prec':1}, 
            {'title':'EGT',        'type':'gauge', 'scale':4.5,  'NOR':(0, 880), 'LIM':([900], 940), 'ULT':[950], 'prec':1}, 
            {'title':'N/2',        'type':'gauge', 'scale':.555, 'NOR':(0, 115), 'ULT':[117], 'prec':1}, 
            {'title':'FF',         'type':'value', 'scale':1.,   'prec':0}, 
            {'title':'OIL\nPRESS', 'type':'level', 'scale':2.1,  'ULT':[1], 'LIM':(5, 25), 'NOR':(29, 125), 'prec':0},
            {'title':'OIL\nTEMP',  'type':'level', 'scale':2.25, 'NOR':(0, 110), 'LIM':[114] , 'ULT':[126], 'prec':0 }, 
            {'title':'OIL QTY %',  'type':'value', 'scale':1.,   'prec':0 },
            {'title':'VIB',        'type':'level', 'scale':0.085,'NOR':(0, 3.8), 'LIM':([4], 5), 'prec':1},
        ],[
            {'title':'FPAS %',     'type':'level', 'scale':1.,   'LIM':(-FPAS_MAX,[-2]), 'NOR':(0, FPAS_MAX), 'offset':FPAS_MAX, 'prec':0}, 
            {'title':'OGV %',      'type':'level', 'scale':1.,   'NOR':(-OGV_MAX, OGV_MAX), 'offset':OGV_MAX, 'prec':0}, 
            {'title':'VBV %',      'type':'value', 'scale':1.,   'prec':0 },
            {'title':'VSV %',      'type':'value', 'scale':1.,   'prec':0 },
            {'title':'ACC %',      'type':'value', 'scale':1.,   'prec':0 },
        ]]       

# Draw panels
@window.event
def on_draw():   
    global N1, EGT, N2, FF, OP, OT, OQ, VIB,   FPAS, OGV, VBV, VSV, ACC

    window.clear()

    type_ = None
    shape = []
    det_lab, det_N1 = '', ''

    # COntrol by Thrustmaster Throttle
    if joystick:
        if control['master_eng']:
            if control['thr'] < 0.5:
                N1 = np.interp(control['thr'], [-1.,-.5, 0, .5], [TOGA_N1, CL_N1, CRZ_N1, GI_N1])
                FPAS = FPAS_MAX
                OGV = OGV_MAX
            else:
                N1 = np.interp(control['thr'], [.5, 1], [GI_N1, REV_N1])
                det_lab = 'REV'
                FPAS = -FPAS_MAX  
                OGV = -OGV_MAX              
        else:
            N1 = 0.0

        # N1 detent values
        if control['thr1']:
            det_lab = 'CRZ'
            det_N1 = CRZ_N1
        elif control['thr2']:
            det_lab = 'CL'
            det_N1 = CL_N1
        elif control['thr3']:
            det_lab = 'TOGA'
            det_N1 = TOGA_N1

    EGT = np.interp(N1,[0,20,60,90,100]	,[0,200,600,800,900])
    N2 = np.interp(N1,[0,20,60,90,100]  ,[0,60,80,95,100])
    FF = np.interp(N1,[0,20,60,90,100]	,[0,20,50,70,100])
    VIB = np.interp(N1,[0,20,60,90,100]	,[0,0.1,0.3,0.45,0.5])
        
    values = [[N1, EGT, N2, FF, OP, OT, OQ, VIB], [FPAS, OGV, VBV, VSV, ACC]]

    # 1st line w/ TAT and detend
    x0, y0 = 25, height - 75
    for text, dx, size, color in [('TAT', 10, 10, bl), (TAT, 50, 13, wh), ('C', 75, 10, wh), (det_lab, 110,13, gr)]:
        shape.append(pyglet.text.Label(str(text), x = x0 + dx, y = y0 + 10, font_name = 'Arial', font_size = size, bold = True, color = (*color, 255), batch = batch,
                                       align = 'left', anchor_x = 'left', anchor_y = 'bottom', multiline = False))

    for col in range(2):
        x0, y0 = 25 + col*200, height - 75
        for value, panel in zip(values[col], panels[col]):
            type_prev = type_
            type_ = panel['type']
            scale = panel['scale']
            title = panel['title']
            prec = panel['prec']
            if prec:
                value = round(value, prec)
            else:
                value = int(value)
    
            if 'offset' in panel:
                offset = panel['offset']
            else:
                offset = 0

            if type_ != type_prev == 'gauge':
                y0 -= 20

            if type_ == 'gauge':
                w0, h0, r0 = 130, 95, 45
                y0 -= h0
                xt, yt = x0 + w0, y0 + 5 # title
                xc, yc = x0 + int(w0/2), y0 + r0 # circle center
                xb, yb, w, h, thc, vsize  = xc, yc + 10, 65, 25, 2, 17  # value border            
            elif type_ == 'value':
                w0, h0 = 130, 70
                y0 -= h0
                xt, yt = x0 + w0, y0 + int(h0/2) # title
                xb, yb, w, h, thc, vsize  = x0 + 25, y0 + 25, 50, 25, 2, 17    
            elif type_ == 'level':
                w0, h0 = 130, 80
                y0 -= h0
                xt, yt = x0 + w0, y0 + int(h0/2) # title
                xb, yb, w, h, thc, vsize  = x0 + 40, y0 + 25, 35, 25, 2, 15    
                xc, yc = xb + w + 5, y0 + 10

            # title           
            tsize = 10
            for t in title.split('/'):
                shape.append(pyglet.text.Label(t, x = xt, y = yt, font_name = 'Arial', font_size = tsize, bold = True, color = (*bl, 255), batch = batch,
                                            align = 'center', anchor_x = 'center', anchor_y = 'center', multiline = True, width = 100))
                xt += 10
                yt -= 5
                tsize -= 1

            # text label w/ value
            shape.append(pyglet.shapes.Rectangle(xb, yb, w, h, color = wh, batch = batch))
            shape.append(pyglet.shapes.Rectangle(xb+thc, yb+thc, w-thc*2, h-thc*2, color = bk, batch = batch))   
            xv, yv = xb + w - 2 - thc, yb -2 + thc 
            shape.append(pyglet.text.Label(str(value), x = xv, y = yv, font_name = 'Arial', font_size = vsize, bold = True, color = (*wh, 255), batch = batch,
                                        align = 'right', anchor_x = 'right', anchor_y = 'bottom', multiline = False))

            # Autothrust Label
            if title == 'N/1':
                xl, yl, size = xb + 20 , yb + h + 2, 13
                shape.append(pyglet.text.Label(str(det_N1), x = xl, y = yl, font_name = 'Arial', font_size = size, bold = True, color = (*gr, 255), batch = batch,
                                            align = 'left', anchor_x = 'left', anchor_y = 'bottom', multiline = False))

            value += offset

            # gauge arrow & sector
            if type_ == 'gauge':        
                a = value/scale
                shape.append(pyglet.shapes.Sector(xc, yc, r0,   segments = 20, start_angle = 0, angle = a*rad, color = gray, batch = batch))
                r2 = r0 + 10
                x1, y1 = xc, yc
                x2, y2 = r2*math.cos(a*rad)+xc, r2*math.sin(a*rad)+yc
                shape.append(pyglet.shapes.Line(x1, y1, x2, y2, width = 3, color = wh, batch = batch)) 

            # level arrow 
            if type_ == 'level':
                x1, y1 = xc + 2,  yc + value/scale
                x2, y2 = x1 + 15, y1 - 4
                x3, y3 = x1 + 15, y1 + 4
                shape.append(pyglet.shapes.Triangle(x1, y1, x2, y2, x3, y3, color = wh, batch = batch))

            # Markers & scale divisions
            for lab in ['NOR', 'LIM', 'ULT']:
                markers = []
                if lab not in panel:
                    continue

                if type(panel[lab]) in [int, float]:
                    a0 = (panel[lab]+offset)/scale
                    a1 = a0

                elif type(panel[lab]) == list:
                    a0 = (panel[lab][0]+offset)/scale
                    a1 = a0     
                    markers.append(abs(a0))   

                elif type(panel[lab] == tuple):
                    a0, a1 = panel[lab]

                    if type(a0) == list:
                        a0 = (a0[0]+offset)/scale
                        markers.append(abs(a0))
                    else:
                        a0 = (a0+offset)/scale

                    if type(a1) == list:
                        a1 = (a1[0]+offset)/scale
                        markers.append(abs(a1))
                    else:
                        a1 = (a1+offset)/scale

                if type_ == 'gauge': 

                    if lab == 'NOR':
                        color, r1, r2 = wh,  r0-5, r0 + 0
                    elif lab == 'LIM':
                        color, r1, r2 = yel, r0-1, r0 + 10    
                    elif lab == 'ULT':
                        color, r1, r2 = red, r0-1, r0 + 10  

                    # Arcs
                    da = a1 - a0
                    if da != 0:
                        shape.append(pyglet.shapes.Arc(   xc, yc, r0,   segments = int(da/10), start_angle = abs(a0)*rad, angle = da*rad, color = color, batch = batch))
                        shape.append(pyglet.shapes.Arc(   xc, yc, r0-1, segments = int(da/10), start_angle = abs(a0)*rad, angle = da*rad, color = color, batch = batch))

                    # Markers
                    for a in markers:
                        x1, y1 = r1 * math.cos(a * rad) + xc, r1 * math.sin(a * rad) + yc
                        x2, y2 = r2 * math.cos(a * rad) + xc, r2 * math.sin(a * rad) + yc
                        shape.append(pyglet.shapes.Line(x1, y1, x2, y2, width = 2, color = color, batch = batch))
        
                    # Scale division
                    if 'div' in panel and lab == 'NOR':
                        division, modulo = panel['div'] 
                        for d in range(11): 
                            a = d * division
                            x1, y1 = r1 * math.cos(a * rad) + xc, r1 * math.sin(a * rad) + yc
                            x2, y2 = r2 * math.cos(a * rad) + xc, r2 * math.sin(a * rad) + yc
                            shape.append(pyglet.shapes.Line(x1, y1, x2, y2, width = 2, color = color, batch = batch))

                            if d % modulo == 0:
                                rd = r0-15
                                xd, yd = rd * math.cos(a * rad) + xc, rd * math.sin(a * rad) + yc
                                shape.append(pyglet.text.Label(str(d), x = xd, y = yd, font_name = 'Arial', font_size = 10, color = (*color, 255), batch = batch,
                                                            align = 'center', anchor_x = 'center', anchor_y = 'center', multiline = False))
                            
                elif type_ == 'level':

                    if lab == 'NOR':
                        color, r1, r2 = wh,  -1, 5
                    elif lab == 'LIM':
                        color, r1, r2 = yel, -1, 5    
                    elif lab == 'ULT':
                        color, r1, r2 = red, -2, 8              

                    if a0 != a1:
                        x1, y1 = xc, yc + abs(a0)
                        x2, y2 = xc, yc + abs(a1)     
                        shape.append(pyglet.shapes.Line(x1, y1, x2, y2, width = 2, color = color, batch = batch))

                    for a in markers:
                        x1, y1 = xc+r1, yc + abs(a)
                        x2, y2 = xc+r2, yc + abs(a)
                        shape.append(pyglet.shapes.Line(x1, y1, x2, y2, width = 2, color = color, batch = batch))

    x0, y0, text = 25, 50, "1/Q - N1; 2/W - N2, 3/E - FF, 4/R - OGV\n5/T - FPAS, 6/Y - VBV, 7/U - VSV, 8/I - ACC\nS - stop motors"
    shape.append(pyglet.text.Label(str(text), x = x0 , y = y0 , font_name = 'Arial', font_size = 10, bold = True, color = (*wh, 255), batch = batch,
                                   width = 400, align = 'left', anchor_x = 'left', anchor_y = 'bottom', multiline = True))

    batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    global N1, N2, OGV, FF,  FPAS, VBV, VSV, ACC

    if symbol == key.S:
        print('imidiately stop all motors!')

    if symbol == key._1:
        N1 += 20
    if symbol == key.Q:
        N1 -= 20        
    N1 = np.interp(N1, [0,100],[0,100])

    if symbol == key._2:
        N2 += 20
    if symbol == key.W:
        N2 -= 20
    N2 = np.interp(N2, [0,100],[0,100])

    if symbol == key._3:
        OGV += 10
    if symbol == key.E:
        OGV -= 10
    OGV = np.interp(OGV, [-OGV_MAX,OGV_MAX],[OGV_MAX,OGV_MAX]) 

    if symbol == key._4:
        FF += 20
    if symbol == key.R:
        FF -= 20
    FF = np.interp(FF, [0,100],[0,100])    


    if symbol == key._5:
        FPAS += 10
    if symbol == key.T:
        FPAS -= 10
    FPAS = np.interp(FPAS, [-FPAS_MAX,FPAS_MAX],[FPAS_MAX,FPAS_MAX]) 

    if symbol == key._6:
        VBV += 20
    if symbol == key.Y:
        VBV -= 20
    VBV = np.interp(VBV, [0,100],[0,100]) 

    if symbol == key._7:
        VSV += 20
    if symbol == key.U:
        VSV -= 20
    VSV = np.interp(VSV, [0,100],[0,100])

    if symbol == key._8:
        ACC += 20
    if symbol == key.I:
        ACC -= 20
    ACC = np.interp(ACC, [0,100],[0,100])


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        pass

        
def on_joyaxis_motion(joystick, axis, value):
    global control

    if  verbose:
        print(axis, value)

    if axis == control_map['thr']:
        control['thr'] = value
    
def on_joybutton_press(joystick, button):
    global control

    if verbose:
        print(button)

    for k, b in control_map.items():
        if type(b) == int and button == b:
            control[k] = True

def on_joybutton_release(joystick, button):
    global control

    if verbose:
        print(button)

    for k, b in control_map.items():
        if type(b) == int and button == b:
            control[k] = False

        if type(b) == str and '|' in b:
            adj_b = b.split('|')
            b1, b2 = int(adj_b[0]), int(adj_b[1])
            if not(joystick.buttons[b1] or joystick.buttons[b2]):
                control[k] = True

joystick = None
joysticks = pyglet.input.get_joysticks()
if joysticks:
    for joy in joysticks:
        name = joy.__dict__['device'].name
        if name == 'TCA Q-Eng 1&2':
            print(f'{name} connected')
            joystick = joy
            joystick.open()
            joystick.push_handlers(on_joyaxis_motion)
            joystick.push_handlers(on_joybutton_press)
            joystick.push_handlers(on_joybutton_release)

            break

pyglet.app.run()

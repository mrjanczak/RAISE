
# Script to draw engine panel from 737 MAX and read values from throttle quadrant

import math
import numpy as np
# Example file showing a circle moving on screen
import pygame
import pygame.gfxdraw

verbose = False

width = 1024
height = 600 
caption = "ENG Display Panel"   
running = True
dt = 0.1

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(caption)
clock = pygame.time.Clock()

# colors
black = (0,0,0)
white = (255, 255, 255)
gray = (145, 146, 150)
red = (235, 50, 40)
yellow = (247,173,1)
blue = (0,255,255)
green = (0,255,0)

rad = math.pi/180

columns = 4
locked = True

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

# Definition of panels; NOR/LIM/ULT tuplets define arc range, values in [] are shown as yellow/red markers
panels = [[
            {'title':'N1',         'type':'gauge', 'scale':.5,   'NOR':(0, 91),  'LIM':([-92], 103), 'ULT':[105], 'div':(20,2), 'prec':1}, 
            {'title':'EGT',        'type':'gauge', 'scale':4.5,  'NOR':(0, 920), 'LIM':[930],        'ULT':[950], 'prec':1}, 
            {'title':'N2',         'type':'gauge', 'scale':.555, 'NOR':(0, 115), 'ULT':[117], 'prec':1},
        ],[
            {'title':'FF',         'type':'value', 'scale':1.,   'prec':0}, 
            {'title':'OIL/PRESS',  'type':'level', 'scale':1.55, 'ULT':[1], 'LIM':(5, [25]), 'NOR':(29, 125), 'prec':0},
            {'title':'OIL/TEMP',   'type':'level', 'scale':1.6,  'NOR':(0, 110), 'LIM':[114] , 'ULT':[126], 'prec':0 }, 
            {'title':'OIL/QTY %',  'type':'value', 'scale':1.,   'prec':0 },
            {'title':'VIB',        'type':'level', 'scale':0.065,'NOR':(0, 3.8), 'LIM':([4], 5), 'prec':1},
        ],[
            {'title':'PCM %',      'type':'level', 'scale':0.75, 'LIM':(-FPAS_MAX,[-2]), 'NOR':(0, FPAS_MAX), 'offset':FPAS_MAX, 'prec':0}, 
            {'title':'OGV %',      'type':'level', 'scale':0.75, 'NOR':(-OGV_MAX, OGV_MAX), 'offset':OGV_MAX, 'prec':0}, 
            {'title':'VBV %',      'type':'value', 'scale':1.,   'prec':0 },
            {'title':'VSV %',      'type':'value', 'scale':1.,   'prec':0 },
            {'title':'ACC %',      'type':'value', 'scale':1.,   'prec':0 },
        ],[
            {'type':'buttons', 'buttons':['1', '2', '3']},
            {'type':'buttons', 'buttons':['4', '5', '6']},
            {'type':'buttons', 'buttons':['7', '8', '9']},
            {'type':'buttons', 'buttons':['0', 'ENTER']},
        ]]
     
def on_draw():
    type_ = None
    shape = []
    det_lab, det_N1 = '---', '0.0'
    font1 = 'PibotoCondensed'

    EGT = np.interp(N1,[0,20,60,90,100]	,[0,200,600,800,900])
    N2 = np.interp(N1,[0,20,60,90,100]  ,[0,60,80,95,100])
    FF = np.interp(N1,[0,20,60,90,100]	,[0,20,50,70,100])
    VIB = np.interp(N1,[0,20,60,90,100]	,[0,0.1,0.3,0.45,0.5])
        
    values = [[N1, EGT, N2,], [FF, OP, OT, OQ, VIB], [FPAS, OGV, VBV, VSV, ACC], [0,0,0,0]]
    
    # Show header
    x0, y0 = 20, 30
    
    if locked:
        lock_header = (f'Panel locked', 800, 20, red)
    else:
        lock_header = (f'Panel unlocked', 800, 20, green)
        
    for text, dx, size, color in [('TAT', 10, 15, blue), (TAT, 40, 20, white), ('C', 55, 15, white), (det_lab, 100,20, green), lock_header]:
        
        font = pygame.font.SysFont(font1,size, bold = True)
        text = font.render(str(text), True, color, black)
        rect = text.get_rect()
        rect.midbottom = (x0 + dx, y0 )
        screen.blit(text, rect)
    
    # Show columns
    for col in range(columns):
        x0, y0 = 20 + col*250, 45
        
        for value, panel in zip(values[col], panels[col]):
            
            y0 += 5
            
            type_prev = type_
            type_ = panel.get('type', 'value')
            scale = panel.get('scale',1.0)
            title = panel.get('title',False)
            prec = panel.get('prec',0)
            offset = panel.get('offset', 0)          
            value = round(value, prec)

            # Basic dimensions
            if type_ == 'gauge':
                w0, h0, r0 = 200, 150, 65
                y0 += h0
                xt, yt = x0 + w0, y0 - 10 # title center
                xc, yc = x0 + int(w0/2), y0 - r0 # circle center
                wb, hb, thc, vsize = 95, 40,  2, 35
                xb, yb = xc, yc - hb - 10  # value border
                
            elif type_ == 'value':
                w0, h0 = 200, 75
                y0 += h0
                xt, yt = x0 + w0, y0 - int(h0/2) # title center
                wb, hb, thc, vsize = 75, 40,  2, 35
                xb, yb   = x0 + 50, yt - int((hb)/2)  # value border
                
            elif type_ == 'level':
                w0, h0 = 200, 100
                y0 += h0
                xt, yt = x0 + w0, y0 - int(h0/2) # title center
                wb, hb, thc, vsize = 50, 30, 2, 25
                xb, yb  = x0 + 50, yt - int((hb)/2)  # value border                
                xc, yc = xb + wb + 20, y0 - 10

            elif type_ == 'buttons':
                w0, h0 = 200, 60
                y0 += h0
                wb, hb, thc, bsize = 50, 50, 2, 35

            pygame.draw.rect(screen, red, [x0, y0-h0, w0, h0], width = 1)

            # title (index smaller and shifted)
            if title:
                tsize = 20
                if '/' in title:
                    yt -= int(tsize/2)
                
                line = -1
                for txt in title.split('/'):
                    line += 1                
                    if line > 0:
                        yt += tsize + 1
                        
                    font = pygame.font.SysFont(font1,tsize, bold = True)
                    text = font.render(txt, True, blue, black)
                    rect = text.get_rect()
                    rect.center = (xt, yt)
                    screen.blit(text, rect)
                
            # value with border
            if type_ in ['gauge','value','level']:
                pygame.draw.rect(screen, white, [xb, yb, wb, hb], width = thc)            
                font = pygame.font.SysFont(font1,vsize, bold = True)
                text = font.render(str(value), True, white)
                rect = text.get_rect()
                rect.bottomright = (xb + wb - thc, yb + hb + 2)
                screen.blit(text, rect)
     
                # Autothrust Label - detent
                if title == 'N/1':
                    font = pygame.font.SysFont(font1,vsize-2, bold = True)
                    text = font.render(str(det_N1), True, green, black)
                    rect = text.get_rect()
                    rect.bottomright = (xb + w - thc-3, yb)
                    screen.blit(text, rect)
                    
                value += offset

            # gauge arrow & sector
            if type_ == 'gauge':        
                a = value/scale
                #pygame.draw.arc(screen, gray, [xc-r0,yc-r0,2*r0,2*r0], (-a)*rad, (0)*rad, width=2)                
                #pygame.gfxdraw.pie(screen, xc, yc, r0,  0, int(a), gray) 
                
                # Start list of polygon points
                p = [(xc, yc)]

                # Get points on arc
                for n in range(0, int(a)):
                    x = xc + int(r0*math.cos(n*rad))
                    y = yc+int(r0*math.sin(n*rad))
                    p.append((x, y))
                p.append((xc, yc))
                if len(p) > 2:
                    pygame.draw.polygon(screen, gray, p)                
                
                r2 = r0 + 10
                x1, y1 = xc, yc
                x2, y2 = r2*math.cos(a*rad)+xc, r2*math.sin(a*rad) + yc
                pygame.draw.line(screen, white, [x1, y1], [x2, y2], width=3)

            # level arrow 
            if type_ == 'level':
                x1, y1 = xc + 2,  yc - value/scale
                x2, y2 = x1 + 15, y1 + 4
                x3, y3 = x1 + 15, y1 - 4
                pygame.draw.polygon(screen, white, [[x1, y1], [x2, y2], [x3, y3]], width = 0 )
 

            if type_== 'buttons':
                xb, yb = x0, y0 - h0
                for button in panel['buttons']:
                    
                    if not button.isnumeric():
                        wb = 115
                    
                    pygame.draw.rect(screen, white, [xb, yb, wb, hb], width = thc)
                    
                    font = pygame.font.SysFont(font1, bsize, bold = True)
                    text = font.render(str(button), True, white)
                    rect = text.get_rect()
                    rect.center = (xb + int(wb/2), yb + int(hb/2))
                    screen.blit(text, rect)
                    
                    xb += wb + 15

            # Markers & scale divisions
            for lab in ['NOR', 'LIM', 'ULT']:
                markers = []
                rad_sign = []
                if lab not in panel:
                    continue
                
                # single value
                if type(panel[lab]) in [int, float]:
                    a0 = (panel[lab]+offset)/scale
                    a1 = a0

                # list with single value - marker
                elif type(panel[lab]) == list:
                    a0 = (panel[lab][0]+offset)/scale
                    a1 = a0     
                    markers.append(abs(a0))
                    rad_sign.append(np.sign(a0))

                elif type(panel[lab] == tuple):
                    a0, a1 = panel[lab]
                    
                    # first value in [] - marker
                    if type(a0) == list:
                        a0 = (a0[0]+offset)/scale
                        markers.append(abs(a0))
                        rad_sign.append(np.sign(a0))
                    else:
                        a0 = (a0+offset)/scale

                    # second value in [] - marker
                    if type(a1) == list:
                        a1 = (a1[0]+offset)/scale
                        markers.append(abs(a1))
                        rad_sign.append(np.sign(a1))
                    else:
                        a1 = (a1+offset)/scale

                if type_ == 'gauge': 

                    if lab == 'NOR':
                        color, r1 = white,  r0-5
                    elif lab == 'LIM':
                        color, r1 = yellow, r0-1
                    elif lab == 'ULT':
                        color, r1 = red,    r0-1

                    # Arcs
                    da = a1 - a0
                    if da != 0:
                        pygame.gfxdraw.arc(screen, xc, yc, r0,  int(a0), int(a1), white)
                        pygame.gfxdraw.arc(screen, xc, yc, r0-1,  int(a0), int(a1), white)

                    # Markers
                    for a, sign in zip(markers, rad_sign):
                        r2 = r1+sign*10
                        x1, y1 = r1 * math.cos(a * rad) + xc, r1 * math.sin(a * rad) + yc
                        x2, y2 = r2 * math.cos(a * rad) + xc, r2 * math.sin(a * rad) + yc
                        pygame.draw.line(screen, color, [x1, y1], [x2, y2], width=2)
         
                    # Scale division
                    if 'div' in panel and lab == 'NOR':
                        division, modulo = panel['div'] 
                        for d in range(11): 
                            a = d * division
                            r2 = r1 + 5
                            x1, y1 = r1 * math.cos(a * rad) + xc, r1 * math.sin(a * rad) + yc
                            x2, y2 = r2 * math.cos(a * rad) + xc, r2 * math.sin(a * rad) + yc
                            pygame.draw.line(screen, color, [x1, y1], [x2, y2], width=2)
 
                            if d % modulo == 0:
                                rd = r0 - 15
                                xd, yd = rd * math.cos(a * rad) + xc, rd * math.sin(a * rad) + yc
                                font = pygame.font.SysFont(font1,13, bold = True)
                                text = font.render(str(d), True, color)
                                rect = text.get_rect()
                                rect.center = (xd, yd)
                                screen.blit(text, rect)
                             
                elif type_ == 'level':

                    if lab == 'NOR':
                        color, r1, r2 = white,  0, 5
                    elif lab == 'LIM':
                        color, r1, r2 = yellow, 0, 5    
                    elif lab == 'ULT':
                        color, r1, r2 = red,   -2, 8              

                    if a0 != a1:
                        x1, y1 = xc, yc - abs(a0)
                        x2, y2 = xc, yc - abs(a1)
                        pygame.draw.line(screen, color, [x1, y1], [x2, y2], width=2)

                    for a in markers:
                        x1, y1 = xc+r1, yc - abs(a)
                        x2, y2 = xc+r2, yc - abs(a)
                        pygame.draw.line(screen, color, [x1, y1], [x2, y2], width=2)

    x0, y0 = 25, height-30
    txt = "1/Q - N1; 2/W - N2, 3/E - FF, 4/R - OGV, 5/T - FPAS, 6/Y - VBV, 7/U - VSV, 8/I - ACC, S - stop all"
    font = pygame.font.SysFont(font1,20, bold = True)
    text = font.render(txt, True, white, black)
    rect = text.get_rect()
    rect.bottomleft = (x0, y0)
    screen.blit(text, rect)

    
    #text.Label(str(text), x = x0 , y = y0 , font_name = font1, font_size = 10, bold = True, color = (*wh, 255),
    #                               width = 400, align = 'left', anchor_x = 'left', anchor_y = 'bottom', multiline = True))


def on_key_press(event):
    global N1, N2, OGV, FF,  FPAS, VBV, VSV, ACC

    keys = pygame.key.get_pressed()

    if keys[pygame.K_s]:
        print('imidiately stop all motors!')

    if keys[pygame.K_1]:
        N1 += 10
    if keys[pygame.K_q]:
        N1 -= 10        
    N1 = np.interp(N1, [0,100],[0,100])

    if keys[pygame.K_2]:
        N2 += 10
    if keys[pygame.K_w]:
        N2 -= 10
    N2 = np.interp(N2, [0,100],[0,100])

    if keys[pygame.K_3]:
        OGV += 10
    if keys[pygame.K_e]:
        OGV -= 10
    OGV = np.interp(OGV, [-OGV_MAX,OGV_MAX],[-OGV_MAX,OGV_MAX]) 

    if keys[pygame.K_4]:
        FF += 10
    if keys[pygame.K_r]:
        FF -= 10
    FF = np.interp(FF, [0,100],[0,100])    


    if keys[pygame.K_5]:
        FPAS += 10
    if keys[pygame.K_t]:
        FPAS -= 10
    FPAS = np.interp(FPAS, [-FPAS_MAX,FPAS_MAX],[-FPAS_MAX,FPAS_MAX]) 

    if keys[pygame.K_6]:
        VBV += 20
    if keys[pygame.K_y]:
        VBV -= 20
    VBV = np.interp(VBV, [0,100],[0,100]) 

    if keys[pygame.K_7]:
        VSV += 20
    if keys[pygame.K_u]:
        VSV -= 20
    VSV = np.interp(VSV, [0,100],[0,100])

    if keys[pygame.K_8]:
        ACC += 20
    if keys[pygame.K_i]:
        ACC -= 20
    ACC = np.interp(ACC, [0,100],[0,100])
        

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    on_key_press(event)
    
    on_draw()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()    
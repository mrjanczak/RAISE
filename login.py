import PySimpleGUI as sg

def check_login(PIN):
    sg.theme('light grey')

    DISPLAY_FONT = 'Arial 25'
    BUTTON_FONT = 'Arial 12'
    SMALL_BUTTON_COLOR = ('black', 'Gray92')
    BIG_BUTTON_COLOR = ('black', 'LightGrey')
    BUTTONS = (('7','8', '9'),
                ('4','5','6'),
                ('1','2','3'),
                ('0','OK'),)

    def cbut(text, color=SMALL_BUTTON_COLOR, size=(6,3)):
        if len(text) == 1:
            return sg.Button(text, size=size, font=BUTTON_FONT, button_color=color, border_width=2)
        else:
            return sg.Button(text, size=(13,3), font=BUTTON_FONT, button_color=BIG_BUTTON_COLOR, border_width=2)
        
    layout = [[sg.In(font = DISPLAY_FONT, size=(21,1), disabled=True, key='-DISPLAY-')]]
    for row in BUTTONS:
        layout += [[cbut(text) for text in row]]

    window = sg.Window('Provide PIN', layout, element_padding=(0,0), return_keyboard_events=True, margins=(0,0))

    display = ''
    pin = ''
    while True:             # Event Loop
        event, values = window.read()
        if event in (None, 'Exit','OK'):
            break
        if event in '0123456789':
            display += '*'
            pin += event
        window['-DISPLAY-'].update(display)
    window.close()

    if pin == PIN:
        print('pin accepted')
        return True
    else:
        print('wrong pin')
        return False

import PySimpleGUI as sg
import start_up_page
import os
import sys
import serial

timer = 2000

# Get the path to the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Get the path to the sibling directory by joining the script directory with the sibling directory name
database_dir = (os.path.abspath(os.path.join(script_dir, '..', 'Database'))).replace("\\", "/")

# get the database functions to use in the selection page
# Add the path to the directory containing my_module.py to the system path
sys.path.insert(0, database_dir)

# Import the my_module.py module
from query_plant_param import PlantParam


def output(dB: PlantParam, ser, ideal_params):
    # set a colour theme for window
    sg.theme('LightGrey')
    sg.theme_button_color('Grey')
    print(type(ideal_params[0]))
    # getting the screen size to make the window full screen
    screen_width, screen_height = sg.Window.get_screen_size()

    column1 = [[sg.Text("Soil Nitrogen value:", font=("Arial", 20, 'bold'))],
               [sg.Text('0', font=('Arial', 80), size=(10, 1), justification='center', key='NITROGEN')],
               [sg.VerticalSeparator(pad=(0, 15))],
               [sg.Text("Ideal Nitrogen value:", font=("Arial", 20, 'bold'))],
               [sg.Text(ideal_params[0], font=('Arial', 80), size=(10, 1), justification='center')],
               [sg.VerticalSeparator(pad=(0, 25))],
               [sg.Text("Soil Potassium value:", font=("Arial", 20, 'bold'))],
               [sg.Text('0', font=('Arial', 80), size=(10, 1), justification='center', key='POTASSIUM')],
               [sg.VerticalSeparator(pad=(0, 15))],
               [sg.Text("Ideal Potassium value:", font=("Arial", 20, 'bold'))],
               [sg.Text(ideal_params[1], font=('Arial', 80), size=(10, 1), justification='center')]
               ]

    column2 = [[sg.Text("Soil Phosphorus value:", font=("Arial", 20, 'bold'))],
               [sg.Text('0', font=('Arial', 80), size=(10, 1), justification='center', key='PHOSPHORUS')],
               [sg.VerticalSeparator(pad=(0, 15))],
               [sg.Text("Ideal Phosphorus value:", font=("Arial", 20, 'bold'))],
               [sg.Text(ideal_params[2], font=('Arial', 80), size=(10, 1), justification='center')],
               [sg.VerticalSeparator(pad=(0, 25))],
               [sg.Text("Soil Moisture value:", font=("Arial", 20, 'bold'))],
               [sg.Text('0', font=('Arial', 80), size=(10, 1), justification='center', key='MOISTURE')],
               [sg.VerticalSeparator(pad=(0, 15))],
               [sg.Text("Ideal Moisture value:", font=("Arial", 20, 'bold'))],
               [sg.Text(ideal_params[3], font=('Arial', 80), size=(10, 1), justification='center')]
               ]

    # button to close the window
    button_layout = [[sg.Button('Return To Home', size=(100, 3), font=("Arial", 16))]]

    # setting up the layout
    layout = [[sg.Column(column1, size=(500, screen_height)),
               sg.Column(column2, size=(500, screen_height)),
               sg.Column(button_layout)]
              ]

    # Create the window
    window = sg.Window('Current and Ideal Soil Conditions', layout, size=(screen_width, screen_height), location=(0, 0),
                       titlebar_text_color='black', finalize=True, resizable=True)
    n_val = 0
    p_val = 0
    k_val = 0

    while True:
        data = ser.readline().decode('utf-8')
        if data:
            data = data.strip().split(' ')
            print(data)
        event, values = window.read(timeout=timer)
        event, values = window.read(timeout=100)
        # close the window
        if event == sg.WINDOW_CLOSED:
            break
        if event == '__TIMEOUT__':
            # read data from serial port
            data = ser.readline().decode().strip().split(' ')
            if data:
                # update the output window
                if data[0] == "Nitrogen" and data[1] == "value:":
                    n_val = int(data[4])
                    if n_val >= ideal_params[0]:
                        window['NITROGEN'].update(n_val, text_color='green')
                    else:
                        window['NITROGEN'].update(n_val, text_color='red')
                elif data[0] == "Phosphorous" and data[1] == "value:":
                    p_val = int(data[4])
                    if p_val >= ideal_params[1]:
                        window['PHOSPHORUS'].update(p_val, text_color='green')
                    else:
                        window['PHOSPHORUS'].update(p_val, text_color='red')
                elif data[0] == "Potassium" and data[1] == "value:":
                    k_val = int(data[4])
                    if p_val >= ideal_params[2]:
                        window['POTASSIUM'].update(k_val, text_color='green')
                    else:
                        window['POTASSIUM'].update(k_val, text_color='red')
                elif data[0] == "Modal":
                    m_val = int(data[3])
                    if p_val >= ideal_params[3]:
                        window['MOISTURE'].update(m_val, text_color='green')
                    else:
                        window['MOISTURE'].update(m_val, text_color='red')
        if event == 'Return To Home':
            window.close()
            start_up_page.start_up_page(dB, ser)
            break
    window.close()
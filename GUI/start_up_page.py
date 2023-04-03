import PySimpleGUI as sg                        # Part 1 - The import
import selection_page
import output
import os
import sys
import serial


# Get the path to the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Get the path to the sibling directory by joining the script directory with the sibling directory name
database_dir = (os.path.abspath(os.path.join(script_dir, '..', 'Database'))).replace("\\", "/")

# Print the path to the sibling directory
print(database_dir)

# get the database functions to use in the selection page
# Add the path to the directory containing my_module.py to the system path
sys.path.insert(0, database_dir)

# Import the my_module.py module
from query_plant_param import PlantParam


def start_up_page(dB : PlantParam, ser):
    sg.theme('LightGrey')
    sg.theme_button_color('Grey')

    # Get screen resolution
    screen_width, screen_height = sg.Window.get_screen_size()

    button1 = sg.Button('Select Plant To Monitor', font=("Arial", 18), button_color=('black', 'grey'))
    button2 = sg.Button('Monitor Current Plant',font=("Arial", 18), button_color=('black', 'grey'))

    # Define the window's contents
    layout = [
        [sg.Text("Smart Plant Care Control System", justification = 'center', expand_x= True,
                 font= ("Arial", 40))],
        [sg.Column([[sg.Text('', size=(1, 4))]], element_justification='center')],
        [sg.Image(filename='startup.png', expand_x= True)],
        [sg.Column([[sg.Text('', size=(1, 4))]], element_justification='center')],
        [sg.Column([[button1, button2]], justification='center', element_justification='center')]
    ]

    # Create the window
    window = sg.Window('Smart Plant Care Control Start Up Page',
                       layout, size = (screen_width, screen_height), location = (0,0))


    while True:
        data = ser.readline().decode('utf-8')
        if data:
            data = data.strip().split(' ')
            print(data)
        # Display and interact with the Window
        event, values = window.read()                   # Part 4 - Event loop or Window.read call
        print(event)
        if event == sg.WINDOW_CLOSED:
            break
        # if select plant to monitor load selection page
        elif event == 'Select Plant To Monitor':
            print(event)
            window.close()
            selection_page.selection_page(dB,ser)
            break
        # if select monitoring page go to the monitoring page
        elif event == 'Monitor Current Plant':
            window.close()
            output.output(dB,ser)
            break


    # Finish up by removing from the screen
    window.close()                                  # Part 5 - Close the Window


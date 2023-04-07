import PySimpleGUI as sg                        # Part 1 - The import
import selection_page
import output
import os
import sys
import serial
import csv


# Get the path to the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Get the path to the sibling directory by joining the script directory with the sibling directory name
database_dir = (os.path.abspath(os.path.join(script_dir, '..', 'Database'))).replace("\\", "/")

# Get the path to the input CSV file
csv_dir = (os.path.abspath(os.path.join(script_dir, '..', 'Controller'))).replace("\\", "/") + "/IntegratedControl"

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
        event, values = window.read(timeout=1000)                   # Part 4 - Event loop or Window.read call
        if event == sg.WINDOW_CLOSED:
            break
        # if select plant to monitor load selection page
        elif event == 'Select Plant To Monitor':
            window.close()
            selection_page.selection_page(dB, ser)
            break
        # if select monitoring page go to the monitoring page
        # this will give an error: need to check this
        elif event == 'Monitor Current Plant':
            # read selected parameters from the csv file
            # open the CSV file for reading
            file_path = csv_dir + "/inputToArduino.csv"
            with open(file_path, 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                # skip the header row
                next(csvreader)
                # read the second row
                my_array = next(csvreader)
                my_array.pop(0)
                my_array = [int(i) for i in my_array]
            window.close()
            output.output(dB,ser, my_array)
            break

    # Finish up by removing from the screen
    window.close()                                  # Part 5 - Close the Window


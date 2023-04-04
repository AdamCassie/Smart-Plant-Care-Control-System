import PySimpleGUI as sg
import selection_page
import start_up_page
import output
import csv
import os
import sys
import serial

timer = 2000

# Get the path to the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Get the path to the sibling directory by joining the script directory with the sibling directory name
database_dir = (os.path.abspath(os.path.join(script_dir, '..', 'Database'))).replace("\\", "/")

# Get the path to the input CSV file
csv_dir = (os.path.abspath(os.path.join(script_dir, '..', 'Controller'))).replace("\\", "/") + "/IntegratedControl"


# get the database functions to use in the selection page
# Add the path to the directory containing my_module.py to the system path
sys.path.insert(0, database_dir)

# Import the my_module.py module
from query_plant_param import PlantParam

def registration_page(dB : PlantParam, ser):
    # set a colour theme for window
    sg.theme('LightGrey')
    sg.theme_button_color('Grey')

    # getting the screen size to make the window fullscreen
    screen_width, screen_height = sg.Window.get_screen_size()

    layout = [
        [sg.Text('', size=(1, 2), font=('Arial', 20))],
        [sg.Text('Plant type', font=("Arial", 20)), sg.InputText(key = '-PlantType-',background_color='lightgrey', text_color='black',
                                                                 font=("Arial", 20))],

        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Text('Required moisture level (%)', font=("Arial", 20)), sg.InputText(key = '-Moisture-',background_color='lightgrey',
                                                                              text_color='black', font=("Arial", 20))],
        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Text('Required Nitrogen level (mg/kg)', font=("Arial", 20)), sg.InputText(key = '-Nitrogen-',
                                                                                      background_color='lightgrey',
                                                                                      text_color='black',
                                                                                      font=("Arial", 20))],
        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Text('Required Phosphorus level (mg/kg)', font=("Arial", 20)), sg.InputText(key = '-Phosphorous-',
                                                                                        background_color='lightgrey',
                                                                                        text_color='black',
                                                                                        font=("Arial", 20))],
        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Text('Required Potassium level (mg/kg)', font=("Arial", 20)), sg.InputText(key = '-Potassium-',
                                                                                       background_color='lightgrey',
                                                                                       text_color='black',
                                                                                       font=("Arial", 20))],
        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Button('Confirm Registration', font=("Arial", 16)), sg.Button('Cancel', font=("Arial", 16),
                                                                           button_color=('white','darkred'))],
        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Text("", key= '-Error-', font=("Arial", 20), text_color = 'red')]

    ]

    window = sg.Window('Registration', layout, resizable=True, size=(screen_width, screen_height))

    while True:
        data = ser.readline().decode('utf-8')
        if data:
            data = data.strip().split(' ')
            print(data)
        event, values = window.read(timeout=timer)
        if event == sg.WINDOW_CLOSED:

            break
        elif event == 'Confirm Registration':

            # handle registration logic here
            # checking for invalid input (empty strings)
            invalid = True

            # check the input parameters for validity
            if values['-PlantType-'] == '' or values['-Moisture-'] == '' or values['-Nitrogen-'] == '' or values['-Phosphorous-'] == '' or values['-Potassium-'] == '':

                invalid = True
                window['-Error-'].update(value="Please ensure all text-fields are completed")
            elif int(values['-Moisture-']) > 100 or int(values['-Moisture-']) < 0:

                invalid = True
                window['-Error-'].update(value="Moisture should be within 0 and 100%")
            elif int(values['-Nitrogen-']) < 0 or int(values['-Nitrogen-']) > 1999 :

                invalid = True
                window['-Error-'].update(value="Nitrogen should be between 0 and 1999 mg/Kg")
            elif int(values['-Phosphorous-']) < 0 or int(values['-Phosphorous-']) > 1999 :

                invalid = True
                window['-Error-'].update(value="Phosphorous should be between 0 and 1999 mg/Kg")
            elif int(values['-Potassium-']) < 0 or int(values['-Potassium-']) > 1999 :

                invalid = True
                window['-Error-'].update(value="Potassium should be between 0 and 1999 mg/Kg")
            else:

                invalid = False
            #push valid values
            # go to monitoring page
            if not invalid:

                # write the selected params to the csv file
                # open the CSV file for writing
                file_path = csv_dir + "/inputToArduino.csv"
                with open(file_path, 'w', newline='') as csvfile:
                    csvfile.write('')
                    # create a CSV writer object
                    csvwriter = csv.writer(csvfile)

                    # write a row of column headers
                    csvwriter.writerow(['Plant Name', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous'])
                    csvwriter.writerow([values['-PlantType-'],values['-Moisture-'],values['-Nitrogen-'],
                                       values['-Phosphorous-'],values['-Potassium-']])

                # update the database
                dB.add_plant_params(values['-PlantType-'], int(values['-Moisture-']),
                                    int(values['-Nitrogen-']), int(values['-Phosphorous-']),
                                    int(values['-Potassium-']))

                my_array = dB.get_plant_params(values['-PlantType-'])

                # Convert the array to a string
                array_string = str(my_array)

                # Remove the parentheses from the string
                array_string = array_string.replace("(", "")
                array_string = array_string.replace(")", "")

                # print("selected parameters are ", my_array)

                ser.write(bytes(array_string, 'utf-8'))  # send the array to the Arduino over Serial

                window.close()
                output.output(dB, ser, my_array)
                break



        elif event == 'Cancel':
            window.close()
            # send back to homepage
            start_up_page.start_up_page(dB, ser)
            break

    window.close()
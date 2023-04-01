import PySimpleGUI as sg
import selection_page
import start_up_page
import output
import csv

def registration_page():
    # set a colour theme for window
    sg.theme('LightGrey')
    sg.theme_button_color('Grey')

    # getting the screen size to make the window fullscreen
    screen_width, screen_height = sg.Window.get_screen_size()

    layout = [
        [sg.Text('', size=(1, 2), font=('Arial', 20))],
        [sg.Text('Plant type', font=("Arial", 20)), sg.InputText(background_color='lightgrey', text_color='black',
                                                                 font=("Arial", 20))],

        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Text('Required moisture level', font=("Arial", 20)), sg.InputText(background_color='lightgrey',
                                                                              text_color='black', font=("Arial", 20))],
        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Text('Required Nitrogen level (mg/kg)', font=("Arial", 20)), sg.InputText(background_color='lightgrey',
                                                                                      text_color='black',
                                                                                      font=("Arial", 20))],
        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Text('Required Phosphorus level (mg/kg)', font=("Arial", 20)), sg.InputText(background_color='lightgrey',
                                                                                        text_color='black',
                                                                                        font=("Arial", 20))],
        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Text('Required Potassium level (mg/kg)', font=("Arial", 20)), sg.InputText(background_color='lightgrey',
                                                                                       text_color='black',
                                                                                       font=("Arial", 20))],
        [sg.VerticalSeparator(pad=(0, 25))],
        [sg.Button('Confirm Registration', font=("Arial", 16)), sg.Button('Cancel', font=("Arial", 16),
                                                                           button_color=('white','darkred'))]
    ]

    window = sg.Window('Registration', layout, resizable=True, size=(screen_width, screen_height))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Confirm Registration':
            # rows of input
            row = []
            # handle registration logic here
            # checking for invalid input (empty strings)
            invalid = False
            for i in values:
                row.append(values[i])
                if(values[i] == ''):
                    # tell the user that input was invalid
                    print('invalid input')
                    invalid = True
                    break
            if(invalid):
                break
            #push valid values
            # go to monitoring page
            if (not(invalid)):
                # write the selected params to the csv file
                # open the CSV file for writing
                with open('inputToArduino.csv', 'w', newline='') as csvfile:
                    csvfile.write('')
                    # create a CSV writer object
                    csvwriter = csv.writer(csvfile)

                    # write a row of column headers
                    csvwriter.writerow(['Plant Name', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous'])
                    csvwriter.writerow(row)

                window.close()
                output.output()
                break



        elif event == 'Cancel':
            window.close()
            # send back to homepage
            start_up_page.start_up_page()
            break

    window.close()
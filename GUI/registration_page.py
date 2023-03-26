import PySimpleGUI as sg
import selection_page
import start_up_page

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
        [sg.Text('Soil type', font=("Arial", 20)), sg.InputText(background_color='lightgrey', text_color='black',
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
            # handle registration logic here
            # checking for invalid input (empty strings)
            invalid = False
            for i in values:
                if(values[i] == ''):
                    # tell the user that input was invalid
                    print('invalid input')
                    invalid = True
                    break
            break


        elif event == 'Cancel':
            window.close()
            # send back to homepage
            start_up_page.start_up_page()
            break

    window.close()
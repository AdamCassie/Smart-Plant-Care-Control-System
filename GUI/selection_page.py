import PySimpleGUI as sg                        # Part 1 - The import


def selection_page():
    # set a colour theme for window
    sg.theme('LightGrey')
    #sg.theme_background_color('Black')
    sg.theme_button_color('Grey')

    # Get screen resolution
    screen_width, screen_height = sg.Window.get_screen_size()

    # data for plant drop down menu
    plantNames = ["Plant 1", "Plant 2", "Plant 3"] # replace with a query to database
    # data for soil drop down menu
    soilNames = ["Loamy", "Gravel", "Red Sand", "Over burdden"] # replace with a query to database

    # Define the window's input contents
    inputColumn = [[sg.Text("Select your plant from the list", font = ("Arial", 20))],     # Part 2 - The Layout
                [sg.Combo(plantNames, size = (50,150), key = "-OPTION1-", background_color= 'lightgrey',
                          text_color= 'black',enable_events = True, font=("Arial", 16))],
                [sg.Column([[sg.Text('', size=(1, 3))]], element_justification='center')],
                [sg.Text("Select your soil type for plant from the list", font = ("Arial", 20))],
                [sg.Combo(soilNames,  size = (50,150), key = "-OPTION2-", background_color= 'lightgrey',
                          text_color= 'black',enable_events = True, font=("Arial", 16))],
                [sg.Column([[sg.Text('', size=(1, 3))]], element_justification='center')],
                [sg.Text("If plant or soil type not found, click register to register new control parameters",
                         font = ("Arial", 20), size = (40,None), auto_size_text = True)],
                [sg.Column([[sg.Text('', size=(1, 3))]], element_justification='center')],
                [sg.Button('Go to Plant Registration',font=("Arial",16)),
                 sg.Button('Cancel Plant Selection',font=("Arial",16), button_color=('white','darkred'))]]

    OutputColumn = [[sg.Text("Control Values selected",font=("Arial",20))],
                    [sg.Text("Plant Selected: ", font=("Arial",20)),sg.Text("", key = "-OUTPUT1-", font=("Arial",20))],
                    [sg.Text("Soil Type Selected: ", font=("Arial",20)),sg.Text("", key = "-OUTPUT2-", font=("Arial",20))],
                    [sg.Text("Soil Moisture Level: ", font=("Arial",20)), sg.Text("", key = "-MOISTURE-", font=("Arial",20))],
                    [sg.Text("Nitrogen Level: ", font=("Arial",20)), sg.Text("", key = "-Nitrogen-", font=("Arial",20)),
                     sg.Text("mg/kg", font=("Arial",20))],
                    [sg.Text("Phosphorous Level: ", font=("Arial",20)), sg.Text("", key = "-Phosphorous-", font=("Arial",20)),
                     sg.Text("mg/kg", font=("Arial",20))],
                    [sg.Text("Potassium Level: ", font=("Arial",20)), sg.Text("", key = "-Potassium-", font=("Arial",20)),
                     sg.Text("mg/kg", font=("Arial",20))],
                    [sg.Column([[sg.Text('', size=(1, 1))]], element_justification='center')],
                    [sg.Button('Confirm Control Parameters Selection', font=("Arial",16))]]

    layout = [[sg.Column(inputColumn, size = (750,1500)),
               sg.VSeparator(),
               sg.Column(OutputColumn, size = (750,1500))]]

    # Create the window
    window = sg.Window('Plant Selection', layout, titlebar_text_color= 'black',
                       size=(screen_width, screen_height), location=(0, 0)
                       ,resizable = True)      # Part 3 - Window Defintion

    while True:
        # Display and interact with the Window
        event, values = window.read()                   # Part 4 - Event loop or Window.read call
        # clean up when window closed
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        # when plant selected output the selected plant
        elif event == "-OPTION1-":
            window["-OUTPUT1-"].update(value=values["-OPTION1-"])
        # when soil selected output the selected soil type
        elif event == "-OPTION2-":
            window["-OUTPUT2-"].update(value=values["-OPTION2-"])
        elif event == 'Cancel Plant Selection':
            window.close();
            sg.UserSettings().add('active_window', 'window_home')

        # query the database for the Nitrogen Potassium and Phosphorous levels and print them to the screen

        # Finish up by removing from the screen
        if event == 'Cancel Plant Selection' or event == 'Confirm Control Parameters Selection':
            window.close()                                  # Part 5 - Close the Window


    window.close()

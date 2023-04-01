import PySimpleGUI as sg                        # Part 1 - The import
import output
import registration_page
import start_up_page
import csv
import os
import sys

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



def selection_page(dB : PlantParam):
    # create an instance of the database

    # set a colour theme for window
    sg.theme('LightGrey')
    sg.theme_button_color('Grey')

    # Get screen resolution
    screen_width, screen_height = sg.Window.get_screen_size()

    # data for plant drop down menu
    plantNames = dB.get_all_plant_types() # replace with a query to database
    # data for soil drop down menu
    soilNames = ["Loamy", "Gravel", "Red Sand", "Over burdden"] # replace with a query to database

    # Define the window's input contents
    inputColumn = [[sg.Text("Select your plant from the list", font = ("Arial", 20))],     # Part 2 - The Layout
                [sg.Combo(plantNames, size = (50,150), key = "-OPTION1-", background_color= 'lightgrey',
                          text_color= 'black',enable_events = True, font=("Arial", 16))],
                [sg.Column([[sg.Text('', size=(1, 3))]], element_justification='center')],
                [sg.Text("If plant type not found, click register to register new control parameters",
                         font = ("Arial", 20), size = (40,None), auto_size_text = True)],
                [sg.Column([[sg.Text('', size=(1, 3))]], element_justification='center')],
                [sg.Button('Go to Plant Registration',font=("Arial",16)),
                 sg.Button('Cancel Plant Selection',font=("Arial",16), button_color=('white','darkred'))]]

    OutputColumn = [[sg.Text("Control Values selected",font=("Arial",20))],
                    [sg.Text("Plant Selected: ", font=("Arial",20)),sg.Text("", key = "-OUTPUT1-", font=("Arial",20))],
                    [sg.Text("Moisture Level: ", font=("Arial", 20)), sg.Text("", key="-Moisture-", font=("Arial", 20)),
                     sg.Text("mg/kg", font=("Arial", 20))],
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
            # query to get selected plant parameters
            selected_prams = list(dB.get_plant_params(values["-OPTION1-"]))
            window["-Moisture-"].update(value=selected_prams[0])
            window["-Nitrogen-"].update(value=selected_prams[1])
            window["-Phosphorous-"].update(value=selected_prams[2])
            window["-Potassium-"].update(value=selected_prams[3])
        elif event == 'Go to Plant Registration':
            window.close()
            registration_page.registration_page()
            break
        elif event == 'Confirm Control Parameters Selection':
            # write selected parameters to the csv file
            # open the CSV file for writing
            with open('inputToArduino.csv', 'w', newline='') as csvfile:
                csvfile.write('')
                # create a CSV writer object
                csvwriter = csv.writer(csvfile)
                row = dB.get_plant_params(values["-OPTION1-"])
                # write a row of column headers
                csvwriter.writerow(['Plant Name','Moisture','Nitrogen', 'Potassium', 'Phosphorous'])
                row = [values["-OPTION1-"]] + list(row)
                csvwriter.writerow(row)

            window.close()
            output.output()
            break

        elif event == 'Cancel Plant Selection':
            window.close()
            # send back to homepage
            start_up_page.start_up_page(dB)
            break

        # query the database for the Nitrogen Potassium and Phosphorous levels and print them to the screen

    window.close()

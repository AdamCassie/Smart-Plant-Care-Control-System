import PySimpleGUI as sg


# Create the PySimpleGUI layout
layout = [
    [sg.Button('Close')]
]

# Create the PySimpleGUI window
window = sg.Window('Registration', layout, size=(1500,1500),location=(0,0),finalize=True)

# Run the PySimpleGUI event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        break

# Close the window
window.close()
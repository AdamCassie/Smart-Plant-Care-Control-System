import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import start_up_page


def output_and_monitoring_page():
    # set a colour theme for window
    sg.theme('LightGrey')
    sg.theme_button_color('Grey')

    # Create some data to plot (time)
    x = np.linspace(0, 24, 25)

    # adding moisture, N, P and K values to plot. these will have to be replaced by actual data from arduino and database
    # moisture
    moisture_real = np.cos(x)
    moisture_ideal = np.linspace(5, 5, 25)

    # nitrogen
    N_real = np.cos(x)
    N_ideal = np.linspace(5, 5, 25)

    # phosphorus
    P_real = np.cos(x)
    P_ideal = np.linspace(5, 5, 25)

    # potassium
    K_real = np.cos(x)
    K_ideal = np.linspace(5, 5, 25)

    # creating the figures
    # moisture
    moisture_figure = plt.Figure(figsize=(7, 4), dpi=100)
    ax1 = moisture_figure.add_subplot()
    ax1.plot(x, moisture_real, color='blue', label='Soil moisture value')
    ax1.plot(x, moisture_ideal, color='green', label='Ideal moisture value')
    ax1.legend()
    ax1.set_xlabel('Time (hours)')
    ax1.set_xticks(x)

    # N
    N_figure = plt.Figure(figsize=(7, 4), dpi=100)
    ax2 = N_figure.add_subplot()
    ax2.plot(x, N_real, color='red', label='Soil N value')
    ax2.plot(x, N_ideal, color='green', label='Ideal N value')
    ax2.legend()
    ax2.set_xlabel('Time (hours)')
    ax2.set_xticks(x)

    # P
    P_figure = plt.Figure(figsize=(7, 4), dpi=100)
    ax3 = P_figure.add_subplot()
    ax3.plot(x, P_real, color='purple', label='Soil P value')
    ax3.plot(x, P_ideal, color='green', label='Ideal P value')
    ax3.legend()
    ax3.set_xlabel('Time (hours)')
    ax3.set_xticks(x)

    # K
    K_figure = plt.Figure(figsize=(7, 4), dpi=100)
    ax4 = K_figure.add_subplot()
    ax4.plot(x, K_real, color='orange', label='Soil K value')
    ax4.plot(x, K_ideal, color='green', label='Ideal K value')
    ax4.legend()
    ax4.set_xlabel('Time (hours)')
    ax4.set_xticks(x)

    # creating the layouts for the window
    # left hand side - moisture and N
    graph_layout_1 = [[sg.Graph((600, 400), (0, 0), (600, 400), key='-MOISTURE-')],
                      [sg.Graph((600, 400), (0, 0), (600, 400), key='-N-')]]

    # right hand side - P and K
    graph_layout_2 = [[sg.Graph((600, 400), (0, 0), (600, 400), key='-P-')],
                      [sg.Graph((600, 400), (0, 0), (600, 400), key='-K-')]]

    # button to close the window
    button_layout = [[sg.Button('Close')]]
    # button to return to home
    button_home = [sg.Button('Return to Home')]
    # getting the screen size to make the window fullscreen
    screen_width, screen_height = sg.Window.get_screen_size()

    # setting up the layout
    layout = [[sg.Column(graph_layout_1, size=(700, screen_height)),
               sg.Column([], size=((screen_width - 2000) // 2, screen_height)),
               sg.Column(graph_layout_2, size=(700, screen_height)),
               sg.Column(button_layout),
               sg.Column(button_home)]
              ]

    # Create the window
    window = sg.Window('Current and Ideal Soil Conditions', layout, size=(screen_width, screen_height), location=(0, 0),
                       titlebar_text_color='black', finalize=True, resizable=True)

    # Add the Figure objects to the Graph elements on the window
    # moisture
    fig_canvas1 = FigureCanvasTkAgg(moisture_figure, window['-MOISTURE-'].TKCanvas)
    fig_canvas1.draw()
    fig_canvas1.get_tk_widget().pack(side='top', fill='both', expand=1)

    # N
    fig_canvas2 = FigureCanvasTkAgg(N_figure, window['-N-'].TKCanvas)
    fig_canvas2.draw()
    fig_canvas2.get_tk_widget().pack(side='top', fill='both', expand=1)

    # P
    fig_canvas3 = FigureCanvasTkAgg(P_figure, window['-P-'].TKCanvas)
    fig_canvas3.draw()
    fig_canvas3.get_tk_widget().pack(side='top', fill='both', expand=1)

    # K
    fig_canvas4 = FigureCanvasTkAgg(K_figure, window['-K-'].TKCanvas)
    fig_canvas4.draw()
    fig_canvas4.get_tk_widget().pack(side='top', fill='both', expand=1)

    # Wait for user interaction and close the window
    while True:
        event, values = window.read()
        # close the window
        if event == sg.WINDOW_CLOSED or event == 'Close':
            break
        if event == 'Return To Home':
            window.close()
            start_up_page.start_up_page()
            break

    window.close()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

# Create some data to plot
x = np.linspace(0, 24, 25)

# adding moisture, N, P and K values to plot
# moisture
moisture_real = np.cos(x)
moisture_ideal = np.linspace(5,5,25)

# nitrogen
N_real = np.cos(x)
N_ideal = np.linspace(5,5,25)

# phosphorus
P_real = np.cos(x)
P_ideal = np.linspace(5,5,25)

# potassium
K_real = np.cos(x)
K_ideal = np.linspace(5,5,25)

# Create the PySimpleGUI layout
layout = [
    [sg.Canvas(size=(800, 1200), key='canvas')],
    [sg.Button('Close')]
]

# Create the PySimpleGUI window
window = sg.Window('Graphs', layout, size=(1500,1500),location=(0,0),finalize=True)

# Create a single Figure object for all the plots
figure = plt.figure(figsize=(15, 15))

# Add each plot to the figure using add_subplot
# moisture plot
ax1 = figure.add_subplot(4,1, 1)
ax1.plot(x, moisture_real, color='blue', label='Soil moisture value')
ax1.plot(x, moisture_ideal, color='green', label='Ideal moisture value')
ax1.legend()
ax1.set_xlabel('Time (hours)')
ax1.set_xticks(x)

# nitrogen plot
ax2 = figure.add_subplot(4,1, 2)
ax2.plot(x, N_real, color='red', label='Soil N value')
ax2.plot(x, N_ideal, color='green', label='Ideal N value')
ax2.legend()
ax2.set_xlabel('Time (hours)')
ax2.set_xticks(x)

# phosphorus plot
ax3 = figure.add_subplot(4,1, 3)
ax3.plot(x, P_real, color='purple', label='Soil P value')
ax3.plot(x, P_ideal, color='green', label='Ideal P value')
ax3.legend()
ax3.set_xlabel('Time (hours)')
ax3.set_xticks(x)

# potassium plot
ax4 = figure.add_subplot(4,1, 4)
ax4.plot(x, K_real, color='orange', label='Soil K value')
ax4.plot(x, K_ideal, color='green', label='Ideal K value')
ax4.legend()
ax4.set_xlabel('Time (hours)')
ax4.set_xticks(x)

figure.subplots_adjust(hspace=1.25)

# Draw the figure on the canvas
canvas = window['canvas'].TKCanvas
figure_canvas = FigureCanvasTkAgg(figure, canvas)
figure_canvas.draw()
figure_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

# Run the PySimpleGUI event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        break

# Close the window
window.close()


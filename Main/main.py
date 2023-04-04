"""
=== Module Description ===

This is the main file for the Smart Plant Care Control System. It executes
the GUI (Python script) and the Integrated Controller (Arduino code) at
the same time.
"""

import multiprocessing
import serial
import time
import os
import sys

from multiprocessing import Process, Lock

# Define a function to run the Arduino file
def run_controller(lock):
    with lock:
        # Get the path to the directory containing the current script
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Get the path to the GUI directory by joining the script directory with the sibling directory name
        controller_dir = (os.path.abspath(os.path.join(script_dir, '..', 'Controller/IntegratedControl'))).replace("\\", "/")
        print(f"Controller directory is: {controller_dir}")

        # set the port name and baud rate
        port = "COM3"
        # valid_port = False
        # while(valid_port == False):
        #     port = input("Please enter the port for the Arduino board: ").upper()
        #     if port in ["COM3", "COM4"]:
        #         print(f"Valid port {port} chosen for Arduino.")
        #         valid_port = True
        #     else:
        #         print("Invalid port entered. Try again.")
        baudrate = 4800

        # create a serial connection
        ser = serial.Serial(port, baudrate, timeout=1)

        # wait for the arduino to reset
        time.sleep(2)

        # read any data that may be in the input buffer
        ser.flushInput()

        # change to the arduino directory
        os.chdir(controller_dir)

        # send a command to the arduino to start the program
        ser.write(b'start\n')

        # wait for the arduino to respond
        response = ser.readline()

        # print the response
        print(response)

        # close the serial connection
        ser.close()

# Define a function to run the other Python script
def run_gui(lock):
    with(lock):
        # Get the path to the directory containing the current script
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Get the path to the GUI directory by joining the script directory with the sibling directory name
        gui_dir = (os.path.abspath(os.path.join(script_dir, '..', 'GUI'))).replace("\\", "/")
        print(f"GUI directory is: {gui_dir}")


        # change to the python directory
        os.chdir(gui_dir)

        import main

if __name__ == '__main__':
    lock = Lock()
    # Create two processes to run the Arduino and Python scripts concurrently
    p1 = Process(target=run_controller, args=(lock,))
    p2 = Process(target=run_gui, args=(lock,))

    # Start the processes
    p1.start()
    p2.start()

    # Wait for the processes to finish
    p1.join()
    p2.join()


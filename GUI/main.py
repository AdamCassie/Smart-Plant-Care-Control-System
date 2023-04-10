import start_up_page
import os
import sys
import serial


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
import query_plant_param

port = None
ser = None
valid_port = False
while(valid_port == False):
    port = input("Please enter the port for the Arduino board: ").upper()
    try:
        ser = serial.Serial(port, 4800, timeout=1)
        valid_port = True
    except serial.serialutil.SerialException:
        print(f"Invalid port {port} entered. Try again.")

pp = PlantParam()
qf = None
try:
    # TODO: Change the values of the following variables to connect to your
    #  own database:
    dbname = 'plantcare'
    user = 'postgres'
    password = 'password'

    connected = pp.connect(dbname, user, password)

    # The following is an assert statement. It checks that the value for
    # connected is True. The message after the comma will be printed if
    # that is not the case (connected is False).
    # Use the same notation to thoroughly test the methods we have provided
    assert connected, f"[Connected] Expected True | Got {connected}."

    # TODO: Test one or more methods here, or better yet, make more testing
    #   functions, with each testing a different aspect of the code.

    # The following function will set up the testing environment by loading
    # the sample data we have provided into your database. You can create
    # more sample data files and use the same function to load them into
    # your database.
    # Note: make sure that the schema and data files are in the same
    # directory (folder) as your query_plant_param.py file.
    query_plant_param.setup(dbname, user, password, database_dir)

    # Delete csv file with input for Arduino (if it exists)
    csv_file = csv_dir + "/inputToArduino.csv"
    if os.path.isfile(csv_file):
        os.remove(csv_file)
        print(f"The csv file {csv_file} has been deleted.")
    else:
        print(f"The csv file {csv_file} does not exist.")


    # Go to startup page
    start_up_page.start_up_page(pp, ser)

    # while True:
    #     data = ser.readline().decode('utf-8')
    #     if data:
    #         1data = data.strip().split(' ')
    #         print(data)

finally:
    if qf and not qf.closed:
        qf.close()
    pp.disconnect()

sys.exit()


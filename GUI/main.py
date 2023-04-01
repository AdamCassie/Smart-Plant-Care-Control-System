import start_up_page
import sys

# get the database functions to use in the selection page
# Add the path to the directory containing my_module.py to the system path
sys.path.insert(0, 'C:/Users/vishn/OneDrive/Documents/GitHub/ECE496/Database')

# Import the my_module.py module
from query_plant_param import PlantParam


pp = PlantParam()
qf = None
try:
    # TODO: Change the values of the following variables to connect to your
    #  own database:
    dbname = 'csc343h-cassiead'
    user = 'cassiead'
    password = ''

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
    setup(dbname, user, password, './plant_param_data.sql')

finally:
    if qf and not qf.closed:
        qf.close()
    pp.disconnect()

start_up_page.start_up_page()
print("Execute")
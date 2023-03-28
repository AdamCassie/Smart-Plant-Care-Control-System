"""
=== Module Description ===

This file contains the PlantParam class and some simple testing functions.
"""

# import datetime as dt
import psycopg2 as pg
import psycopg2.extensions as pg_ext
import psycopg2.extras as pg_extras
from typing import Optional, TextIO


class PlantParam:
    """A class that can work with data conforming to the schema in
    plant_param_schema.ddl.

    === Instance Attributes ===
    connection: connection to a PostgreSQL database of a waste management
    service.

    Representation invariants:
    - The database to which connection is established conforms to the schema
      in plant_param_schema.ddl.
    """
    connection: Optional[pg_ext.connection]

    def __init__(self) -> None:
        """Initialize this PlantParam instance, with no database connection
        yet.
        """
        self.connection = None

    def connect(self, dbname: str, username: str, password: str) -> bool:
        """Establish a connection to the database <dbname> using the
        username <username> and password <password>, and assign it to the
        instance attribute <connection>. In addition, set the search path
        to plant_param.

        Return True if the connection was made successfully, False otherwise.
        I.e., do NOT throw an error if making the connection fails.

        >>> pp = PlantParam()
        >>> pp.connect("csc343h-cassiead", "cassiead", "")
        True
        >>> # In this example, the connection cannot be made.
        >>> pp.connect("invalid", "nonsense", "incorrect")
        False
        """
        try:
            self.connection = pg.connect(
                dbname=dbname, user=username, password=password,
                options="-c search_path=plant_param"
            )
            return True
        except pg.Error:
            return False

    def disconnect(self) -> bool:
        """Close this PlantParam's connection to the database.

        Return True if closing the connection was successful, False otherwise.
        I.e., do NOT throw an error if closing the connection failed.

        >>> pp = PlantParam()
        >>> pp.connect("csc343h-cassiead", "cassiead", "")
        True
        >>> pp.disconnect()
        True
        """
        try:
            if self.connection and not self.connection.closed:
                self.connection.close()
            return True
        except pg.Error:
            return False

    def get_plant_params(self, plant_type: str) -> tuple:
        """Given the type of a plant <plant_type>, which is represented by a
        string, query the database for the ideal moisture, Nitrogen, Phosphorous
        and Potassium levels of this plant type. If found, return a tuple
        containing the ideal parameter values inthe following format:
        (<moisture_target>, <nitrogen_target>, <phosphorous_target>, <potassium_target>).
        Else, return and empty tuple
        """
        try:
            cur = self.connection.cursor()

            result = tuple()

            cur.execute(
                'SELECT moistureTarget, nitrogenTarget, phosphorousTarget, potassiumTarget FROM IdealPlantParams WHERE plantType=%s;', [plant_type])

            if cur.rowcount == 0:
                print(f"Plant type {plant_type} not found in the database.")
                cur.close()
                return result

            result = cur.fetchone()
            cur.close()
            return result

        except pg.Error as ex:
            # You may find it helpful to uncomment this line while debugging,
            # as it will show you all the details of the error that occurred:
            # raise ex
            return 0

    def add_plant_params(self, plant_type: str, moisture_target: int, n_target: int, p_target, k_target: int) -> bool:
        """Given the type of a plant <plant_type>, check if it's already registered
        in the database. If not, then add it to the database along with its ideal
        parameter values. Return True if the plant is added, else return False.
        """
        try:
            cur = self.connection.cursor()

            cur.execute(
                'SELECT * FROM IdealPlantParams WHERE plantType=%s;', [plant_type])

            if cur.rowcount > 0:
                print(
                    f"Plant type {plant_type} already registered in the database.")
                cur.close()
                return False

            cur.execute(
                'INSERT INTO IdealPlantParams VALUES (%s, %s, %s, %s, %s);', [plant_type, moisture_target, n_target, p_target, k_target])
            self.connection.commit()
            cur.close()
            return True

        except pg.Error as ex:
            # You may find it helpful to uncomment this line while debugging,
            # as it will show you all the details of the error that occurred:
            # raise ex
            return 0

    def update_plant_params(self, plant_type: str, moisture_target: int, n_target: int, p_target, k_target: int) -> bool:
        """Given the type of a plant <plant_type>, check if it's already registered
        in the database. If it is, then update its ideal parameter values.
        Return True if the plant parameters are updated, else return False.
        """
        try:
            cur = self.connection.cursor()

            cur.execute(
                'SELECT * FROM IdealPlantParams WHERE plantType=%s;', [plant_type])

            if cur.rowcount == 0:
                print(
                    f"Plant type {plant_type} not found in the database.")
                cur.close()
                return False

            cur.execute(
                'UPDATE IdealPlantParams SET moistureTarget=%s, nitrogenTarget=%s, phosphorousTarget=%s, potassiumTarget=%s WHERE plantType=%s;', [moisture_target, n_target, p_target, k_target, plant_type])
            self.connection.commit()
            cur.close()
            return True

        except pg.Error as ex:
            # You may find it helpful to uncomment this line while debugging,
            # as it will show you all the details of the error that occurred:
            # raise ex
            return 0


def setup(dbname: str, username: str, password: str, file_path: str) -> None:
    """Set up the testing environment for the database <dbname> using the
    username <username> and password <password> by importing the schema file
    and the file containing the data at <file_path>.
    """
    connection, cursor, schema_file, data_file = None, None, None, None
    try:
        # Change this to connect to your own database
        connection = pg.connect(
            dbname=dbname, user=username, password=password,
            options="-c search_path=plant_param"
        )
        cursor = connection.cursor()

        schema_file = open("./plant_param_schema.sql", "r")
        cursor.execute(schema_file.read())

        data_file = open(file_path, "r")
        cursor.execute(data_file.read())

        connection.commit()
    except Exception as ex:
        connection.rollback()
        raise Exception(f"Couldn't set up environment for tests: \n{ex}")
    finally:
        if cursor and not cursor.closed:
            cursor.close()
        if connection and not connection.closed:
            connection.close()
        if schema_file:
            schema_file.close()
        if data_file:
            data_file.close()


def test_preliminary() -> None:
    """Test preliminary aspects of the PlantParam methods."""
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

        # --------------------- Testing get_plant_params  ------------------------#
        result = pp.get_plant_params("Plant1")
        print(f"Result for get_plant_params is {result}")
        # -------------------- Testing add_plant_params  ------------------------#
        result = pp.add_plant_params("Plant4", 55, 55, 55)
        print(f"Result for add_plant_params is {result}")
        # ----------------- Testing update_plant_params  -----------------------#
        result = pp.update_plant_params("Plant1", 55, 55, 55)
        print(f"Result for update_plant_params is {result}")

    finally:
        if qf and not qf.closed:
            qf.close()
        pp.disconnect()


if __name__ == '__main__':
    # Un comment-out the next two lines if you would like to run the doctest
    # examples (see ">>>" in the methods connect and disconnect)
    # import doctest
    # doctest.testmod()

    test_preliminary()

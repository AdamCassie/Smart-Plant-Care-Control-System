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

    def get_all_plant_types(self)->list:
        """Return a list of all plant types in the database
        """

        try:
            cur = self.connection.cursor()

            result = []

            cur.execute(
                'SELECT plantType FROM IdealPlantParams;')

            if cur.rowcount == 0:
                print(f"No plants found in database.")
                cur.close()
                return result

            for row in cur:
                result.append(row[0])

            cur.close()
            return result

        except pg.Error as ex:
            # You may find it helpful to uncomment this line while debugging,
            # as it will show you all the details of the error that occurred:
            # raise ex
            return 0


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
            self.connection.rollback()
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
            self.connection.rollback()
            # You may find it helpful to uncomment this line while debugging,
            # as it will show you all the details of the error that occurred:
            # raise ex
            return 0

    def print_plant_params(self) -> None:
        """Print the contents of the database
        """
        try:
            cur = self.connection.cursor()

            cur.execute(
                'SELECT * FROM IdealPlantParams;')

            for row in cur:
                print(row)

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

        schema_file = open(file_path +  "./plant_param_schema.sql", "r")
        cursor.execute(schema_file.read())

        data_file = open(file_path + "./plant_param_data.sql", "r")
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

import sqlite3 as lite
from FileInit import FileInit


class DataBase():
    """
        This class is responsible on anything relates to the server's data base.
    """

    def __init__(self, name, user, password, host="127.0.0.1", port=3306):

        # The name of the data base.
        self.name = name

        self.user = user

        self.password = password

        self.host = host

        self.port = port

        # The data base connection handle.
        self.db = None

        # The instance which returned when connecting to the data base.
        self.connector = None

        # The cursor of the data base.
        self.cursor = None

    def connect(self, db_name):
        """
            The function connects to the data base.
        """

        # Make sure the path to the .db file exists.
        FileInit.make_dir("Records")

        # Connect the data base.
        self.connector = lite.connect("Records" + "/" + db_name + ".db")

        # Get the cursor to the data base.
        self.cursor = self.connector.cursor()

        print "Connected to the data base."

    def create_table(self, table_name, columns):
        """
            The function creates new table in the data base. In addition, it inserts the columns and their types to the
            table. columns is as follow: [[column_name, type]...]
        """

        # If the table already exist, delete it.
        self.cursor.execute("DROP TABLE IF EXISTS " + table_name)

        self.cursor.execute("CREATE TABLE " + table_name + "(" +
                            ', '.join(rubric[0] + " " + rubric[1] for rubric in columns) + ")")

    def insert(self, table_name, values):
        """
            The function receives a name of a table, and a list of the values of the new row by the order of the columns
            in the table.
        """

        self.cursor.execute("INSERT INTO " + table_name + " VALUES(" + ", ".join(value for value in values) + ")")

    def remove(self, table_name, condition):
        """
            The function removes rows from the received table according to the condition.
        """

        pass
import MySQLdb

class DBAdapter:
    """
    Adapter class for MySQL Database.

    Attributes:
        connection: connection object represents the database
        cursor: cursor object has methods to perform SQL commands:

    """
    def __init__( self ):
        self.connection = None
        self.cursor = None

    def connect( self, host_name, port_number, user_name, password, database_name ):
        # Execute an SQL statement
        self.connection = MySQLdb.connect( host=host_name, port=port_number, user=user_name, passwd=password, db=database_name)
        self.cursor = self.connection.cursor()
        print "db connection open --"
        
    def execute( self, sql ):
        # Execute an SQL statement.
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()

    def select_one_row( self, sql ):
        # Retrieve a single matching row.
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def close( self ):
        # Close database connection.
        self.cursor.close()
        self.connection.close()
        print "db connection close --"

    def get_result( self ):
        # Get a list of the matching rows.
        return self.cursor.fetchall()

if __name__ == "__main__":
    obj = DBAdapter()
    obj.connect()


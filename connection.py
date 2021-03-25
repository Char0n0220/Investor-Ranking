import psycopg2
import pandas as pd

class Connection():
    """Object holding data for database connections and connection string."""

    def __init__(self, host_name, data_base, user_name, password):
        """Initialize from environment variables."""
        self.hostname = host_name
        self.database = data_base
        self.username = user_name
        self.password = password


        # self.hostname = util_env.getenv('DB_HOSTNAME')
        # self.database = util_env.getenv('DB_DATABASE')
        # self.username = util_env.getenv('DB_USERNAME')
        # self.password = util_env.getenv('DB_PASSWORD')

    def connect(self):
        """Connect psycopg2 using instance variables."""
        self.connection = psycopg2.connect(self._get_connection_string())

    def close(self):
        """Close the instance psycopg2 connection object."""
        self.connection.close()

    def read_sql(self, query):
        """
        Wrap pandas.read_sql with a reconnect function in case db connection
        disconnects for some reason.
        """
        try:
            result = pd.read_sql(query, self.connection)
        except:
            self.reconnect()
            result = pd.read_sql(query, self.connection)
        return result

    def reconnect(self):
        """Close connection and create a new connection"""
        print("Reconnecting to database")
        self.connection.close()
        self.connection = psycopg2.connect(self._get_connection_string())

    def _get_connection_string(self):
        """Generate psycopg2 connection string, used by connect function."""
        connection_string = f"dbname='{self.database}' user='{self.username}'" \
                            f" host='{self.hostname}' password='{self.password}'"
        return connection_string

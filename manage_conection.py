
import psycopg2

class postgresController():

    def __init__(self, db_config):
        self.user = db_config["user"]
        self.password = db_config["password"]
        self.host = db_config["host"]
        self.port = db_config["port"]
        self.database = db_config["database"]
        self.conection = self.create_conection()
        self.cursor = self.create_cursor()

    def create_conection(self):
        return psycopg2.connect(
                                user = self.user,
                                password = self.password,
                                host = self.host,
                                port = self.port,
                                database = self.database,
        )

    def create_cursor(self):
        return self.conection.cursor()

    def close_manager(self):
        self.cursor.close()
        self.conection.close()

    def get_instance(self):
        return self.cursor, self.conection

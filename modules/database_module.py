#######################################################################
## Este módulo se encarga de la comunicacion con base de datos       ##
#######################################################################

# Importamos conector SQL
import mysql.connector
from mysql.connector import Error
import json

# Definicion del objeto
class DatabaseModule:
    # Atributos de configuracion
    database = 'melissa_smart_home'
    server = '127.0.0.1'
    user = 'root'
    password = ''
    # Instancias MySQL
    connection = None

    # Constructor
    def __init__(self):
        # Conectamos con base de datos
        self.connect()
    # Destructor
    def __del__(self):
        print("Finished connection")
        # Quitamos la conexion con base de datos al acabar
        self.connection.close()

    # Método que conecta con base de datos
    def connect(self):
        print("Starting connection")
        # Conectamos con base de datos
        self.connection = mysql.connector.connect(
            host=self.server,
            user=self.user,
            password=self.password,
            database=self.database
        )

    # Método para ejecutar querys de update / delete / create
    def execute_query(self, query):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query successful")
            cursor.close()
        except Error as err:
            print(f"Error: '{err}'")

    # Metodo para querys de lectura
    def read_query(self, query):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return json.dumps(results)
            cursor.close()
        except Error as err:
            print(f"Error: '{err}'")

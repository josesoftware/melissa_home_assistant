#######################################################################
## Este módulo se encarga de la comunicacion con base de datos       ##
#######################################################################

## Importamos conector SQL
import mysql.connector as MariaDB

## Definicion del objeto
class Database_Module:
    ## Atributos de configuracion
    Database = 'melissa_smart_home'
    Server = 'localhost'
    User = 'melissa'
    Password = 'melissa'

    ## Instancias MySQL
    Connection = None

    ## Constructor
    def __init__(self):
        ## Conectamos con base de datos
        self.Connect()
    
    ## Método que conecta con base de datos
    def Connect(self):
        ## Conectamos con base de datos
        self.Connection = MariaDB.connect(
            host = self.Server,
            user = self.User,
            password = self.Password,
            database = self.Database
        )
#######################################################################
## Este módulo se encarga de la comunicacion con base de datos       ##
#######################################################################

# Importamos conector SQL
from modules.database_module import DatabaseModule

p1 = DatabaseModule()
print(p1.read_query("select * from melissa_command;"))

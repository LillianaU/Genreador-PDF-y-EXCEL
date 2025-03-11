# Importa el módulo pymysql, que es un conector de MySQL para Python.ódulo pymysql, que es un conector de MySQL para Python.
import pymysql






pymysql.install_as_MySQLdb()# puede ser utilizado como un reemplazo compatible.# Esto es necesario porque Django espera usar MySQLdb, pero pymysql# Configura pymysql para que se utilice como el conector MySQLdb.# Configura pymysql para que se utilice como el conector MySQLdb.
# Esto es necesario porque Django espera usar MySQLdb, pero pymysql
# puede ser utilizado como un reemplazo compatible.
pymysql.install_as_MySQLdb()

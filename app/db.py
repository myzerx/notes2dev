from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Lab2dev@2022'
app.config['MYSQL_DATABASE_DB'] = 'notes2dev'
app.config['MYSQL_DATABASE_HOST'] = 'db'
mysql.init_app(app)

import pymysql
import json
from app import app
from db import mysql
from flask import jsonify, Response, request

class create_dict(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

@app.route('/api/get/colaboradores', methods=['GET'])
def getColaborador():
    try:
        connection = mysql.connect()
        if connection.open:
            select_employee = """SELECT * FROM colaborador"""
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(select_employee)
            rows = cursor.fetchall()
            result = jsonify(rows)
            result.status_code = 200
    
            return result
        else:
            print("Error while connecting to MySQL")
    finally:
        if connection.open:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/api/get/dashboard', methods=['GET'])
def getDashboard():
    try:
        connection = mysql.connect()
        if connection.open:
            select_dashboard = """SELECT 
                                colaborador.nome as nome, 
                                colaborador.email as email, 
                                count(nota.nota) as notas, 
                                count(notapos.nota) as notaspos, 
                                count(notaneg.nota) as notasneg, 
                                ifnull(DATE_FORMAT((select data from nota where colaborador = colaborador.email  order by data desc limit 1),'%d %b %y %h:%i'),'') as ultimanota,
                                CASE WHEN DATE((select data from nota where colaborador = colaborador.email  order by data desc limit 1) + INTERVAL 15 DAY) > NOW()
                                THEN
                                    'ATUALIZADO'
                                ELSE
                                    'ATRASADO'
                                END as status
                            FROM colaborador
                            LEFT JOIN nota
                            on nota.colaborador = colaborador.email
                            LEFT JOIN nota as notapos
                            on notapos.colaborador = colaborador.email
                            and notapos.tipo = '2'
                            LEFT JOIN nota as notaneg
                            on notaneg.colaborador = colaborador.email
                            and notaneg.tipo = '1'
                            group by colaborador.nome, colaborador.email"""
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(select_dashboard)           
            rows = cursor.fetchall()
            result = jsonify(rows)
            result.status_code = 200
    
            return result
        else:
            print("Error while connecting to MySQL")
    finally:
        if connection.open:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/api/get/tipo_nota', methods=['GET'])
def getTipoNota():  
    try:
        connection = mysql.connect()
        if connection.open:
            select_employee = """SELECT * FROM tipo_nota"""
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(select_employee)
            rows = cursor.fetchall()
            result = jsonify(rows)
            result.status_code = 200
    
            return result
        else:
            print("Error while connecting to MySQL")
    finally:
        if connection.open:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/api/get/nota', methods=['GET'])
def getNota(colab=False):
    try:
        connection = mysql.connect()
        if connection.open:
            select_employee = """SELECT * FROM nota """
            if colab != False:
                select_employee += f""" WHERE colaborador = '{colab}'"""
            select_employee += """ORDER BY data DESC """
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(select_employee)
            rows = cursor.fetchall()
            result = jsonify(rows)
            result.status_code = 200
    
            return result
        else:
            print("Error while connecting to MySQL")
    finally:
        if connection.open:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def getLogin(email, pasw):
    try:
        connection = mysql.connect()
        if connection.open:
            select_login = f"""SELECT * FROM login 
               WHERE email = '{email}' and senha = '{pasw}'"""
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(select_login)
            row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rows = cursor.fetchall()
            result = jsonify(rows)
            result.status_code = 200
            json_data=[]
            for result in rows:
                    json_data.append(dict(zip(row_headers,result)))
            return json.dumps(json_data, indent=4, sort_keys=True, default=str)
            
        else:
            print("Error while connecting to MySQL")
    finally:
        if connection.open:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def addNota(jObj):
    try:
        connection = mysql.connect()
        if connection.open:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                """INSERT INTO `nota`
                    (`data`,
                    `nota`,
                    `tipo`,
                    `colaborador`)
                    VALUES
                    (NOW(),
                    %s,
                    %s,
                    %s);""", (jObj['nota'], jObj['tipo'], jObj['colaborador']))
            connection.commit()
            rows = cursor.fetchall()
            result = jsonify(rows)
            result.status_code = 200
            return str(cursor.rowcount) + " record inserted."
    
        
        else:
            print("Error while connecting to MySQL")
    finally:
        if connection.open:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/api/add/nota/', methods=['POST','OPTIONS'])
def apiAddNota():
    try:
        jRequest = request.get_json()
        resp = Response(addNota(jRequest),status=200, mimetype="application/json")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
       return(str(e))

@app.route('/api/get/login', methods=['GET'])
def apiGetLogin():
    try:
        user,pasw = False, False
        if request.args.get('$email') and request.args.get('$pasw'):
            user = request.args.get('$email')
            pasw = request.args.get('$pasw')
            content = getLogin(user,pasw)
            print(content)
            return  Response(content,status=200, mimetype="application/json")
        else: 
            return  Response("NAO AUTORIZADO",status=401, mimetype="application/json")
    except Exception as e:
       return(str(e))
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

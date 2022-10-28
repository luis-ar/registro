from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
app=Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS']='Content-Type'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='system'
mysql=MySQL(app)

@app.route('/customers')
@cross_origin()
def getAllCustomer():
    cur=mysql.connection.cursor()
    cur.execute('SELECT id,firstname,lastname,email,phone,address FROM customers')
    data=cur.fetchall()
    result=[]
    for row in data:
        content ={'id':row[0], 'firstname':row[1], 'lastname':row[2], 'email':row[3], 'phone':row[4], 'address':row[5]}
        result.append(content)
    return jsonify(result)

@app.route('/customers/<int:id>')
@cross_origin()
def getCustomer(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT id,firstname,lastname,email,phone,address FROM customers WHERE id='+str(id))
    data=cur.fetchall()
    content={}
    for row in data:
        content ={'id':row[0], 'firstname':row[1], 'lastname':row[2], 'email':row[3], 'phone':row[4], 'address':row[5]}
    return jsonify(content)


@app.route('/customers', methods=['POST'])
@cross_origin()
def createCustomers():#repite
    if 'id' in request.json:
        updateCustomer()
    else:
        createCustomer()
    return "ok"


def createCustomer():
    cur= mysql.connection.cursor()
    cur.execute("INSERT INTO `customers` (`id`, `firstname`, `lastname`, `email`, `phone`, `address`) VALUES (NULL, %s, %s, %s, %s, %s);",
                (request.json['firstname'],request.json['lastname'],request.json['email'],request.json['phone'],request.json['address']))
    mysql.connection.commit()
    return "Cliente guardado"


@app.route('/customers', methods=['PUT'])
@cross_origin()
def updateCustomer():
    cur= mysql.connection.cursor()
    cur.execute("UPDATE `customers` SET `firstname` = %s, `lastname` = %s, `email` = %s, `phone` = %s, `address` = %s WHERE `customers`.`id` = %s;",
                (request.json['firstname'], request.json['lastname'], request.json['email'], request.json['phone'],
                 request.json['address'], request.json['id']))
    mysql.connection.commit()
    return "Cliente guardado"



@app.route('/customers/<int:id>', methods=['DELETE'])
@cross_origin()
def removeCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE `customers`.`id` ="+str(id)+ ";")
    mysql.connection.commit()
    return "Cliente eliminado"


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/<path:path>')
@cross_origin()
def publicFiles(path):
    return render_template(path)


if __name__=='__main__':
    app.run(None, 3000, True)
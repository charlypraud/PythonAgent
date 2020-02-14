from flask import Flask, render_template,request,jsonify
import pymysql.cursors
def initConnection():
# Connect to the database
  connection = pymysql.connect(host='localhost',
                              port=3308,
                              user='root',
                              password='',
                              db='tests4',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
  return connection
app = Flask(__name__)
@app.route('/',methods=['GET'])
def getAllMachines():
  # Read a single record
  connection = initConnection()
  cursor = connection.cursor()
  sql = "SELECT hote.idHote,hote.nom from hote"
  cursor.execute(sql)
  data = cursor.fetchall()
  cursor.close()
  connection.close()
  return render_template("index.html", taille = len(data), listeMachines=data)
@app.route("/machine/<int:idMachine>/getCPUInfo",methods=['GET'])
def getCPUInfo(idMachine):
  connection = initConnection()
  cursor = connection.cursor()
  metrics = {}
  sql = "SELECT * FROM cpu where cpu.idHote="+(str(idMachine))
  cursor.execute(sql)
  metrics['cpuUsage']=cursor.fetchall()
  cursor.close()
  connection.close()        
  return jsonify(metrics)

@app.route("/machine/<int:idMachine>/getMemoryInfo",methods=['GET'])
def getMemoryInfo(idMachine):
  connection = initConnection()
  cursor = connection.cursor()
  metrics = {}
  sql = "SELECT * FROM disque where disque.idHote="+(str(idMachine)+" ORDER BY idDisque DESC LIMIT 10")
  cursor.execute(sql)  
  metrics['memoryUsage']=cursor.fetchall()
  cursor.close()
  connection.close()
  return jsonify(metrics)  

@app.route("/machine/<int:idMachine>/getDiskInfo",methods=['GET'])
def getDiskInfo(idMachine):
  connection = initConnection()
  cursor = connection.cursor()
  metrics = {}  
  sql = "SELECT * FROM typepartition inner join disque on disque.idDisque=typepartition.idDisque where disque.idHote="+(str(idMachine)+" ORDER BY typepartition.idDisque DESC LIMIT 10")
  cursor.execute(sql)
  metrics['diskUsage']=cursor.fetchall()
  cursor.close()
  connection.close()
  return jsonify(metrics)

@app.route("/machine/<int:idMachine>/hostInfo",methods=['GET'])
def getHostInfo(idMachine):
  connection = initConnection()
  cursor = connection.cursor()  
  sql = "SELECT * FROM hote where hote.idHote="+(str(idMachine))
  cursor.execute(sql)
  metrics=cursor.fetchone()
  cursor.close()
  connection.close()
  return jsonify(metrics)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

import flask
from flask import request
import json
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import mysql.connector
import sys

with open("config.conf","r") as fichier:
    ip = fichier.read()

app = flask.Flask(__name__)
app.config['DEBUG'] = True

conn = mysql.connector.connect(host="localhost",user="tests4",password="4NqGjgkZ", database="tests4")
cursor = conn.cursor()

# création de l'objet logger qui va nous servir à écrire dans les logs
loggerClient = logging.getLogger()
loggerClient.setLevel(logging.DEBUG)

# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('./logs/clients.log', 'a', 1000000, 1)        
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
loggerClient.addHandler(file_handler)


@app.route('/api', methods=['POST'])
def home():
    # some JSON:
    x = request.data
    try:
        y = json.loads(x)
        sql = "SELECT idHote from hote where idHote=%s"
        val = (y['id'],)        
        
        cursor.execute(sql,val)
        rows = cursor.fetchall()
        if not rows:     
            loggerClient.error("L'hote n'existe pas")   
            return json.dumps({'error':"ERREUR : L'hote n'existe pas"})
        else:
            sql = """UPDATE hote SET nom=%s, OS=%s, uptime=%s, noyaux=%s WHERE idHote=%s"""
            val = (y['nomhost'],y['os'],y['uptime'],y['noyau'],y['id'])
            cursor.execute(sql, val)
            conn.commit()
            
            sql = """INSERT INTO cpu(idHote, frequence,frequenceMax, type) VALUES (%s, %s, %s, %s)"""
            val = (y['id'],y['cpufrequence'],y['cpufrequencemax'],y['cputype'])
            cursor.execute(sql, val)
            conn.commit()
            cpuId = cursor.lastrowid
    
            sql = """INSERT INTO disque(idHote,memoireTotal,memoireLibre,memoireOccupe,buffer,cache) VALUES (%s,%s,%s,%s,%s,%s)"""
            val = (y['id'],y['total'],y['mlibre'],y['moccupe'],y['mbuffer'],y['mcached'])
            cursor.execute(sql, val)
            conn.commit()
            partitionId = cursor.lastrowid
            for partition in y['metrique']:
                sql = """INSERT INTO typepartition(idDisque,available,fileSystem,mounted,pourcentage,size,used) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                val = (partitionId,partition['available'],partition['fileSystem'],partition['mounted'],partition['pourcentage'],partition['size'],partition['used'])
                cursor.execute(sql, val)
                conn.commit()
            
            for service in y['service']:
                sql = """SELECT nom FROM service WHERE nom=%s"""
                val = (service['name'],)
                cursor.execute(sql, val)
                rows = cursor.fetchall()
                if not rows:
                    sql = """INSERT INTO service(nom) VALUES (%s)"""
                    val = (service['name'],)
                    cursor.execute(sql, val)
                    conn.commit()
                    print("4 insert")
                    if service['etat'].lower() == "true":
                        etat = 1
                    else:
                        etat = 0
                    sql = """INSERT INTO servicehote(idHote,idService,etat) VALUES (%s,%s,%s)"""
                    val = (y['id'],cursor.lastrowid,etat)
                    cursor.execute(sql, val)
                    conn.commit()
    
            return y
        
        
    except (RuntimeError, TypeError, NameError, ValueError) as error:       
        loggerServeur = logging.getLogger()
        loggerServeur.setLevel(logging.DEBUG)
        formatterServeur = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handlerServeur = RotatingFileHandler('./logs/serveur.log', 'a', 1000000, 1)        
        file_handlerServeur.setLevel(logging.DEBUG)
        file_handlerServeur.setFormatter(formatterServeur)
        loggerServeur.addHandler(file_handlerServeur)
        loggerServeur.error(error)

@app.route('/api/init', methods=['POST'])
def init():  
    x = request.data
    try:
        y = json.loads(x)
        sql = """SELECT nom from hote where nom=%s"""
        val = (y['nom'],)
        cursor.execute(sql,val)
        rows = cursor.fetchall()
        try:
            if not rows:        
                sql = """INSERT INTO hote(nom, OS, uptime, noyaux) VALUES (%s,%s,"","")"""
                val = (y['nom'],y['os'])
                cursor.execute(sql,val)
                conn.commit()
                id = cursor.lastrowid
        
                sql = """SELECT nom from hote where nom=%s"""
                val = (y['nom'],)
                cursor.execute(sql,val)
                rows = cursor.fetchall()
            else:
                sql = """SELECT idHote from hote where nom=%s"""
                val = (y['nom'],)
                cursor.execute(sql,val)
                id = cursor.fetchall()
            for i in id:
                idStr = i
            if y['os'] == "Linux":
                return json.dumps({"id":idStr[0], "services":[{"name":"bluetooth"},{"name":"cron"},{"name":"alsa-store"}]})
            else:
                return json.dumps({"id":idStr[0], "services":[{"name":"cmd.exe"},{"name":"mpssvc"},{"name":"WSearch"}]})           
        except:
            loggerClient.error("Mauvaises données")  
    except:
        loggerClient.error("Aucune données envoyées")





from flask import Flask, render_template,request,jsonify
import pymysql.cursors
def initConnection():
# Connect to the database
  connection = pymysql.connect(host='localhost',
                              
                              user='tests4',
                              password='4NqGjgkZ',
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








app.run(host = ip)




#!/usr/bin/python
# -*- coding: utf8 -*-

import MySQLdb


def iniciodb():
  global db
  import ConfigParser
  config = ConfigParser.RawConfigParser()
  config.read('config.cfg')
  varUser = config.get('mysql', 'user')
  varPass = config.get('mysql', 'pass')
  varDBName = config.get('mysql', 'dbname')
  varHost = config.get('mysql', 'hostname')
  db = MySQLdb.connect(host=varHost,user=varUser,passwd=varPass,db=varDBName)
  global cur
  cur = db.cursor() 


iniciodb()
cur.execute('SELECT name, owner FROM pet')
#for row in cur.fetchall():
  #print row
#cur.execute("SET NAMES 'utf8'")			# Esto en principio solo habría que ejecutarlo al crear la tabla
#cur.execute("SET character_set_client = utf8")
cur.execute("SET CHARACTER SET utf8")
name = "Jesús"
owner = "paquete"
species = "pájaro"
sex = "m"
birth = "1949-05-24"
death = ""

querry2 = "INSERT INTO pet VALUES (%s, %s, %s, %s, %s, %s)" 
cur.execute(querry2,(name,owner,species,sex,birth,'NULL'))

#db.commit()			# Esta linea es fundamental porque es la que ordena la escritura de los cambios.
cur.execute('SELECT * FROM pet')
for row in cur.fetchall():
  #row2[range(len(row))]
  row=list(row)
  #for i in (range(len(row)-2)):
    #row[i]=row[i].decode('utf8','ignore')
  k=0
  row[k]=row[k].decode('utf8','ignore')
  print row[k]
  print row[4]
  print row

#import time
#time.sleep(50)
cur.close()
db.close()
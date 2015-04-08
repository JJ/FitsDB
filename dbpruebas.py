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
  
name = "Joselito"
owner = "pacote"
species = "perico"
sex = "m"
birth = "1949-05-24"
death = ""

querry2 = "INSERT INTO pet VALUES (%s, %s, %s, %s, %s, %s)" 
cur.execute(querry2,(name,owner,species,sex,birth,'NULL'))

db.commit()
cur.execute('SELECT * FROM pet')
for row in cur.fetchall():
  print row

#import time
#time.sleep(50)
cur.close()
db.close()
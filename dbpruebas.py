#!/usr/bin/python
# -*- coding: utf8 -*-

import MySQLdb


def iniciodb():
  global db
  db = MySQLdb.connect(host="localhost",user="pablo",passwd="halconmilenario",db="pruebasdb")
  global cur
  cur = db.cursor() 


iniciodb()
cur.execute('SELECT name, owner FROM pet')
#for row in cur.fetchall():
  #print row
  
name = "bobete"
owner = "paco"
species = "perico"
sex = "m"
birth = "1999-05-24"
death = ""
querry = 'INSERT INTO pet VALUES (\'' + name + '\',\'' + owner + '\',\'' + species + '\',\'' + sex + '\',\'' + birth + '\',NULL);'
print querry
#cur.execute(querry)

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
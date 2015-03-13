#!/usr/bin/python
# -*- coding: utf8 -*-
import csv
with open('prueba.csv','w') as csvfile:
  fieldnames = ['nombre','apellidos','uno','dos','tres']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerow({'nombre':'pepe','uno':'aquel','tres':'nose'})
  writer.writerow({'nombre':'papo','apellidos':'jeremias','tres':'ytuque'})
  writer.writerow({'nombre':'jaime','dos':'aquelarre','apellidos':'nosesabe nada mas'})
csvfile.close()
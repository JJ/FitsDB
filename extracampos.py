#!/usr/bin/python
# -*- coding: utf8 -*-
# Extracción de campos de archivos fits
import os, pyfits
from os import listdir, walk

def add(url, salida):
  listaDatos = pyfits.open(url)
  listaCamposNuevos = listaDatos[0].header.keys()
  fileCampos = open(salida, 'r')
  listaCampos = fileCampos.read().splitlines()
  for strCampoNuevo in listaCamposNuevos:
    if strCampoNuevo not in (s.rstrip(' ') for s in listaCampos):
      fileCampos = open(salida, 'a')
      fileCampos.write(strCampoNuevo + ' \n')
      fileCampos.close()

def sort(file):
  f = open(file, 'r')
  mano = f.readlines()
  mano.sort()
  f.close()
  f = open(file, 'w')
  f.writelines(mano)
  f.close()

import hashlib
def hashfile(ruta):
  BLOCKSIZE = 65536
  hasher = hashlib.md5()
  with open(ruta, 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
	  hasher.update(buf)
	  buf = afile.read(BLOCKSIZE)
  print(hasher.hexdigest())

# SIN TERMINAR
#def genCsvWithHeaders(sitio, name):
  #url = sitio + "/" + name
  #listaDatos = pyfits.open(url)
  #salida = "salida.csv"
  ## Vendría bien comprobar si existe y tal
  #f = open('salida.csv','w')
  #for campo in listaDatos[0].header.keys():
    #print listaDatos[0].header[campo]


directorio_imagenes = "ImagenesPrueba"
archivo_nombres_campos = "nombres_de_campos"
j = 0
for (path, ficheros, archivos) in walk (directorio_imagenes):
  for file in archivos:
    if file.endswith(".fits") or file.endswith(".fit") or file.endswith(".fts"):
      ruta = path + '/' + file
      add(ruta, archivo_nombres_campos)
      #hashfile(ruta)
      j += 1
sort(archivo_nombres_campos)
print "Procesados " + str(j) + " archivos."


#import sys
#total = len(sys.argv)
 
## Get the arguments list 
#cmdargs = str(sys.argv)
 
## Print it
#print ("The total numbers of args passed to the script: %d " % total)
#print ("Args list: %s " % cmdargs)
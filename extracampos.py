#!/usr/bin/python
# -*- coding: utf8 -*-
# Extracción de campos de archivos fits
import os, pyfits, sys
from os import listdir, walk


def CheckFileExistence(nombrearchivo):
  if os.path.exists(nombrearchivo):
    return 1
  elif not os.path.exists(nombrearchivo):
    file(nombrearchivo, 'w').close()
    return 0


def Add(url, salida):
  listaDatos = pyfits.open(url)
  listaCamposNuevos = listaDatos[0].header.keys()
  if CheckFileExistence(salida):
    fileCampos = open(salida, 'r')
    listaCampos = fileCampos.read().splitlines()
    for strCampoNuevo in listaCamposNuevos:
      if strCampoNuevo not in (s.rstrip(' ') for s in listaCampos):
	fileCampos = open(salida, 'a')
	fileCampos.write(strCampoNuevo + ' \n')
  else:
    for strCampoNuevo in listaCamposNuevos:
      fileCampos = open(salida, 'a')
      fileCampos.write(strCampoNuevo + ' \n')
  fileCampos.close()


def Sort(archivo):
  f = open(archivo, 'r')
  mano = f.readlines()
  mano.sort()
  f.close()
  f = open(archivo, 'w')
  f.writelines(mano)
  f.close()


import hashlib
def HashFile(ruta):
  BLOCKSIZE = 65536
  hasher = hashlib.md5()
  with open(ruta, 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
	  hasher.update(buf)
	  buf = afile.read(BLOCKSIZE)
  print(hasher.hexdigest())


# SIN TERMINAR
#def GenCsvWithHeaders(sitio, name):
  #url = sitio + "/" + name
  #listaDatos = pyfits.open(url)
  #salida = "salida.csv"
  ## Vendría bien comprobar si existe y tal
  #f = open('salida.csv','w')
  #for campo in listaDatos[0].header.keys():
    #print listaDatos[0].header[campo]


if len(sys.argv) == 2:
  directorio_imagenes = sys.argv[1]
elif len(sys.argv) > 2:
  from termcolor import colored
  print colored ("¡ERROR!", "red")
  print "Solo se admite un único argumento: un directorio que contenga las imagenes"
  print "del tipo .fits, .fit y/o .fts"
  print " "
  print "A continuación se muestra un ejemplo:"
  print " "
  print "$ ./extracampos.py rutaamidirectorio/"
  print " "
  print "Donde \"rutaamidirectorio/\" es la ruta desde donde se está ejecutando este"
  print "programa hasta donde se encuentran las imágenes del tipo .fits, .fit y/o .fts"
  print " "
  print "Vuelva a intentarlo, por favor."
  print " "
  sys.exit()
elif len(sys.argv) == 1:
  from termcolor import colored
  print colored ("¡ERROR!", "red")
  print "Para que el programa funcione correctamente tiene que añadirle un argumento."
  print "A continuación se muestra un ejemplo:"
  print " "
  print "$ ./extracampos.py rutaamidirectorio/"
  print " "
  print "Donde \"rutaamidirectorio/\" es la ruta desde donde se está ejecutando este"
  print "programa hasta donde se encuentran las imágenes del tipo .fits, .fit y/o .fts"
  print " "
  print "Vuelva a intentarlo, por favor."
  print " "
  sys.exit()

archivo_nombres_campos = "nombres_de_campos"
j = 0
for (path, ficheros, archivos) in walk (directorio_imagenes):
  for file in archivos:
    if file.endswith(".fits") or file.endswith(".fit") or file.endswith(".fts"):
      ruta = path + '/' + file
      Add(ruta, archivo_nombres_campos)
      #HashFile(ruta)
      j += 1
Sort(archivo_nombres_campos)
print colored ("Se han procesados " + str(j) + " archivos.", "green")


#!/usr/bin/python
# -*- coding: utf8 -*-
# Extracción de campos de archivos fits
import os, pyfits
from os import listdir, walk

def add(url):
  #print url
  listaDatos = pyfits.open(url)
  listaCamposNuevos = listaDatos[0].header.keys()
  fileCampos = open('nombres_de_campos', 'r')
  listaCampos = fileCampos.read().splitlines()
  for strCampoNuevo in listaCamposNuevos:
    n = 0
    for strFileCampos in listaCampos:
      print strFileCampos + " -> " + strCampoNuevo
      if strCampoNuevo == strFileCampos:
	n += 1
	print "sumando"
      #else:
	#n += 0 
	#print "no hacemos nada"
    if n == 0:
      fileCampos = open('nombres_de_campos', 'a')
      fileCampos.write(strCampoNuevo + ' \n')
      fileCampos.close()


# Lista los archivos del directorio de ejecución y los almacena en el array aArchivos
directorio_imagenes = "ImagenesPrueba"
for (path, ficheros, archivos) in walk (directorio_imagenes):
  for file in archivos:
    if file.endswith(".fits") or file.endswith(".fit") or file.endswith(".fts"):
      ruta = path + '/' + file
      add(ruta)
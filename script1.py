#!/usr/bin/python
# -*- coding: utf8 -*-
# Extracción de campos de archivos fits
import os, pyfits
from os import listdir, walk

def add(url):
  #print url
  listaDatos = pyfits.open(url)
  campos = listaDatos[0].header.keys()
  archivocampos = open('nombres_de_campos', 'r')
  listCampos = archivocampos.read()
  for campo in campos:
    #print campos
    for campo_archivo in listCampos:
      n = 0
      if campo == campo_archivo:
	n += 1
      else:
	n += 0 
    if n == 0:
      archivocampos = open('nombres_de_campos', 'a')
      archivocampos.write(campo + '\n')
      archivocampos.close()
	
	


# Lista los archivos del directorio de ejecución y los almacena en el array aArchivos
directorio_imagenes = "ImagenesPrueba"
for (path, ficheros, archivos) in walk (directorio_imagenes):
  for file in archivos:
    if file.endswith(".fits") or file.endswith(".fit") or file.endswith(".fts"):
      ruta = path + '/' + file
      add(ruta)
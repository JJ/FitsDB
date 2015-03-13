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

def ordena(file):
  f = open(file, 'r')
  mano = f.readlines()
  mano.sort()
  f.close()
  f = open(file, 'w')
  f.writelines(mano)
  f.close()


directorio_imagenes = "ImagenesPrueba"
archivo_nombres_campos = "nombres_de_campos"
j = 0
for (path, ficheros, archivos) in walk (directorio_imagenes):
  for file in archivos:
    if file.endswith(".fits") or file.endswith(".fit") or file.endswith(".fts"):
      ruta = path + '/' + file
      add(ruta, archivo_nombres_campos)
      j += 1
ordena(archivo_nombres_campos)
print "Procesados " + str(j) + " archivos."
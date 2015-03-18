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


def AddCampos(url, salida):
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
  listaDatos.close()


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
  #CheckFileExistence(salida)
  #f = open('salida.csv','w')
  #for campo in listaDatos[0].header.keys():
    #print listaDatos[0].header[campo]

def JD2Date(entrada):
  from astropy.time import Time
  dato = float(entrada)
  dia = int(dato)
  inst = dato - dia
  t = Time(dia, inst, format='jd')
  return t.iso


def MJD2Date(entrada):
  from astropy.time import Time
  dato = float(entrada)
  dia = int(dato)
  inst = dato - dia
  t = Time(dia, inst, format='mjd')
  return t.iso


def BuscaTiempo(fuente,listaCampos): # Sin acabar
  if "DATE-AVG"  in (s.rstrip(' ') for s in listaCampos):
    print "Fecha media -> \t" + str(fuente[0].header["DATE-AVG"])
  elif "DATE" in (s.rstrip(' ') for s in listaCampos):
    print "Fecha -> \t" + str(fuente[0].header["DATE"])
    if "T" in str(fuente[0].header["DATE"]):
      print "\t\t\t" + str(fuente[0].header["DATE"]).split("T")[0]+ "\t" + str(fuente[0].header["DATE"]).split("T")[1]
    elif "-" in str(fuente[0].header["DATE"]):
      print "\t\t\t" + str(fuente[0].header["DATE"]).replace("-","/")
  elif "DATE-OBS" in (s.rstrip(' ') for s in listaCampos):
    print "Fecha obs -> \t" + str(fuente[0].header["DATE-OBS"]) 
  elif "DATE_OBS" in (s.rstrip(' ') for s in listaCampos):
    print "Fecha obs_ -> \t" + str(fuente[0].header["DATE_OBS"]) 
    
  elif "JD" in (s.rstrip(' ') for s in listaCampos):
    print "Fecha juliana -> \t" + str(fuente[0].header["JD"])
  elif "JUL-DATE" in (s.rstrip(' ') for s in listaCampos):
    print "Fecha juliana -> \t" + str(fuente[0].header["JUL-DATE"])
  elif "JUL_DATE" in (s.rstrip(' ') for s in listaCampos):
    print "Fecha juliana -> \t" + str(fuente[0].header["JUL_DATE"])
  elif "JD-HELIO" in (s.rstrip(' ') for s in listaCampos):
    print "fecha juliana heliocen. -> \t" + str(fuente[0].header["JD-HELIO"])
  elif "JD_HELIO" in (s.rstrip(' ') for s in listaCampos):
    print "fecha juliana heliocen. -> \t" + str(fuente[0].header["JD_HELIO"])
  elif "SID-TIME" in (s.rstrip(' ') for s in listaCampos):
    print "tiempo sideral -> \t" + str(fuente[0].header["SID-TIME"])
  elif "SID_TIME" in (s.rstrip(' ') for s in listaCampos):
    print "tiempo sideral -> \t" + str(fuente[0].header["SID_TIME"])
  elif "MJD" in (s.rstrip(' ') for s in listaCampos):
    print "fecha juliana mod -> \t" + str(fuente[0].header["MJD"])
  elif "MJD-OBS" in (s.rstrip(' ') for s in listaCampos):
    print "fecha juliana mod -> " + str(fuente[0].header["MJD-OBS"])
  elif "MNT_INFO" in (s.rstrip(' ') for s in listaCampos):
    print "mnt_info"
  elif "OPENTIME" in (s.rstrip(' ') for s in listaCampos):
    print "instante apertura obturador"
  elif "READTIME" in (s.rstrip(' ') for s in listaCampos):
    print "tiempod de lectura"
  elif "ST" or "STSTART" in (s.rstrip(' ') for s in listaCampos):
    print "tiempo inicio exp \t" + ruta
  elif "TIME" in (s.rstrip(' ') for s in listaCampos):
    print "instante en el que empieza algo"
  elif "TIME-END" or "TIME_END" in (s.rstrip(' ') for s in listaCampos):
    print "instante en el que termina la última adquisición"
  elif "TM_START" or "TM-START" in (s.rstrip(' ') for s in listaCampos):
    print "instante de inicio indet"
  elif "UNI-TIME" or "UNI_TIME" in (s.rstrip(' ') for s in listaCampos):
    print "tiempo universal, ahí es nada"
  elif "USEC" in (s.rstrip(' ') for s in listaCampos):
    print "tiempo de exposición"
  elif "UT" in (s.rstrip(' ') for s in listaCampos):
    print "inicio de algo, lo que sea"
  elif "UTC" in (s.rstrip(' ') for s in listaCampos):
    print "inst de inicio en segundos suma"
  elif "UT_END" or "UT-END" in (s.rstrip(' ') for s in listaCampos):
    print "inst de fin en segundos suma"
  elif "UTOBS" in (s.rstrip(' ') for s in listaCampos):
    print "inst aprox de inicio"
  elif "UT_START" in (s.rstrip(' ') for s in listaCampos):
    print "inst de inicio indet de algo"
  elif "CLOSTIME" in (s.rstrip(' ') for s in listaCampos):
    print "inst de cierre del obturador"
  elif "CTIME" in (s.rstrip(' ') for s in listaCampos):
    print "inst de inicio de exposicion"
  elif "DARKTIME" in (s.rstrip(' ') for s in listaCampos):
    print "darktime. muchas cosas"
  elif "ELAPSED" in (s.rstrip(' ') for s in listaCampos):
    print "elapsed"
  elif "EXPOSED" in (s.rstrip(' ') for s in listaCampos):
    print "exposed"
  elif "EXP_ID" in (s.rstrip(' ') for s in listaCampos):
    print "exp ip"
  elif "EXPOSURE" or "EXPTIME" in (s.rstrip(' ') for s in listaCampos):
    print "exposure"
  elif "EXPSTART" in (s.rstrip(' ') for s in listaCampos):
    print "expstart"
  elif "LST" in (s.rstrip(' ') for s in listaCampos):
    print "lst"
  elif "MNT_INFO" in (s.rstrip(' ') for s in listaCampos):
    print "mnt info"
  else:
    print "No se encuentra."

def GetData(url):
  fuente = pyfits.open(url)
  listaCampos = fuente[0].header.keys()
  tiempo = BuscaTiempo(fuente, listaCampos)
  fuente.close()
  

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
      #AddCampos(ruta, archivo_nombres_campos)
      #HashFile(ruta)
      GetData(ruta)
      j += 1
Sort(archivo_nombres_campos)
msgfin = "Se han procesados " + str(j) + " archivos.", "green"
from termcolor import colored
print colored (msgfin, "green")


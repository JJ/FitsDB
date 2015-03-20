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

def FormatoFecha(cadena):
  if 'T' in cadena:
    par = cadena.split("T")
    par[0] = par[0].replace('-','/')
    par[1] = par[1].replace('-',':')
  else:
    par = [cadena.replace('-','/'),'']
  return par
 
def EstCom(comentario,buscamos):
  palabras = comentario.split(' ')
  for i in palabras:
    if i == buscamos:
      return 1
      break
  return 0



def TratamientoFecha(nomcampo,valcampo,comcampo):
  if nomcampo == "DATE-AVG":
    par = FormatoFecha(valcampo)
    print "Femed\t"+ "\t"  + par[0] + ' ' + par[1] + "\t\t\t" + comcampo
  elif nomcampo == "DATE":
    par = FormatoFecha(valcampo)
    print "Fecha\t" + "\t" + par[0] + ' ' + par[1] + "\t\t\t" + comcampo
  elif nomcampo == "DATE-OBS":
    par = FormatoFecha(valcampo)
    print "Feobs\t" + "\t" + par[0] + ' ' + par[1] + "\t\t\t" + comcampo
  elif nomcampo == "DATE_OBS":
    par = FormatoFecha(valcampo)
    print "Feobs_\t" +"\t" + par[0] + ' ' + par[1] + "\t\t\t" + comcampo
  elif nomcampo == "JD":
    print "Fejul\t" + "\t" + JD2Date(str(valcampo)) + "\t\t\t" + comcampo
  elif nomcampo == "JUL-DATE":
    print "Fejul\t" + "\t" + JD2Date(str(valcampo)) + "\t\t\t" + comcampo
  elif nomcampo == "JUL_DATE":
    print "Fejul\t" + "\t" + JD2Date(str(valcampo)) + "\t\t\t" + comcampo
  elif nomcampo == "JD-HELIO":
    print "FeHel\t" + "\t" + str(valcampo) + "\t\t\t" + comcampo
  elif nomcampo == "JD_HELIO":
    print "FeHel\t" + "\t" + str(valcampo) + "\t\t\t" + comcampo
    
    
  #elif nomcampo == "SID-TIME":
    #print "tiempo sideral\t" + "\t" + str(valcampo) + "\t\t" + comcampo
  #elif nomcampo == "SID_TIME":
    #print "tiempo sideral\t" + str(valcampo) + "\t\t" + comcampo
  #elif nomcampo == "MJD":
    #print "fecha juliana mod\t" + str(valcampo) + '\t' + MJD2Date(str(valcampo)) + "\t\t\t" + comcampo
  #elif nomcampo == "MJD-OBS":
    #print "fecha juliana mod" + str(valcampo) + '\t' + MJD2Date(str(valcampo)) + "\t\t\t" + comcampo
  #elif nomcampo == "MNT_INFO":
    #print "mnt_info"
  #elif nomcampo == "OPENTIME":
    #print "instante apertura obturador"
  #elif nomcampo == "READTIME":
    #print "tiempod de lectura"
  #elif nomcampo == "STSTART":
    #print "tiempo inicio exp \t" + ruta
  #elif nomcampo == "ST":
    #print "tiempo inicio exp \t" + ruta
  #elif nomcampo == "TIME":
    #print "instante en el que empieza algo"
  #elif nomcampo == "TIME-END":
    #print "instante en el que termina la última adqu==ición"
  #elif nomcampo == "TM-START":
    #print "instante de inicio indet"
  #elif nomcampo == "TM_START":
    #print "instante de inicio indet"
  #elif nomcampo == "UNI-TIME":
    #print "tiempo universal, ahí es nada"
  #elif nomcampo == "UNI_TIME":
    #print "tiempo universal, ahí es nada"
  #elif nomcampo == "USEC":
    #print "tiempo de exposición"
  #elif nomcampo == "UT":
    #print "inicio de algo, lo que sea"
  #elif nomcampo == "UTC":
    #print "inst de inicio en segundos suma"
  #elif nomcampo == "UT-END":
    #print "inst de fin en segundos suma"
  #elif nomcampo == "UT_END":
    #print "inst de fin en segundos suma"
  #elif nomcampo == "UTOBS":
    #print "inst aprox de inicio"
  #elif nomcampo == "UT_START":
    #print "inst de inicio indet de algo"
  #elif nomcampo == "CLOSTIME":
    #print "inst de cierre del obturador"
  #elif nomcampo == "CTIME":
    #print "inst de inicio de exposicion"
  #elif nomcampo == "DARKTIME":
    #print "darktime. muchas cosas"
  #elif nomcampo == "ELAPSED":
    #print "elapsed"
  #elif nomcampo == "EXPOSED":
    #print "exposed"
  #elif nomcampo == "EXP_ID":
    #print "exp ip"
  #elif nomcampo == "EXPTIME":
    #print "exposure"
  #elif nomcampo == "EXPOSURE":
    #print "exposure"
  #elif nomcampo == "EXPSTART":
    #print "expstart"
  #elif nomcampo == "LST":
    #print "lst"
  #elif nomcampo == "MNT_INFO":
    #print "mnt info"
  else:
    print "No se encuentra " +'\"'+ nomcampo +'\"'+ '\t\t' + ruta

def BuscaTiempo(cabecera,listaCampos):
  CamposFecha = ['DATE-AVG','JD-HELIO','JD','JUL-DATE','JUL_DATE','DATE','DATE-OBS','DATE_OBS','JD_HELIO','SID-TIME','SID_TIME','MJD','MJD-OBS','MNT_INFO','OPENTIME','READTIME','ST','STSTART','TIME''TIME-END','TIME_END','TM_START','TM-START','UNI-TIME','UNI_TIME','USEC','UT','UTC','UT_END','UT-END','UTOBS','UT_START','CLOSTIME','CTIME','DARKTIME','ELAPSED','EXPOSED','EXP_ID','EXPOSURE','EXPTIME','EXPSTART','LST']
  for i in CamposFecha:
    if i in (s.rstrip(' ') for s in listaCampos):
      TratamientoFecha(i,cabecera[i],cabecera.comments[i])
      break



  

def GetData(url):
  try:
    fuente = pyfits.open(url)
    listaCampos = fuente[0].header.keys()
    cabecera = fuente[0].header
    tiempo = BuscaTiempo(cabecera, listaCampos)
    fuente.close()
  except:
    print "Error al abrir " + url
    pass

  

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
      ruta = path + '/' + file # aquí antes había en medio un  + '/'
      #AddCampos(ruta, archivo_nombres_campos)
      #HashFile(ruta)
      GetData(ruta)
      j += 1
#GetData('ImagenesPrueba/2013AZ60-027Cle.fit')

Sort(archivo_nombres_campos)
msgfin = "Se han procesados " + str(j) + " archivos.", "green"
from termcolor import colored
print colored (msgfin, "green")


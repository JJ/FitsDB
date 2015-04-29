#!/usr/bin/python
# -*- coding: utf8 -*-
# Extracción de campos de archivos fits
import os, pyfits, sys
from os import listdir, walk
from datetime import datetime

print "Inicio: " + str(datetime.utcnow())

# HAY QUE IMPLEMENTAR UN LOG
#import logging
#LOG_FILENAME = 'fitsdb.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
#https://docs.python.org/2.6/library/logging.html


def ErrorSQL():
  from termcolor import colored
  print colored ("¡ERROR!", "red")
  print "No se ha encontrado la configuración necesaria para el uso de"
  print "la base de datos MySQL."
  print " "
  print "Debe rellenar los campos del archivo \'config.cfg\' relativos a"
  print "la base de datos según el ejemplo que se muestra a continuación:"
  print " "
  print "[mysql]"
  print "user = NombreDeUsuario"
  print "pass = Contraseña"
  print "dbname = NombreDeLaBaseDeDatos"
  print "hostname = DirecciónDelServidor"
  print " "
  print "Vuelva a intentarlo, por favor."
  print " "


def ErrorNoArg():
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


def ErrorMuchosArg():
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



def CheckFileExistence(nombrearchivo):
  if os.path.exists(nombrearchivo):
    return 1
  elif not os.path.exists(nombrearchivo):
    file(nombrearchivo, 'w').close()
    return 0


def CheckConfFileExistence():
  if os.path.exists("./config.cfg"):
    return 1
  elif not os.path.exists("./config.cfg"):
    import shutil
    shutil.copy("./config.cfg.new","./config.cfg")
    ErrorSQL()
    sys.exit()


def AddCampos(url, salida): # En desuso
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


def Sort(archivo): # En desuso
  f = open(archivo, 'r')
  mano = f.readlines()
  mano.sort()
  f.close()
  f = open(archivo, 'w')
  f.writelines(mano)
  f.close()



def HashFile(ruta):
  import hashlib
  BLOCKSIZE = 65536
  hasher = hashlib.md5()
  with open(ruta, 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
	  hasher.update(buf)
	  buf = afile.read(BLOCKSIZE)
  return hasher.hexdigest()



def JD2Date(entrada): # En desuso
  from astropy.time import Time
  dato = float(entrada)
  dia = int(dato)
  inst = dato - dia
  t = Time(dia, inst, format='jd')
  par = t.iso.split(' ')
  par[0] = t.iso.split(' ')[0].replace('/','-')
  par[1] = t.iso.split(' ')[1].replace('-',':')
  return par


def MJD2Date(entrada): # En desuso
  from astropy.time import Time
  dato = float(entrada)
  dia = int(dato)
  inst = dato - dia
  t = Time(dia, inst, format='mjd')
  par = t.iso.split(' ')
  par[0] = t.iso.split(' ')[0].replace('/','-')
  par[1] = t.iso.split(' ')[1].replace('-',':')
  return par

def FormatoFecha(cadena):
  if 'T' in cadena:
    par = cadena.split("T")
    par[0] = par[0].replace('/','-')
    par[1] = par[1].replace('-',':')
  else:
    par = [cadena.replace('/','-'),'']
  return par
 

# NO SE HA LLEGADO A USAR
#def EstCom(comentario,buscamos):
  #palabras = comentario.split(' ')
  #for i in palabras:
    #if i == buscamos:
      #return 1
      #break
  #return 0


def BuscaCosasEnCadena(cadena,arraycosas):
  contador = 0
  for j in arraycosas:
    if cadena.find(j) >= 0:
      contador -= 1
    else:
      contador += 1
  if contador != len(arraycosas):
    return 1
  else:
    return 0


def TiempoExp(cabecera,listaCampos):
  #CamposExp= ['EXPOSURE','EXPTIME']
  if "EXPOSURE" in listaCampos:
    return str(cabecera['EXPOSURE']).lstrip(' ')
  elif "EXPTIME" in listaCampos:
    return str(cabecera['EXPTIME']).lstrip(' ')
  else:
    print "No se encuentra el tiempo de exposición."
    
    
def BuscaHora(cabecera, listaCampos):
  CamposHora=['TIME-OBS','TIME_OBS','UTSTART','UT','EXPSTART','TIME-INI']
  for i in CamposHora:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
	return cabecera[i].rstrip(' ')
	break
  #print ruta
  #print listaCampos
  return 'UNK'

def TratamientoFecha(nomcampo,valcampo,comcampo): # Recibe los comentarios como argumento porque a veces hay info útil
  if nomcampo == "DATE-OBS":
    par = FormatoFecha(valcampo)
    par.extend([''])
  elif nomcampo == "DATE_OBS":
    par = FormatoFecha(valcampo)
    par.extend([''])
  elif nomcampo == "DATE-AVG":
    par = FormatoFecha(valcampo)
    par.extend([''])
    par.extend(['0']) # No hay que +/- T.exposición
  elif nomcampo == "DATE":
    par = FormatoFecha(valcampo)
    par.extend([''])
  elif nomcampo == "JD":
    par = JD2Date(str(valcampo))
    par.extend([''])
  elif nomcampo == "JUL-DATE":
    par = JD2Date(str(valcampo))
    par.extend([''])
  elif nomcampo == "JUL_DATE":
    par = JD2Date(str(valcampo))
    par.extend([''])
  elif nomcampo == "JD-HELIO":
    par.extend(['0']) # No hay que +/- T.exposición
  elif nomcampo == "JD_HELIO":
    par.extend(['0']) # No hay que +/- T.exposición
  else:
    print "No se encuentra " +'\"'+ nomcampo +'\"'+ '\t\t' + ruta
    par.extend([''])
  return par

def FechaDelNombre(par):
  import re
  rutaseg = ruta.split('/')
  for i in rutaseg:
    if re.search('[0-9]{8}',i):
      fecharuta = re.search('[0-9]{8}',i).group(0)
      par[0] = fecharuta[0:4] + "-" + fecharuta[4:6] + "-" + fecharuta[6:8]
      break
    elif re.search('[0-9]{6}',i):
      fecharuta = re.search('[0-9]{6}',i).group(0)
      par[0] = "20" + fecharuta[0:2] + "-" + fecharuta[2:4] + "-" + fecharuta[4:6]
      break
  return par



def BuscaFyT(cabecera,listaCampos):
  CamposFecha = ['DATE-OBS','DATE-AVG','JD','JUL-DATE','JUL_DATE','JD-HELIO','JD_HELIO','DATE_OBS','DATE','SID-TIME','SID_TIME','MJD','MJD-OBS','MNT_INFO','OPENTIME','READTIME','ST','STSTART','TIME''TIME-END','TIME_END','TM_START','TM-START','UNI-TIME','UNI_TIME','USEC','UT','UTC','UT_END','UT-END','UTOBS','UT_START','CLOSTIME','CTIME','DARKTIME','ELAPSED','EXPOSED','EXP_ID','EXPSTART','LST','SIMPLE']
  par = ['0','0','0']
  for i in CamposFecha:
    if i in (s.rstrip(' ') for s in listaCampos):
      if i != "SIMPLE":
	par = TratamientoFecha(i,cabecera[i].rstrip(' '),cabecera.comments[i]) # par es una lista de 3 componentes
	if par[1] == '0':
	  par[1] = BuscaHora(cabecera,listaCampos)
	par[2] = TiempoExp(cabecera, listaCampos)
	break
      else:
	break
  par = FechaDelNombre(par)
  return par



def BuscaInstr(cabecera,listaCampos): # Algunos archivos no tienen esta información
  CamposInstr = ['INSTRID','INSTRKEY','INSTRUM','INSTRUME','DETECTOR']
  for i in CamposInstr:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
	return cabecera[i]
	break
  #print ruta
  #prinLight Framet listaCampos
  return 'UNK'


def BuscarTelescopio(cabecera,listaCampos):
  CamposTelescopio = ['TELESCOP']
  for i in CamposTelescopio:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
	return cabecera[i]
	break
  #print ruta
  #print listaCampos
  return 'UNK'



def BuscaObservatorio2(cabecera,listaCampos): # Esta incluye coordenadas para los archivos sin observatorio WIP. En desuso
  CamposObservatorio = ['OBSERVAT','ORIGIN']
  salida = 'UNK'
  for i in CamposObservatorio:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
	salida = cabecera[i].replace('stron?mico','stronómico')
	return salida
	break
  print "peto1"
  CamposLong = ['SITELONG','LONGITUD','LONG-OBS']
  CamposLat = ['SITELAT','LATITUDE','LAT-OBS']
  for j in CamposLong:
    if j in (s.rstrip(' ') for s in listaCampos):
      print "peto2"
      if cabecera[j] != '':
	print "peto3"
	Long = cabecera[j]
    else:
      print "no está"
  print "peto2.1"
  for k in CamposLat:
    if k in (s.rstrip(' ') for s in listaCampos):
      if cabecera[k] != '':
	Lat = cabecera[k]
    else:
      print "tampoco está"
  if len(str(Long)) > 1:
    print "hay datos"
    salida = str(Long) + '; ' + str(Lat)
  else:
    return salida


def BuscaObservatorio(cabecera,listaCampos):
  CamposObservatorio = ['OBSERVAT','ORIGIN']
  salida = 'UNK'
  for i in CamposObservatorio:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
	salida = cabecera[i].replace('stron?mico','stronómico')
	return salida
	break
  return salida


def BuscaObject(cabecera,listaCampos): # En desuso en favor de la mejorada BuscaObject2
  CamposObject = ['OBJECT','OBJCAT']
  evitamos = ['','flat','bias','domme']
  import re
  for i in CamposObject:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i].strip(' ').lower() not in evitamos:
	#print ruta
	return cabecera[i]
	break
  #print ruta
  #print listaCampos
  return ruta.split('/')[-1].replace(" ", "")



def BuscaObject2(cabecera,listaCampos):
  CamposObject = ['OBJECT','OBJCAT','SIMPLE']
  lista1 = ['flat','dome']
  lista2 = ['dark','bias']
  import re
  for i in CamposObject:
    if i in (s.rstrip(' ') for s in listaCampos):
      if i != 'SIMPLE':
	if BuscaCosasEnCadena(cabecera[i].lower(),lista1):
	  ImgType = "Flat/Dome"
	  return "UNK"
	elif BuscaCosasEnCadena(cabecera[i].lower(),lista2):
	  ImgType = "Dark/Bias"
	  return "UNK"
	else:
	  ImgType = "Object"
	  return cabecera[i].upper().replace(" ", "")
	
	#if cabecera[i].strip(' ').lower() not in evitamos:
	  ##print ruta
	  #return cabecera[i].upper().replace(" ", "")
	  #break
      elif re.search('\d{4}[ A-Za-z]{2,3}\d{1,3}',ruta.split('/')[-1].replace("-","")):
	posiblenombre = re.search('\d{4}[ A-Za-z]{2,3}\d{1,3}',ruta.split('/')[-1].replace("-","")).group(0).replace(" ", "").upper()
	return posiblenombre
      else:
	posiblenombre = ruta.split('/')[-1].replace(" ", "")
	return posiblenombre


def ClassifyImgType(tipo, ruta):
  partes = tipo.lower().split(' ')
  carpetas = ruta.lower()
  listaCal = ['bias','flat','dark','dome']
  for i in listaCal:# and carpetas:
    if i in partes:
      return 0
    elif i in carpetas:
      return 0
  return 1



# Hay que unificar los tipos de imágenes
def BuscaImgType(cabecera,listaCampos):
  CamposImgType = ['IMAGETYP']
  lista1 = ['flat','dome']
  lista2 = ['dark','bias']
  for i in CamposImgType:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
        if BuscaCosasEnCadena(cabecera[i].lower(),lista1):
          return "Flat/Dome"
        elif BuscaCosasEnCadena(cabecera[i].lower(),lista2):
          return "Dark/Bias"
        else:
          return cabecera[i]
	#break
  #print ruta
  #print listaCampos
  return 'UNK'


 

def BuscaImgType2(cabecera,listaCampos):
  CamposImgType = ['IMAGETYP','SIMPLE']
  for i in CamposImgType:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
	return cabecera[i]
	break
  #print ruta
  #print listaCampos
  return 'UNK'



def BuscaFilter(cabecera,listaCampos):
  CamposFilter = ['FILTER']
  for i in CamposFilter:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
	return cabecera[i]
	break
  #print ruta
  #print listaCampos
  return 'UNK'

#--------------------------


def CrearTablaObs():
  cur.execute("""CREATE TABLE IF NOT EXISTS tablaobs
  (id BIGINT NOT NULL UNIQUE AUTO_INCREMENT,
  moddate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  md5sum CHAR(32),
  imgtype VARCHAR(20),
  object VARCHAR(30),
  dateobs DATE,
  timeobs TIME,
  exptime INT,
  observatory VARCHAR(80),
  telescope VARCHAR(80),
  instrument VARCHAR(80),
  filter VARCHAR(50),
  rute VARCHAR(200) NOT NULL)""")
  cur.execute("SET NAMES 'utf8'")
  cur.execute("SET CHARACTER SET utf8")


def IniciarDB():
  if CheckConfFileExistence():
    import ConfigParser
    import MySQLdb
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    varUser = config.get('mysql', 'user')
    varPass = config.get('mysql', 'pass')
    varDBName = config.get('mysql', 'dbname')
    varHost = config.get('mysql', 'hostname')
    if (varUser == "") or (varPass == "") or (varDBName == "") or (varHost == ""):
      print ErrorSQL()
      sys.exit()  
    else:
      global db
      db = MySQLdb.connect(host=varHost,user=varUser,passwd=varPass,db=varDBName)
      global cur
      cur = db.cursor()
      #cur.execute("SHOW TABLES")
      CrearTablaObs()






def CheckDB(suma): # más que suma debe recibir la ruta del archivo como argumento
  cur.execute('SELECT md5sum FROM tablaobs WHERE md5sum = %s',(suma,))
  if cur.fetchone():
    return 1
  else:
    return 0


def CheckDB2(ruta): # más que suma debe recibir la ruta del archivo como argumento
  cur.execute('SELECT rute FROM tablaobs WHERE rute = %s',(os.path.abspath(ruta),))
  if cur.fetchone():
    return 1
  else:
    return 0



#--------------------------



def GetData(url):
  #suma = HashFile(url)
  suma =''
  if CheckDB2(url):
    pass
  else:
    try:
      #print "par, instr y telescopio"
      fuente = pyfits.open(url)
      listaCampos = fuente[0].header.keys()
      cabecera = fuente[0].header
      par = BuscaFyT(cabecera, listaCampos)
      Instr = BuscaInstr(cabecera,listaCampos)
      Telescopio = BuscarTelescopio(cabecera,listaCampos)
      
      if 'OSN' in Telescopio:
	Observatorio = 'OSN'
	Telescopio = Telescopio.replace('OSN','').strip(' ')
      elif 'Sierra Nevada Observatory' in Telescopio:
	Observatorio = 'OSN'
	Telescopio = Telescopio.replace('Sierra Nevada Observatory','').strip(' ')
      elif 'ESO' in Telescopio:
	Observatorio = 'ESO'
	Telescopio = Telescopio.replace('ESO-','').strip(' ')
      elif 'IAC' in Telescopio:
	Observatorio = 'IAC'
      else:
	Observatorio = BuscaObservatorio(cabecera,listaCampos)
      Object = 'UNK'
      ImgType = 'UNK'
      Object = BuscaObject2(cabecera,listaCampos)
      ext = ['fit','fits','fts']
      ImgTypeContador = 0
      if ImgType == "UNK":
	if BuscaCosasEnCadena(Object,ext):
	  ImgType = "Object --KK"
	#for j in ext:
	  #if Object.lower().find(j) > 0:
	    #ImgTypeContador += 1
	  #else:
	    #ImgTypeContador -= 1
	#if ImgTypeContador == -3:
	  #ImgType = "Object --KK"
	if ImgType == "UNK":
	  ImgType = BuscaImgType(cabecera, listaCampos)
      
      
      #if ClassifyImgType(ImgType, ruta) == 1:
	#Object = BuscaObject(cabecera,listaCampos)
      #else:
	#Object = 'Flat/Bias'
	#ImgType= 'Flat/Bias'
      Filter = BuscaFilter(cabecera, listaCampos)

      try:
	
	cur.execute("""INSERT INTO tablaobs VALUES ('NULL',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(datetime.utcnow(),suma,ImgType,Object,par[0],par[1],par[2],Observatorio,Telescopio,Instr,Filter,os.path.abspath(url)))
	db.commit()
      except:
	print "---> No se ha podido introducir los datos del archivo: " + url
	pass


      fuente.close()
    except:
      print "---> Error al abrir " + url
      pass



if len(sys.argv) == 2:
  directorio_imagenes = sys.argv[1]
elif len(sys.argv) > 2:
  ErrorMuchosArg()
  sys.exit()
elif len(sys.argv) == 1:
  ErrorNoArg()
  sys.exit()

IniciarDB()
#archivo_nombres_campos = "nombres_de_campos"

j = 0
for (path, ficheros, archivos) in walk (directorio_imagenes):
  for file in archivos:
    if file.endswith(".fits") or file.endswith(".fit") or file.endswith(".fts"):
      ruta = path + '/' + file
      ruta = ruta.replace('//','/')
      #AddCampos(ruta, archivo_nombres_campos) # Antigua. Para listar todos los campos existentes
      GetData(ruta)
      
      j += 1


#Sort(archivo_nombres_campos)
msgfin = "Se han procesado " + str(j) + " archivos.", "green"
from termcolor import colored
print "Fin: " + str(datetime.utcnow())
print colored (msgfin, "green")


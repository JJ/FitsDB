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
  for j in arraycosas:
    if cadena.lower().find(j.lower()) >= 0:
      return 1
  return 0


def TiempoExp(cabecera,listaCampos):
  #CamposExp= ['EXPOSURE','EXPTIME']
  if "EXPOSURE" in listaCampos:
    return str(cabecera['EXPOSURE']).lstrip(' ')
  elif "EXPTIME" in listaCampos:
    return str(cabecera['EXPTIME']).lstrip(' ')
  #else:
    #print "No se encuentra el tiempo de exposición."
    
    
def BuscaHora(cabecera, listaCampos):
  CamposHora=['TIME-OBS','TIME_OBS','UTSTART','UT','EXPSTART','TIME-INI']
  for i in CamposHora:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
	return cabecera[i].rstrip(' ')
	break
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
  return 'UNK'


def BuscarTelescopio(cabecera,listaCampos):
  CamposTelescopio = ['TELESCOP']
  for i in CamposTelescopio:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
	return cabecera[i]
	break
  return 'UNK'


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



def BuscaObjYType(cabecera,listaCampos):
  CamposObject = ['OBJECT','OBJCAT','SIMPLE']
  CamposImgType = ['IMAGETYP','OBS-TYPE','ESO DPR CATG','SIMPLE']
  lista1 = ['flat','dome']
  lista2 = ['dark','bias','zero']
  lista3 = ['science','light','object','ACQUISITION']
  AoYt = ['UNK','UNK']
  if AoYt[1] == 'UNK':
    for j in CamposImgType:
      if j in (t.rstrip(' ') for t in listaCampos):
        if j != 'SIMPLE':
          if cabecera[j] != '':
            AoYt[1] = cabecera[j]
            break
  import re
  for i in CamposObject:
    if i in (s.rstrip(' ') for s in listaCampos):
      if cabecera[i] != '':
        if i != 'SIMPLE':
          AoYt[0] = cabecera[i].upper().replace(" ", "")
          if re.search('\d{4}[ A-Za-z]{2,3}\d{1,3}',AoYt[0]):
            AoYt[1] = 'Science'
          break
        elif re.search('\d{4}[ A-Za-z]{2,3}\d{1,3}',ruta.split('/')[-1].replace("-","")):
          AoYt[0] = re.search('\d{4}[ A-Za-z]{2,3}\d{1,3}',ruta.split('/')[-1].replace("-","")).group(0).replace(" ", "").upper()
          AoYt[1] = 'Science'
          break
        else:
          AoYt[0] = ruta.split('/')[-1].replace(" ", "")
          break
  # Afinando
  if BuscaCosasEnCadena(AoYt[0],lista1) or BuscaCosasEnCadena(AoYt[1],lista1):
    AoYt[0] = 'None'
    AoYt[1] = 'Flat/Dome'
  elif BuscaCosasEnCadena(AoYt[0],lista2) or BuscaCosasEnCadena(AoYt[1],lista2):
    AoYt[0] = 'None'
    AoYt[1] = 'Dark/Bias'
  elif BuscaCosasEnCadena(AoYt[0],lista3) or BuscaCosasEnCadena(AoYt[1],lista3):
    AoYt[1] = 'Science'
  return AoYt[0],AoYt[1]
  
  


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
      Object,ImgType = BuscaObjYType(cabecera,listaCampos)
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


msgfin = "Se han procesado " + str(j) + " archivos.", "green"
from termcolor import colored
print "Fin: " + str(datetime.utcnow())
print colored (msgfin, "green")


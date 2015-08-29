#!/usr/bin/python2
# -*- coding: utf8 -*-
# Extracción de campos de archivos fits
import os, sys
from os import listdir, walk
from datetime import datetime



def Error1():
  from termcolor import colored
  print colored ("¡ERROR!", "red")
  print "No se ha encontrado o no se ha podido acceder al archivo de configuración"
  print "necesario para el uso de la base de datos MySQL."
  print " "
  print "Si la carpeta \'/etc/fitsdb.d/\' no existe debe crearla."
  print "También debe rellenar los campos del archivo \'/etc/fitsdb.d/fitsdb.cfg\'"
  print "relativos a la base de datos según el ejemplo que se muestra a continuación:"
  print " "
  print "[mysql]"
  print "user = NombreDeUsuario"
  print "pass = Contraseña"
  print "dbname = NombreDeLaBaseDeDatos"
  print "hostname = DirecciónDelServidor"
  print " "
  print "Y darle permisos 644 de forma que todos los usuarios puedan leerlo."
  print "Vuelva a intentarlo, por favor."
  print " "


def ErrorNoArg():
  from termcolor import colored
  milog.info('Faltan argumentos! No se ejecutó el escaneo.')
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
  milog.info('Demasiados argumentos! No se ejecutó el escaneo.')
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


def CheckConfFile():
  global config
  import ConfigParser
  if os.path.exists("fitsdb.cfg"):
    config = ConfigParser.RawConfigParser()
    config.read('fitsdb.cfg')
    return 1
  elif not os.path.exists("fitsdb.cfg"):
    #import shutil
    #shutil.copy("/usr/local/etc/fitsdb.d/fitsdb.cfg.new","/usr/local/etc/fitsdb.d/fitsdb.cfg")
    Error1()
    sys.exit()


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



def JD2Date(entrada): # En desuso pero potencialmente útil
  from astropy.time import Time
  dato = float(entrada)
  dia = int(dato)
  inst = dato - dia
  t = Time(dia, inst, format='jd')
  par = t.iso.split(' ')
  par[0] = t.iso.split(' ')[0].replace('/','-')
  par[1] = t.iso.split(' ')[1].replace('-',':')
  return par


def JD2Date2(entrada): # En desuso pero potencialmente útil
  from astropy.time import Time
  arrayFechaJbruta = ['0','0']
  dato = float(entrada)
  dia = int(dato)
  inst = dato - dia
  t = Time(dia, inst, format='jd')
  t_rota = t.iso.split(' ')
  arrayFechaJbruta[0] = t_rota[0].replace('/','-')
  arrayFechaJbruta[1] = t_rota[1].replace('-',':')
  return arrayFechaJbruta[0],arrayFechaJbruta[1]


def MJD2Date(entrada): # En desuso pero potencialmente útil
  from astropy.time import Time
  dato = float(entrada)
  dia = int(dato)
  inst = dato - dia
  t = Time(dia, inst, format='mjd')
  par = t.iso.split(' ')
  par[0] = t.iso.split(' ')[0].replace('/','-')
  par[1] = t.iso.split(' ')[1].replace('-',':')
  return par


def MJD2Date2(entrada): # En desuso pero potencialmente útil
  from astropy.time import Time
  dato = float(entrada)
  dia = int(dato)
  inst = dato - dia
  t = Time(dia, inst, format='mjd')
  par = t.iso.split(' ')
  par[0] = t.iso.split(' ')[0].replace('/','-')
  par[1] = t.iso.split(' ')[1].replace('-',':')
  return par


def FormatoFecha2(fechabruta):
  if 'T' in fechabruta:
    arrayFechabruta = fechabruta.split("T")
    import re
    arrayFechabruta[0] = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}',arrayFechabruta[0].replace('/','-')).group(0)
    arrayFechabruta[1] = arrayFechabruta[1].replace('-',':')
  else:
    arrayFechabruta = ['0','0']
    if '/' in fechabruta:
      arrayFechabruta[0] = fechabruta.replace('/','-')
      arrayFechabruta[1] = '0'
    else:
      arrayFechabruta[0] = fechabruta
      arrayFechabruta[1] = '0'
  return arrayFechabruta[0],arrayFechabruta[1]


def BuscaCosasEnCadena(cadena,arraycosas):
  for j in arraycosas:
    if cadena.lower().find(j.lower()) >= 0:
      return 1
  return 0


def TiempoExp(cabecera,listaCampos):
  if "EXPOSURE" in listaCampos:
    return str(cabecera['EXPOSURE']).lstrip(' ')
  elif "EXPTIME" in listaCampos:
    return str(cabecera['EXPTIME']).lstrip(' ')
  else:
    return '0'
    

def BuscaHora2(cabecera, listaCampos):
  CamposHora=['TIME-OBS','TIME_OBS','UTSTART','UT','EXPSTART','TIME-INI','SIMPLE']
  for i in CamposHora:
    if i in (s.rstrip(' ') for s in listaCampos):
      if i == 'UT': # Esto es una chapuza porque la librería no consigue leer los campos UT
        try:
          import re
          if re.search('UT      = \'[0-9]{2}\:[0-9]{2}\:[0-9]{2}\.[0-9]{0,2}',str(cabecera)):
            horabruta = re.search('UT      = \'[0-9]{2}\:[0-9]{2}\:[0-9]{2}\.[0-9]{0,2}',l).group(0)
            return re.search('[0-9]{2}\:[0-9]{2}\:[0-9]{2}\.[0-9]{0,2}',horabruta).group(0)
          else:
            return '0'
        except:
          if str(cabecera[i]) != '':
            return str(cabecera[i]).rstrip(' ')
            break
      elif i != 'SIMPLE':
        if str(cabecera[i]) != '':
          return str(cabecera[i]).rstrip(' ')
          break
      else:
        return '0'


def TratamientoFecha2(nomcampo,valcampo):
  arrayFecha = ['0','0']
  tipofecha1 = ["DATE-OBS","DATE_OBS","DATE-AVG","DATE"]
  tipofecha2 = ["JD","JUL-DATE","JUL_DATE"]
  if nomcampo in (i for i in tipofecha1):
    arrayFecha[0],arrayFecha[1] = FormatoFecha2(valcampo)
  elif nomcampo in (j for j in tipofecha2):
    arrayFecha[0],arrayFecha[1] = JD2Date2(str(valcampo))
  else:
    print "No se encuentra " +'\"'+ nomcampo +'\"'+ '\t\t' + ruta # Esta linea iría en un hipotético log
  return arrayFecha[0],arrayFecha[1]


def FechaDelNombre2():
  import re
  rutaseg = ruta.split('/')
  for i in rutaseg:
    if re.search('[0-9]{8}',i):
      fecharuta = re.search('[0-9]{8}',i).group(0)
      if int(fecharuta[0:4]) <= int(datetime.utcnow().strftime('%Y')):
        fechamontada = fecharuta[0:4] + "-" + fecharuta[4:6] + "-" + fecharuta[6:8]
      else:
        fechamontada = '0'
      break
    elif re.search('[0-9]{6}',i):
      fecharuta = re.search('[0-9]{6}',i).group(0)
      if ((2000+int(fecharuta[0:2])) <= int(datetime.utcnow().strftime('%Y'))):
        fechamontada = "20" + fecharuta[0:2] + "-" + fecharuta[2:4] + "-" + fecharuta[4:6]
      else:
        fechamontada = '0'
      break
  return fechamontada


def BuscaFyT2(cabecera,listaCampos):
  CamposFecha = ['DATE-OBS','DATE-AVG','JD','JUL-DATE','JUL_DATE','SIMPLE']
  trio = ['0','0','0']
  for i in CamposFecha:
    if i in (s.rstrip(' ') for s in listaCampos):
      if i != "SIMPLE":
        if i !='':
          trio[0],trio[1] = TratamientoFecha2(i,cabecera[i].rstrip(' '))
          if trio[1] == '0':
            trio[1] = BuscaHora2(cabecera,listaCampos)
          trio[2] = TiempoExp(cabecera, listaCampos)
          break
      else:
	break
  if (trio[0] == '0') and int(config.get('general','fechaderuta')):
    print "---> Intentando sacar la fecha a partir de la ruta del archivo..."
    trio[0] = FechaDelNombre2()
  return trio[0],trio[1],trio[2]


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
  return 'UNK'

#--------------------------


def CrearTablaObs():
  try:
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
  except:
    milog.info('No se pudo crear la tabla \'tablaobs\' en la base de datos.')


def IniciarDB():
  if CheckConfFile():
    import MySQLdb
    varUser = config.get('mysql', 'user')
    varPass = config.get('mysql', 'pass')
    varDBName = config.get('mysql', 'dbname')
    varHost = config.get('mysql', 'hostname')
    if (varUser == "") or (varPass == "") or (varDBName == "") or (varHost == ""):
      print Error1()
      milog.info('Faltan datos para conectar con la base de datos. Comprobar archivo de configuración.')
      sys.exit()
    else:
      try:
        global db
        db = MySQLdb.connect(host=varHost,user=varUser,passwd=varPass,db=varDBName)
        global cur
        cur = db.cursor()
        CrearTablaObs()
        milog.info('Conexión a la base de datos realizada con éxito.')
      except:
        milog.info('Error al conectar con la base de datos.')


def IniciarLogging():
  import logging
  from logging.handlers import RotatingFileHandler
  global milog
  milog = logging.getLogger('main')
  milog.setLevel(20)     # Es lo mismo que la linea anterior
  logrot = RotatingFileHandler('logging.log',maxBytes=1048576,backupCount=4)
  milog.addHandler(logrot)
  formato = logging.Formatter('%(asctime)s -  %(message)s')
  logrot.setFormatter(formato)
    



def CheckDB(suma): # más que suma debe recibir la ruta del archivo como argumento
  cur.execute('SELECT md5sum FROM tablaobs WHERE md5sum = %s',(suma,))
  if cur.fetchone():
    return 1
  else:
    return 0


def CheckDB2(ruta):
  cur.execute('SELECT rute FROM tablaobs WHERE rute = %s',(os.path.abspath(ruta),))
  if cur.fetchone():
    return 1
  else:
    return 0



#--------------------------


def BloquePrincipal(url,suma,fuente):
    listaCampos = fuente[0].header.keys()
    cabecera = fuente[0].header
    par = ['0','0','0']
    par[0],par[1],par[2] = BuscaFyT2(cabecera,listaCampos)
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
      milog.info('Error al escribir en la base de datos la información de %s.',url)
      print "---> No se ha podido introducir los datos del archivo: " + url
      pass


    fuente.close()
    
def GetData(url):
  import pyfits
  # Estas dos lineas se quedan aquí por si se desea implementar la verificación por suma en vez de por localización.
  #suma = HashFile(url)
  suma = ''
  try:
    fuente = pyfits.open(url)
    BloquePrincipal(url,suma,fuente)
  except:
    milog.info('Error al abrir %s. Intentando reparar la cabecera...',url)
    try:
      fuente.verify('silentfix')
      fuente = pyfits.open(url)
      BloquePrincipal(url,suma,fuente)
      milog.info('Archivo reparado con éxito.')
    except:
      milog.info('Error. No se pudo reparar la cabecera. El archivo %s no ha sido incluido en la base de datos.',url)
      print "---> Error al abrir " + url
      pass

# --------------------------------------------- CUERPO DEL PROGRAMA ---------------------------------------------

if len(sys.argv) == 2:
  directorio_imagenes = sys.argv[1]
elif len(sys.argv) > 2:
  ErrorMuchosArg()
  sys.exit()
elif len(sys.argv) == 1:
  ErrorNoArg()
  sys.exit()

IniciarLogging()
milog.info('Iniciando FitsDB...')
IniciarDB()

rev = 0
nuevos = 0

milog.info('Iniciando barrido en busca de archivos zip.')
for (path, ficheros, archivos) in walk (directorio_imagenes):
  for archivo in archivos:
    if archivo.endswith(".zip"):
      import zipfile
      ruta = path + '/' + archivo
      ruta = ruta.replace('//','/')
      milog.info('Zip encontrado! Iniciando descompresión.')
      sitio = path + '/' + archivo.strip('.zip')
      try:
        zipfile.ZipFile(ruta).extractall(sitio)
        os.remove(ruta)
        milog.info('Zip descomprimido con éxito.')
      except:
        milog.info('Error al descomprimir el archivo Zip %s.',ruta)
milog.info('Finalizado el barrido en busca de archivos Zip.')


milog.info('Iniciando barrido en busca de archivos fit/fits.')
for (path, ficheros, archivos) in walk (directorio_imagenes):
  for archivo in archivos:
    if archivo.endswith(".fits") or archivo.endswith(".fit") or archivo.endswith(".fts"):
      ruta = path + '/' + archivo
      ruta = ruta.replace('//','/')
      if CheckDB2(ruta):
        pass
      else:
        GetData(ruta)
        nuevos += 1
      rev += 1


msgfin = "Se han procesado " + str(rev) + " archivos.\nSe han incluido "+str(nuevos)+" archivos a la base de datos."
milog.info('Se han procesado %s archivos. %s de ellos son nuevos.', str(rev), str(nuevos))
milog.info('Fin del escaneo. Se cierra Fitsdb.\n\n')
from termcolor import colored
print "\n\nFin: " + str(datetime.utcnow())
print colored (msgfin, "green")

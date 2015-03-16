#!/usr/bin/python
# -*- coding: utf8 -*-
# Probando existencia de archivos

import os, sys

ListaArgumentos = sys.argv
filename = ListaArgumentos[1]
def check(filename):
  if os.path.exists(filename):
    return 1
    #print "No existe el archivo."
    #file(filename, 'w').close()
  #else:
    #print "El archivo ya existe."
    
print "hola"

if check(filename):
  print "no"
else:
  print "si"


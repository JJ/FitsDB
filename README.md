# FitsDB
Utilidad para extraer metadatos de archivos fits y crear con ellos un catálogo que facilite la consulta de grandes colecciones de observaciones.

El catálogo generado es una base de datos MySQL de fácil consulta.

---

## Antes de usarlo

- Instalar las librerías que utiliza: MySQL-python, astropy, configparser,
mysql-connector-python, numpy, pyfits, termcolor
que se pueden instalar fácilmente con la herramienta 'pip'.
- Tener en marcha MySQL en el ordenador que vayáis a usar, con un usuario
para esto y una base de datos propia de ese usuario. Estos datos hay que
introducirlos en el archivo 'fitsdb.cfg' que se puede crear a partir de
'config.cfg.new'.
- Cuando vayáis a ejecutar el fitsdb.py hay que tener en cuenta que corre
con python 2.7 y que hay que pasarle como argumento el directorio raíz
donde se encuentran los archivos fits/fit.

# Documentación
A continuación se describe la documentación relativa al software desarrollado por Juan Pablo Navarro Sánchez para el manejo y consulta de datos fits en base de datos.

Actualmente el proyecto consta de las siguientes utilidades:

- extracampos.py
- otros

Pasamos ahora a describir el funcionamiento y los pormenores de cada utilidad.

## extracampos.py

### Funcionamiento
Se encarga de extraer los nombres de los campos de las cabeceras (headers) de cada uno de los archivos fits/fit/fts y evitando duplicidades los reune en un archivo llamado *nombres_de_campos* que se genera al concluir su ejecución en el mismo directorio de ejecución. Además se muestra el número de imágenes procesadas.

Esta utilidad admite como único argumento el directorio donde se encuentran las imágenes. Si se ejecuta sin argumentos o con más de uno, se mostrará un mensaje de error indicando cómo debe ejecutarse.

### Funciones

- CheckFileExistence(nombrearchivo)
- Add(url,salida)
- Sort(archivo)
- HashFile(ruta)
- GenCsvWithHeaders(sitio,name)

#### CheckFileExistence(nombrearchivo)
Comprueba si el archivo que recibe como argumento existe. Si es así devuelve 1, y si no es así primero crea el archivo y luego devuelve 0.

#### Add(url,salida)
Añade los campos del archivo que se encuentra en *url* al archivo que se encuentra en *salida*.

#### Sort(archivo)
Ordena el archivo que se le da como argumento por orden alfabético.

#### HashFile(ruta)
Genera la suma de verificación md5 del archivo que se le da como argumento.

#### GenCsvWithHeaders(sitio,name)
POR COMPLETAR
Genera un archivo csv (";" como separadores) con los datos listos para incorporar a la base de datos.

### Librerías

- os
- sys
- pyfits
- hashlib
- termcolor

#### os 
Se utiliza para el trabajo con archivos.

#### sys
Se utiliza para interactuar con el sistema.

#### pyfits
Se utiliza para trabajar de forma más cómoda con los archivos fits.

#### hashlib
Se utiliza para calcular sumas de verificación.

#### termcolor
Se utiliza para mostrar salidas en color por pantalla.
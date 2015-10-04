#!/bin/bash
py_path="/usr/bin/python2"
web_path="/var/www"
web_path_full="/var/www/fitsdb"
root_path=$(dirname $0)
home_path="/home/"$USER"/.FitsDB"
temp_path="/tmp/fitsdb_install"
con_pass="""
\n
auth.debug = 2\n
auth.backend = \"plain\"\n
auth.backend.plain.userfile = \"$home_path/lighttpd_password\"\n
auth.require = ( \"/fitsdb/\" =>\n
(\n
\"method\" => \"basic\",\n
\"realm\" => \"Zona protegida\",\n
\"require\" => \"valid-user\"\n
)\n
)
"""

echo -e """
########################### FitsDB ###########################

Iniciando asistente de instalación de FitsDB para Ubuntu. 
Actualmente no soporta otras distribuciones, pero FitsDB 
puede ser instalado siguiendo los pasos descritos en README.md.

--------------------------------------------------------------



"""
distro=$(cat /etc/*-release* | grep -e "ID=ubuntu")
if [ ! $distro ]; then
  exit
fi

# Instalamos requisitos desde el gestor de paqutes
sudo apt install python-{setuptools,mysql.connector,numpy} lighttpd dialog php5-cgi

# Instalamos cosas desde easy install
sudo easy_install pip virtualenv

# Preparamos el entorno privado virtual
virtualenv -p $py_path venv

# Entramos en venv
source venv/bin/activate

# Instalamos requisitos en venv
pip install --upgrade setuptools
pip install -r requirements.txt

# Configuramos el directorio principal de FitsDB
mkdir $home_path
for f in $root_path""/{fitsdb.py,config.cfg.new,License,README.md}""; do
  cp $f $home_path"/."
done
cp $home_path"/config.cfg.new" $home_path"/config.cfg"

dialog --msgbox "Iniciando la configuración de FitsDB... \n \n A continuación se va a mostrar el asistente de configuración de FitsDB. Recuerde que siempre puede cambiar la configuración editando el archivo config.cfg que se encuentra en $home_path. Hágalo bajo su propia responsabilidad." 0 0

type_db=$(dialog --stdout --radiolist 'Seleccione el tipo de base de datos que desee usar:' 0 0 0 sqlite "Recomendada para la mayoría de las instalaciones. Seleccionada por defecto." "on" mysql "Recomendada para instalaciones con gran afluencia. Si elige esta opción tendrá que configurar su servidor MySQL de forma manual." "")

case $type_db in
        sqlite)
          sed -i "s/basededatos =/basededatos = sqlite/" $home_path"/config.cfg"
          nombre=$(dialog --stdout --inputbox "Escriba el nombre de la base de datos SQLite:" 0 0 fitsdb)
          sed -i "s/nombre =/nombre = $nombre/" $home_path"/config.cfg" > $home_path"/config.cfg"
          sudo apt-get install sqlite3
          ln -s $home_path"/"$nombre $web_path_full"/"$nombre
          ;;
        mysql)
          sed -i "s/basededatos =/basededatos = mysql/" $home_path"/config.cfg"
          mysql_user=$(dialog --stdout --inputbox "Escriba el nombre de usuario de MySQL:" 0 0)
          mysql_pass=$(dialog --stdout --inputbox "¡Atención, esta contraseña se guardará en texto plano!\nEscriba la contraseña del usuario $mysql_user:" 0 0)
          mysql_dbname=$(dialog --stdout --inputbox "Escriba el nombre de la base de datos a utilizar:" 0 0)
          mysql_hostname=$(dialog --stdout --inputbox "Escriba la dirección del servidor MySQL:" 0 0 localhost)
          sed -i "s/user =/user = $mysql_user/" $home_path"/config.cfg"
          sed -i "s/pass =/pass = $mysql_pass/" $home_path"/config.cfg"
          sed -i "s/dbname =/dbname = $mysql_dbname/" $home_path"/config.cfg"
          sed -i "s/hostname =/hostname = $mysql_hostname/" $home_path"/config.cfg"
          sudo apt-get install mysql-server
          ;;
        *)
          sed -i "s/basededatos =/basededatos = sqlite/" $home_path"/config.cfg"
          nombre=$(dialog --stdout --inputbox "Escriba el nombre de la base de datos SQLite:" 0 0 fitsdb)
          sed -i "s/nombre =/nombre = $nombre/" $home_path"/config.cfg"
          ;;
esac

# Copiamos los archivos a la carpeta del servidor
mv $web_path"/index.html" $web_path"/index_bak.html"
sudo mkdir $web_path_full
sudo chown $USER $web_path_full
sudo chgrp $USER $web_path_full
for f in $root_path""/web/{estilo.css,{download,index}.php}""; do
  cp $f $web_path_full"/." 
done
# El archivo de configuración va como enlace simbólico
ln -s $home_path"/config.cfg" $web_path_full"/config.cfg" 
# Hacemos una copia de la configuración que tenía Lighttpd
sudo cp /etc/lighttpd/lighttpd.conf /etc/lighttpd/lighttpd_FitsDBbak.conf
# Configuramos el servidor
sudo lighty-enable-mod fastcgi
sudo lighty-enable-mod fastcgi-php


web_pass=$(dialog --stdout --radiolist "¿Desea proteger la interfaz web mediante usuario y contraseña? \n Las credenciales se guardarán en el archivo /lighttpd_password situado en $home_path." 0 0 0 "1" "Sí" "" "2" "No (por defecto)" "on" )
mkdir $temp_path
cp /etc/lighttpd/lighttpd.conf $temp_path"/lighttpd.conf"

case $web_pass in
  1)
    if [ ! $(grep mod_auth $temp_path"/lighttpd.conf") ]; then
      sed -i "s/mod_redirect/mod_redirect\",\n\t\"mod_auth/" $temp_path"/lighttpd.conf"
    fi
    web_user=$(dialog --stdout --inputbox "Escriba el nombre de usuario de la interfaz web:" 0 0)
    web_pass=$(dialog --stdout --inputbox "¡Atención, esta contraseña se guardará en texto plano!\nEscriba la contraseña del usuario $web_user:" 0 0)
    echo $web_user":"$web_pass > $home_path"/lighttpd_password" # OJO! este archivo quizás deba ser del www-data
    dialog --msgbox "Si necesita añadir, quitar o modificar usuarios y contraseñas solo tiene que editar el archivo lighttpd_password situado en $home_path manteniendo el formato nombredeusuario:contraseña." 0 0
    
    if [ ! $(grep "server.follow-symlink" $temp_path"/lighttpd.conf") ]; then
      echo "server.follow-symlink=\"enable\"" >> $temp_path"/lighttpd.conf"
    fi
    echo -e $con_pass >> $temp_path"/lighttpd.conf"
    ;;
  2)
    if [ ! grep "server.follow-symlink" $temp_path"/lighttpd.conf" ]; then
      echo "server.follow-symlink=\"enable\"" >> $temp_path"/lighttpd.conf"
    fi
    ;;
  *)
    if [ ! grep "server.follow-symlink" $temp_path"/lighttpd.conf" ]; then
      echo "server.follow-symlink=\"enable\"" >> $temp_path"/lighttpd.conf"
    fi
    
    ;;
esac

sudo cp $temp_path"/lighttpd.conf" /etc/lighttpd/lighttpd.conf
sudo /etc/init.d/lighttpd force-reload

dialog --stdout --yesno "Para el correcto funcionamiento de FitsDB se recomienda programar mediante CRON un escaneo periódico de la base de datos. ¿Desea programar un escaneo semanal ahora? " 0 0
if [ $? -eq 0 ]; then
  carpeta=$(dialog --stdout --title "Directorio a escanear" --dselect $PWD 0 0)
  dia=$(dialog --stdout --radiolist "Día de la semana" 0 0 0 "1" "lunes" "on" "2" "martes" "" "3" "miércoles" "" "4" "jueves" "" "5" "viernes" "" "6" "sábado" "" "7" "domingo" "")
  hora=$(dialog --stdout --timebox "Seleccione la hora" 0 0 0 0)
  hora1=$(echo $hora| tr ":" " "|awk '{print $1}')
  hora2=$(echo $hora| tr ":" " "|awk '{print $2}')
  linea="$hora2 $hora1 "*" "*" $dia $home_path"/fitsdb.py" $carpeta"
  crontab -l > $temp_path"/cron_tmp"
  echo "$linea" >> $temp_path"/cron_tmp"
  crontab $temp_path"/cron_tmp"
fi

dialog --msgbox "Asistente de instalación finalizado." 0 0
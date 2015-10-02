#!/bin/bash
py_path="/usr/bin/python2"
web_path="/var/www"
web_path_full="/var/www/fitsdb"
root_path=$(dirname $0)
home_path="/home/"$USER"/.FitsDB"

dialog --msgbox "Iniciando asistente de instalación de FitsDB para Ubuntu. Actualmente no soporta otras distribuciones, pero FitsDB puede ser instalado siguiendo los pasos descritos en README.md." 0 0

# Instalamos requisitos desde el gestor de paqutes
sudo apt install python-{setuptools,mysql.connector,numpy} lighttpd

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
for f in $root_path""{fitsdb.py,config.cfg.new,License,README.md}""
  cp $f $home_path"/."
done

dialog --msgbox "Iniciando la configuración de FitsDB... \n \n A continuación se va a mostrar un asistente de configuración de FitsDB. Recuerde que siempre puede editar la configuración si le resulta necesario editando el archivo config.cfg que se encuentra en $home_path. Hágalo bajo su propia responsabilidad." 0 0

type_db=$(dialog --stdout --radiolist 'Seleccione el tipo de base de datos que desee usar:' 0 0 0 sqlite "Recomendada para la mayoría de las instalaciones. Seleccionada por defecto." "" mysql "Recomendada para instalaciones con gran afluencia. Si elige esta opción tendrá que configurar su servidor MySQL de forma manual." "")

case $type_db in
        sqlite)
          sed -e "s/basededatos =/basededatos = sqlite/" $home_path"/config.cfg.new" > $home_path"/config.cfg"
          nombre=$(dialog --stdout --inputbox "Escriba el nombre de la base de datos SQLite:" 0 0 fitsdb)
          sed -e "s/nombre =/nombre = $nombre/" $home_path"/config.cfg" > $home_path"/config.cfg"
          sudo apt-get install sqlite3
          ;;
        mysql)
          sed -e "s/basededatos =/basededatos = mysql/" $home_path"/config.cfg.new" > $home_path"/config.cfg"
          mysql_user=$(dialog --stdout --inputbox "Escriba el nombre de usuario de MySQL:" 0 0)
          mysql_pass=$(dialog --stdout --inputbox "¡Atención, esta contraseña se guardará en texto plano!\nEscriba la contraseña del usuario $mysql_user:" 0 0)
          mysql_dbname=$(dialog --stdout --inputbox "Escriba el nombre de la base de datos a utilizar:" 0 0)
          mysql_hostname=$(dialog --stdout --inputbox "Escriba la dirección del servidor MySQL:" 0 0 localhost)
          sed -e "s/user =/user = $mysql_user/" $home_path"/config.cfg" > $home_path"/config.cfg"
          sed -e "s/pass =/pass = $mysql_pass/" $home_path"/config.cfg" > $home_path"/config.cfg"
          sed -e "s/dbname =/dbname = $mysql_dbname/" $home_path"/config.cfg" > $home_path"/config.cfg"
          sed -e "s/hostname =/hostname = $mysql_hostname/" $home_path"/config.cfg" > $home_path"/config.cfg"
          sudo apt-get install mysql-server
          ;;
        *)
          sed -e "s/basededatos =/basededatos = sqlite/" $home_path"/config.cfg.new" > $home_path"/config.cfg";;
          nombre=$(dialog --stdout --inputbox "Escriba el nombre de la base de datos SQLite:" 0 0 fitsdb)
          sed -e "s/nombre =/nombre = $nombre/" $home_path"/config.cfg" > $home_path"/config.cfg"
esac

# Copiamos los archivos a la carpeta del servidor
mv $web_path"/index.html" $web_path"/index_bak.html"
mkdir $web_path_full
for f in $root_path""/web/{estilo.css,{download,index}.php}""; do
  cp $f $web_path_full"/." 
done
# El archivo de configuración va como enlace simbólico
ln -s $home_path"/config.cfg" $web_path_full"/config.cfg" 
# Hacemos una copia de la configuración que tenía Lighttpd
mv /etc/lighttpd/lighttpd.conf /etc/lighttpd/lighttpd_FitsDBbak.conf
# Configuramos el servidor
sudo /usr/sbin/lighty-enable-mod cgi


web_pass=$(dialog --stdout --radiolist "¿Desea proteger la interfaz web mediante usuario y contraseña? \n Las credenciales se guardarán en el archivo /lighttpd_password situado en $home_path." 0 50 0 "1" "Sí" "" "2" "No (por defecto)" "" )
case $web_pass in
  1)
    sudo sed -e "s/mod_redirect/mod_redirect\",\n\t\"mod_auth/" /etc/lighttpd/lighttpd_FitsDBbak.conf > /etc/lighttpd/lighttpd.conf
    web_user=$(dialog --stdout --inputbox "Escriba el nombre de usuario de la interfaz web:" 0 0)
    web_pass=$(dialog --stdout --inputbox "¡Atención, esta contraseña se guardará en texto plano!\nEscriba la contraseña del usuario $web_user:" 0 0)
    echo $web_user":"$web_pass > $home_path"/lighttpd_password" # OJO! este archivo quizás deba ser del www-data
    dialog --msgbox "Si necesita añadir, quitar o modificar usuarios y contraseñas solo tiene que editar el archivo lighttpd_password situado en $home_path manteniendo el formato nombredeusuario:contraseña." 00
    echo """
server.follow-symlink="enable"

auth.debug = 2
auth.backend = "plain"
auth.backend.plain.userfile = "$home_path/lighttpd_password"
auth.require = ( "/fitsdb/" =>
(
"method" => "basic",
"realm" => "Zona protegida",
"require" => "valid-user"
)
)
""" >> /etc/lighttpd/lighttpd.conf
    ;;
  2)
    echo """server.follow-symlink="enable"
)
""" >> /etc/lighttpd/lighttpd.conf
    ;;
  *)
    echo """server.follow-symlink="enable"
)
""" >> /etc/lighttpd/lighttpd.conf
    ;;
esac



# Falta configurar el cron con escaneos periódicos
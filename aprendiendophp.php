<?php
require_once('funciones.php');
conectar('Tu Servidor', 'Tu Usuario BD', 'Pass de BD', 'Nombre de la BD');
 
//Recibir
$nombre = strip_tags($_POST['nombre']);
$email = strip_tags($_POST['email']);
$user = strip_tags($_POST['user']);
$password = strip_tags(sha1($_POST['password']));
 
$query = @mysql_query('SELECT * FROM usuarios WHERE user="'.mysql_real_escape_string($user).'"');
if($existe = @mysql_fetch_object($query))
{
    echo 'El usuario '.$user.' ya existe.';    
}
else{
    $meter = @mysql_query('INSERT INTO usuarios (nombre, email, user, password) values ("'.mysql_real_escape_string($nombre).'", "'.mysql_real_escape_string($email).'", "'.mysql_real_escape_string($user).'", "'.mysql_real_escape_string($password).'")');
    if($meter)
    {
        echo 'Usuario registrado con exito';
    }else{
        echo 'Hubo un error en el registro.';    
    }
}
?>
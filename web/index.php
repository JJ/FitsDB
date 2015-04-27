<html>
<meta charset="utf-8" /> 
<title>
FitsDB v0.1.1-1
</title>
<link href="estilo.css" rel="stylesheet" type="text/css">
<body>
<div id='main'>
<?php
set_time_limit(0);
define('DEBUG', false);
// session_start();
//error_reporting(E_ALL);
//ini_set('display_errors', true);
limpieza('descargas/');
// limpieza('sesion/');


//Recibir
$idnum = strip_tags($_POST['idnum']);
$typeimg = strip_tags($_POST['typeimg']);
$nombre_obj= strip_tags($_POST['nombre_obj']);
$fecha_obs1= strip_tags($_POST['fecha_obs1']);
$fecha_obs2= strip_tags($_POST['fecha_obs2']);
$exptime1= strip_tags($_POST['exptime1']);
$exptime2= strip_tags($_POST['exptime2']);
$observatorio= strip_tags($_POST['observatorio']);
$telescopio= strip_tags($_POST['telescopio']);
$instrumento= strip_tags($_POST['instrumento']);
$filtro= strip_tags($_POST['filtro']);


?>


<script language="JavaScript"> // Script en js para (des)marcar todas las casillas con una casilla maestras
function cambiar(){
  var cajamaestra = document.forms['form2'].elements['marcartodos'];
  var lista = document.getElementsByClassName('A');
  if (cajamaestra.checked){
  // alert('Ahora está marcado');
    for (var i=0; i < lista.length; i++){
      lista[i].checked = true;
    }
  }
  else{
  // alert('Ahora no está marcado');
    for (var i=0; i < lista.length; i++){
      lista[i].checked = false;
    }
  }
}
</script>

<H1 align=center>Interfaz web de FitsDB</H1>

<form id="form1" name="form1" method="post" action="index.php" align="right">
  <table width="900" border="0" align="center">
  <tr>
    <td>Nombre del objeto:</td>
    <td>
	<?php
	if (strlen($nombre_obj)>0){
	echo "<input type='text' name='nombre_obj' list='listanombres_obj' value='".$nombre_obj."' autocomplete autofocus/>";
	}
	else{
	echo "<input type='text' name='nombre_obj' list='listanombres_obj' autocomplete autofocus/>";
	}
	?>
	<datalist id="listanombres_obj">
	<?php
	$arrayobjetos = array('Varuna','Orcus','Eris');
	natsort($arrayobjetos);
	foreach($arrayobjetos as $i){
	  echo "<option value='".$i."'>".$i."</option>";
	}
	?>
	</datalist>
    </td>
    <td>
    </td>
    </td>
    <td>
    </td>
  </tr>
    <tr>
    <td>Telescopio:</td>
    <td>
<!--       <input type="text" name="telescopio" id="telescopio" autocomplete /> -->
	<?php
	if (strlen($telescopio)>0){
	echo "<input type='text' name='telescopio' id='telescopio' value='".$telescopio."' autocomplete />";
	}
	else{
	echo "<input type='text' name='telescopio' id='telescopio' autocomplete />";
	}
	?>
    </td>
        <td>Instrumento:</td>
    <td>
<!--       <input type="text" name="instrumento" id="instrumento" autocomplete /> -->
      	<?php
	if (strlen($instrumento)>0){
	echo "<input type='text' name='instrumento' id='instrumento' value='".$instrumento."' autocomplete />";
	}
	else{
	echo "<input type='text' name='instrumento' id='instrumento' autocomplete />";
	}
	?>
    </td>
  </tr>
  <tr>
    <td>Fecha de la observación:</td>
    <td>
<!--       <input type="date" name="fecha_obs1" style="width: 140px;"></input> -->
      	<?php
	if (strlen($fecha_obs1)>0){
	echo "<input type='date' name='fecha_obs1' style='width: 140px' value='".$fecha_obs1."' autocomplete />";
	}
	else{
	echo "<input type='date' name='fecha_obs1' style='width: 140px' autocomplete />";
	}
	?>
      a 
<!--       <input type="date" name="fecha_obs2" style="width: 140px;"></input> -->
      	<?php
	if (strlen($fecha_obs2)>0){
	echo "<input type='date' name='fecha_obs2' style='width: 140px' value='".$fecha_obs2."' autocomplete />";
	}
	else{
	echo "<input type='date' name='fecha_obs2' style='width: 140px' autocomplete />";
	}
	?>
    </td>
    <td>
    </td>
    </td>
    <td>
    </td>
  </tr>
    <tr>
    <td>Filtro:</td>
    <td>
<!--       <input type="text" name="filtro" id="filtro" autocomplete /> -->
      	<?php
	if (strlen($filtro)>0){
	echo "<input type='text' name='filtro' id='filtro' value='".$filtro."' autocomplete />";
	}
	else{
	echo "<input type='text' name='filtro' id='filtro' autocomplete />";
	}
	?>
    </td>
    <td>Tipo de imagen:</td>
    <td>
<!-- 	<input type="text" name="typeimg" list="listatipos" autocomplete/> -->
      	<?php
	if (strlen($typeimg)>0){
	echo "<input type='text' name='typeimg' id='typeimg' list='listatipos' value='".$typeimg."' autocomplete />";
	}
	else{
	echo "<input type='text' name='typeimg' id='typeimg' list='listatipos' autocomplete />";
	}
	?>
	<datalist id="listatipos">
	<?php
	$arraytipos = array('Flat', 'Domme','Bias', 'Dark','Science');
	natsort($arraytipos);
	foreach($arraytipos as $i){
	  echo "<option value='".$i."'>".$i."</option>";
	}
	?>
	</datalist>
    </td>
  </tr>
    <tr>
    <td>Tiempo de exposición:</td>
    <td>
<!--       <input type="number" name="exptime1" id="exptime1" step="10" style="width: 79px;" min="0"/> -->
      	<?php
	if (strlen($exptime1)>0){
	echo "<input type='number' name='exptime1' id='exptime1' step='10' style='width: 79px;' min='0' value='".$exptime1."'/>";
	}
	else{
	echo "<input type='number' name='exptime1' id='exptime1' step='10' style='width: 79px;' min='0' />";
	}
	?>
      a 
<!--       <input type="number" name="exptime2" id="exptime2" step="10" style="width: 79px;" min="0" /> -->
      	<?php
	if (strlen($exptime2)>0){
	echo "<input type='number' name='exptime2' id='exptime2' step='10' style='width: 79px;' min='0' value='".$exptime2."'/>";
	}
	else{
	echo "<input type='number' name='exptime2' id='exptime2' step='10' style='width: 79px;' min='0' />";
	}
	?>

    </td>
        </td>
    <td>
    </td>
    </td>
    <td>
    </td>
  </tr>

    <tr>
    <td>Observatorio:</td>
    <td>
<!-- 	<input type="text" name="observatorio" list="listaobservatorio" autocomplete/> -->
      	<?php
	if (strlen($observatorio)>0){
	echo "<input type='text' name='observatorio' id='observatorio' list='listaobservatorio' value='".$observatorio."' autocomplete />";
	}
	else{
	echo "<input type='text' name='observatorio' id='observatorio' list='listaobservatorio' autocomplete />";
	}
	?>
	<datalist id="listaobservatorio">
	<?php
	$arrayobservatorio = array('OSN','DSAZ','CGG','Teide','Atacama','IAC','la hita','lapalma');
	natsort($arrayobservatorio);
	foreach($arrayobservatorio as $i){
	  echo "<option value='".$i."'>".$i."</option>";
	}
	?>
	</datalist>
    </td>
    <td>
    </td>
    </td>
    <td>
    </td>
  </tr>
  <tr>
    <td>ID:</td>
    <td>
<!--       <input type="number" name="idnum" id="idnum" /> -->
      	<?php
	if (strlen($idnum)>0){
	echo "<input type='number' name='idnum' id='idnum' min='0' value='".$idnum."' />";
	}
	else{
	echo "<input type='number' name='idnum' id='idnum' min='0'  />";
	}
	?>
    </td>
    <td>
    </td>
    </td>
    <td>
    </td>
  </tr>
  <tr>
    <td>
    </td>
    <td>
    <input type="submit" name="enviar" id="enviar" value="Enviar consulta" />
    </td>
    <td>
<!--     <input type="reset" id="reset" value="Limpiar formulario" /> -->
    <input type="button" id="reset2" value="Limpiar formulario" onClick='window.location.reload()' />
    </td>
    <td>
    </td>
  </tr>
</table>
</form>
<H2 align=center>Resultados</H2>

<br>

<?php


$prefijo = "SELECT id, object, telescope, instrument, dateobs, timeobs, filter, imgtype, exptime, observatory, rute FROM tablaobs";
$sufijo = '';


if (strlen($idnum) != 0) {
  $sufijo = $sufijo . sprintf(" id = '%s'",$idnum) ." and";
  }

if (strlen($typeimg) != 0) {
  $sufijo = $sufijo . sprintf(" imgtype like '%%%s%%'",$typeimg) . " and";
  }

if (strlen($nombre_obj) != 0) {
  $nombre_obj = str_replace(' ', '', $nombre_obj);
  $sufijo = $sufijo . sprintf(" object like '%%%s%%'",$nombre_obj) . " and";
  }

if ((strlen($fecha_obs1) != 0) && (strlen($fecha_obs2) != 0)) {
  $sufijo = $sufijo . sprintf(" (dateobs BETWEEN '%s' AND '%s')", $fecha_obs1, $fecha_obs2) . " and";
  }

if ((strlen($exptime1) != 0) && (strlen($exptime2) != 0)) {
  $sufijo = $sufijo . sprintf(" (exptime BETWEEN '%s' AND '%s')", $exptime1, $exptime2) . " and";
  }

if (strlen($observatorio) != 0) {
  $sufijo = $sufijo . sprintf(" observatory like '%%%s%%'",$observatorio) . " and";
  }


if (strlen($telescopio) != 0) {
  $sufijo = $sufijo . sprintf(" telescope like '%%%s%%'",$telescopio) . " and";
  }

if (strlen($instrumento) != 0) {
  $sufijo = $sufijo . sprintf(" instrument like '%%%s%%'",$instrumento) . " and";
  }

if (strlen($filtro) != 0) {
$sufijo = $sufijo . sprintf(" filter like '%%%s%%'",$filtro);
}

if ((strlen($idnum) != 0) || (strlen($typeimg) != 0) || (strlen($nombre_obj) != 0) || (strlen($fecha_obs1) != 0) || (strlen($fecha_obs2) != 0) ||(strlen($exptime1) != 0) ||(strlen($exptime2) != 0) || (strlen($observatorio) != 0) || (strlen($telescopio) != 0) || (strlen($instrumento) != 0) || (strlen($filtro) != 0)) {
  $montamos = $prefijo . " WHERE" . $sufijo;
  $peticion = preg_replace('/and$/', '', $montamos);
//   echo "<table width='500' align='left'><tr><td>Se muestra la siguiente petición:</td><td> </td></tr>";
//   echo "<tr><td>Nombre del objeto:</td><td>" . $nombre_obj . "</td></tr>";
//   echo "<tr><td>Telescopio:</td><td>" . $telescopio . "</td></tr>";
//   echo "<tr><td>Instrumento:</td><td>" . $instrumento . "</td></tr>";
//   echo "<tr><td>Fecha de observación entre:</td><td>" . $fecha_obs1 . " y " . $fecha_obs2 . "</td></tr>";
//   echo "<tr><td>Filtro:</td><td>" . $filtro . "</td></tr>";
//   echo "<tr><td>Tipo de de imagen:</td><td>" . $typeimg . "</td></tr>";
//   echo "<tr><td>Tiempo de exposición entre:</td><td>" . $exptime1 . " y " . $exptime2 . "</td></tr>";
//   echo "<tr><td>Observatorio:</td><td>" . $observatorio . "</td></tr>";
//   echo "<tr><td>ID:</td><td>" . $idnum . "</td></tr>";
//   echo "</table>";
//   echo "<br>";

echo "Se muestran los resultados de su consulta.";
  }
else {
  $peticion = "SELECT id, object, telescope, instrument, dateobs, timeobs, filter, imgtype, exptime, observatory, rute FROM tablaobs WHERE DATE_SUB(CURDATE(), INTERVAL 31 DAY) <= dateobs ORDER BY dateobs DESC";
   echo "<p>Se muestran las observaciones realizadas en los últimos 31 días.</p>";
  }

  
  

$conexion = new mysqli("127.0.0.1", "pablo", "halconmilenario", "pruebasdb");

$resultado = $conexion->query($peticion);
$resultado -> data_seek(0);
$archivos = array();
?>
<form id="form2" name="form2" method="post" action="download.php" align="right">
<input type="submit" class ="button" name="descargazip" value="Descargar archivos comprimidos" />
<!-- <input type="submit" class ="button" name="descargatar" value="Descargar sin comprimir" /> -->

<br>
<br>
<table border=0 align=center class='zebra'>
  <thead>
    <tr align='center'>
	<th width=1%>
	    <input type="checkbox" name="marcartodos" onClick="cambiar()" checked>
	</th>
      <th width=3%>
	ID
      </th>
      <th width=7%>
	Nombre
      </th>
      <th width=6%>
	Telescopio
      </th>
      <th width=9%>
	Instrumento
      </th>
      <th width=6%>
	Fecha Obs.
      </th>
      <th width=6%>
	Hora Obs.
      </th>
      <th width=4%>
	Filtro
      </th>
      <th width=5%>
	Tipo Img.
      </th>
      <th width=4%>
	T. Exp.
      </th>
      <th width=14%>
	Observatorio
      </th>
      <th width=35%>
	Ruta
      </th>
    </tr>
  </thead>
<?php
$archivos = array();
/*if (is_dir('sesion/') === false){
  mkdir('sesion/',0777);
}
$salida = fopen('sesion/fitsdb_' . session_id(),'w')*/;
while ($fila = $resultado->fetch_assoc())
{
  $filabuena = array_values($fila);
  echo "<tr>";
  $n = count($filabuena);
  for ($i=-1;$i<$n;$i++)
  {
	if($i == -1){
		echo "<td align='center'>";
		printf("<input type='checkbox' class='A' name='selector[]' checked value='%s'>",$filabuena[$n-1]);
		echo "</td>";
	}
	else{
		echo "<td>";
		echo $filabuena[$i];
		echo "</td>";
	}
  }
  echo "</tr>";
//  $archivo = str_replace('/home/pablo/proyectoBD/FitsDB/','',$filabuena[$n-1]);
//    $archivo = $filabuena[$n-1];
//   fwrite($salida,$archivo.PHP_EOL);
//   file_put_contents(,$archivo);
}
// fclose($salida);
// foreach($archivos as $linea){
// file_put_contents('sesion/fitsdb_' . session_id(),print_r($linea, TRUE));
// }

?>
</table>
</form>
</div>
<div id='autor'>
<p align='center'> 
<!--Autor: Juan Pablo Navarro Sánchez <br>-->
<b>FitsDB</b> se publica bajo licencia GPLv2. Código fuente en <A href='https://github.com/helfio/FitsDB'>Github.</A>
</p>
</div>
<?php

  
// Function limpieza($direccion){
// if (file_exists($direccion)){
//   $path = $direccion;
//     if ($handle = opendir($path)) {
//       while (false !== ($file = readdir($handle))) {
// 	  if ((time()-filectime($path.$file)) <= 86400) {
// 	    unlink($path.$file);
// 	  }
//       }
//     }
//   }
// }

function limpieza($path)
{
    if ((is_dir($path) === true) and ((time()-filemtime($path)) > 86400 ))
    {
        $files = array_diff(scandir($path), array('.', '..'));

        foreach ($files as $file)
        {
            limpieza(realpath($path) . '/' . $file);
        }

        return rmdir($path);
    }

    else if (is_file($path) === true)
    {
        return unlink($path);
    }

    return false;
}
?>


</body>
</html>

<html>
<meta charset="utf-8" /> 
<title>
FitsDB v0.1.1-1
</title>
<link href="prueba.css" rel="stylesheet" type="text/css">
<body>
<?php
/* creates a compressed zip file */
function create_zip($files = array(),$destination = '',$overwrite = false) {
	//if the zip file already exists and overwrite is false, return false
	if(file_exists($destination) && !$overwrite) { return false; }
	//vars
	$valid_files = array();
	//if files were passed in...
	if(is_array($files)) {
		//cycle through each file
		foreach($files as $file) {
			//make sure the file exists
			if(file_exists($file)) {
				$valid_files[] = $file;
			}
		}
	}
	//if we have good files...
	if(count($valid_files)) {
		//create the archive
		$zip = new ZipArchive();
		if($zip->open($destination,$overwrite ? ZIPARCHIVE::OVERWRITE : ZIPARCHIVE::CREATE) !== true) {
			return false;
		}
		//add the files
		foreach($valid_files as $file) {
			$zip->addFile($file,$file);
		}
		//debug
		//echo 'The zip archive contains ',$zip->numFiles,' files with a status of ',$zip->status;
		
		//close the zip -- done!
		$zip->close();
		
		//check to make sure the file exists
		return file_exists($destination);
	}
	else
	{
		return false;
	}
}
?>

<H1 align=center>Interfaz web de FitsDB</H1>

<form id="form1" name="form1" method="post" action="prueba.php" align="right">
  <table width="600" border="0" align="center">
  <tr>
    <td width="200">ID:</td>
    <td width="200">
      <input type="text" name="idnum" id="idnum" />
    </td>
  </tr>
  <tr>
    <td>Fecha de modificación:</td>
    <td>
      <input type="text" name="fecha_mod" id="fecha_mod" />
    </td>
  </tr>
  <tr>
    <td>Tipo de imagen:</td>
    <td>
      <input type="text" name="typeimg" id="idnum" />
    </td>
  </tr>
  <tr>
    <td>Nombre del objeto:</td>
    <td>
      <input type="text" name="nombre_obj" id="nombre_obj" />
    </td>
  </tr>
  <tr>
    <td>Fecha de la observación:</td>
    <td>
      <input type="text" name="fecha_obs" id="fecha_obs" />
    </td>
  </tr>
  <tr>
    <td>Hora de la observación:</td>
    <td>
      <input type="text" name="tiempo_obs" id="tiempo_obs" />
    </td>
  </tr>
    <tr>
    <td>Tiempo de exposición:</td>
    <td>
      <input type="text" name="exptime" id="exptime" />
    </td>
  </tr>
    <tr>
    <td>Observatorio:</td>
    <td>
      <input type="text" name="observatorio" id="observatorio" />
    </td>
  </tr>
    <tr>
    <td>Telescopio:</td>
    <td>
      <input type="text" name="telescopio" id="telescopio" />
    </td>
  </tr>
    <tr>
    <td>Instrumento:</td>
    <td>
      <input type="text" name="instrumento" id="instrumento" />
    </td>
  </tr>
    <tr>
    <td>Filtro:</td>
    <td>
      <input type="text" name="filtro" id="filtro" />
    </td>
  </tr>
  <tr><td> <br></td></tr>
  <tr>
    <td align='left'>
      <input type="submit" name="enviar" id="enviar" value="Enviar consulta" />
    </td>
    <td align='center'>
      <input type="reset" value="Limpiar formulario" />
    </td>
    <td align="right">
	<input type="submit" name="enviar" id="enviar" value="Enviar consulta" />
    </td>
  </tr>
</table>
</form>

<H2 align=center>Resultados</H2>
<table border=0 align=center width=1850 class='zebra'>
  <thead>
    <tr align=center>
      <br>
      <th width=1%>
	ID
      </th>
      <br>
      <th width=9%>
	Fecha Mod.
      </th>
      <br>
      <th width=5%>
	Tipo Img.
      </th>
      <br>
      <th width=9%>
	Nombre
      </th>
      <br>
      <th width=5%>
	Fecha Obs.
      </th>
      <br>
      <th width=4%>
	Tiempo Obs.
      </th>
      <br>
      <th width=2%>
	Exp.
      </th>
      <br>
      <th width=9%>
	Obs.
      </th>
      <br>
      <th width=6%>
	Tele.
      </th>
      <br>
      <th width=12%>
	Instr.
      </th>
      <br>
      <th width=4%>
	Filtro.
      </th>
      <br>
      <th width=50%>
	Ruta
      </th>
      <br>
    </tr>
  </thead>

<?php
//Recibir
$idnum = strip_tags($_POST['idnum']);
$fecha_mod = strip_tags($_POST['fecha_mod']);
$typeimg = strip_tags($_POST['typeimg']);
$nombre_obj= strip_tags($_POST['nombre_obj']);
$fecha_obs= strip_tags($_POST['fecha_obs']);
$tiempo_obs= strip_tags($_POST['tiempo_obs']);
$exptime= strip_tags($_POST['exptime']);
$observatorio= strip_tags($_POST['observatorio']);
$telescopio= strip_tags($_POST['telescopio']);
$instrumento= strip_tags($_POST['instrumento']);
$filtro= strip_tags($_POST['filtro']);



$prefijo = "SELECT id, moddate, imgtype, object, dateobs, timeobs, exptime, observatory, telescope, instrument, filter, rute FROM tablaobs";
$sufijo = '';


if (strlen($idnum) != 0) {
  $sufijo = $sufijo . sprintf(" id like '%%%s%%'",$idnum) ." and";
  }

if (strlen($fecha_mod) != 0) {
  $sufijo = $sufijo . sprintf(" moddate like '%%%s%%'",$fecha_mod) . " and";
  }

if (strlen($typeimg) != 0) {
  $sufijo = $sufijo . sprintf(" typeimg like '%%%s%%'",$typeimg) . " and";
  }
  
if (strlen($nombre_obj) != 0) {
  $sufijo = $sufijo . sprintf(" object like '%%%s%%'",$nombre_obj) . " and";
  }

if (strlen($fecha_obs) != 0) {
  $sufijo = $sufijo . sprintf(" dateobs like '%%%s%%'",$fecha_obs) . " and";
  }

if (strlen($tiempo_obs) != 0) {
  $sufijo = $sufijo . sprintf(" timeobs like '%%%s%%'",$tiempo_obs) . " and";
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

if ((strlen($idnum) != 0) || (strlen($fecha_mod) != 0) || (strlen($typeimg) != 0) || (strlen($nombre_obj) != 0) || (strlen($fecha_obs) != 0) || (strlen($tiempo_obs) != 0) || (strlen($observatorio) != 0) || (strlen($telescopio) != 0) || (strlen($instrumento) != 0) || (strlen($filtro) != 0)) {
  $montamos = $prefijo . " WHERE" . $sufijo;
  $peticion = preg_replace('/and$/', '', $montamos);
  }
else {
  $peticion = "SELECT id, moddate, imgtype, object, dateobs, timeobs, exptime, observatory, telescope, instrument, filter, rute FROM tablaobs WHERE DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= moddate ORDER BY dateobs DESC";
  }
echo "Se ejecuta la siguiente petición a la base de datos: \n" . $peticion;
  
  

$conexion = new mysqli("127.0.0.1", "pablo", "halconmilenario", "pruebasdb");

$resultado = $conexion->query($peticion);
$resultado -> data_seek(0);
$archivos = array();
while ($fila = $resultado->fetch_assoc())
{
  $filabuena = array_values($fila);
  echo "<tr>";
  $n = count($filabuena);
  for ($i=0;$i<$n;$i++)
  {
    echo "<td>";
    echo $filabuena[$i];
    echo "</td>";
  }
  echo "</tr>";
  $archivos[] = $filabuena[$n-1];
}
$archivosbuenos = array_values($archivos);
?>
</table>
<!--<form id="form2" name="form2" method="post" action="./fitsdb/archivosfits.zip" align="right">
// <?php
// $archivozip = create_zip($archivosbuenos, './fitsdb/archivosfits.zip');
// ?>
<input type="button" name="descarga" id="descarga" value="Descargar datos" onClick="window.location.href='./fitsdb/archivosfits.zip'" />
</form>-->

<?php 
if(isset($_POST['submit'])) { 
// foo(); 
$archivozip = create_zip($archivosbuenos, 'archivosfits.zip');
header("Cache-Control: public");
header("Content-Description: File Transfer");
header("Content-Disposition: attachment; filename=archivosfits");
header("Content-Type: application/zip");
header("Content-Transfer-Encoding: binary");
readfile('archivosfits.zip');
} 
?>

<form action="<?=$_SERVER['PHP_SELF'];?>" method="post"> 
<input type="submit" name="submit" value="Click Me"> 
</form> 

</body>
</html>
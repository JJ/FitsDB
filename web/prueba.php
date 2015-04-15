<html>
<meta charset="utf-8" /> 
<title>
FitsDB v0.1.1-1
</title>
<link href="prueba.css" rel="stylesheet" type="text/css">
<body>
<?php
session_start();
//error_reporting(E_ALL);
//ini_set('display_errors', true);
?>

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
    <td width=40%>ID:</td>
    <td width=60%>
      <input type="number" name="idnum" id="idnum" autofocus />
    </td>
  </tr>
  <tr>
    <td>Fecha de modificación:</td>
    <td>
<!--       <input type="text" name="fecha_mod" id="fecha_mod" /> -->
      <input type="date" name="fecha_mod1" style="width: 140px;"></input> a <input type="date" name="fecha_mod2" style="width: 140px;"></input>
    </td>
  </tr>
  <tr>
    <td>Tipo de imagen:</td>
    <td>
     <!-- <input type="text" name="typeimg" id="idnum" /> -->
	<input type="text" name="typeimg" list="listatipos" autocomplete/>
	<datalist id="listatipos">
	<option value="Bias">Bias</option>
	<option value="Flat">Flat</option>
	<option value="Science">Science</option>
</datalist>
    </td>
  </tr>
  <tr>
    <td>Nombre del objeto:</td>
    <td>
<!--       <input type="text" name="nombre_obj" id="nombre_obj" /> -->
	<input type="text" name="nombre_obj" list="listanombres_obj" autocomplete/>
	<datalist id="listanombres_obj">
	<option value="Varuna">Varuna</option>
	<option value="Eris">Eris</option>
	<option value="Orcus">Orcus</option>
    </td>
  </tr>
  <tr>
    <td>Fecha de la observación:</td>
    <td>
<!--       <input type="text" name="fecha_obs" id="fecha_obs" /> -->
      <input type="date" name="fecha_obs1" style="width: 140px;"></input> a <input type="date" name="fecha_obs2" style="width: 140px;"></input>
    </td>
  </tr>
  <tr>
    <td>Hora de la observación:</td>
    <td>
<!--       <input type="text" name="tiempo_obs" id="tiempo_obs" /> -->
      <input type="time" name="tiempo_obs1" style="width: 140px;"></input> a <input type="time" name="tiempo_obs2" style="width: 140px;"></input>
    </td>
  </tr>
    <tr>
    <td>Tiempo de exposición:</td>
    <td>
      <input type="number" name="exptime1" id="exptime" step="10" style="width: 80px;" min="0"/> a <input type="number" name="exptime2" id="exptime" step="10" style="width: 80px;" min="0" />
    </td>
  </tr>
    <tr>
    <td>Observatorio:</td>
    <td>
<!--       <input type="text" name="observatorio" id="observatorio" /> -->
	<input type="text" name="observatorio" list="listaobservatorio" autocomplete/>
	<datalist id="listaobservatorio">
	<option value="OSN">OSN</option>
	<option value="DSAZ">DSAZ</option>
	<option value="CGG">CGG</option>
	<option value="Teide">Teide</option>
	<option value="Atacama">Atacama</option>
	<option value="IAC">IAC</option>
	<option value="la Hita">la Hita</option>
	<option value="lapalma">lapalma</option>
    </td>
  </tr>
    <tr>
    <td>Telescopio:</td>
    <td>
      <input type="text" name="telescopio" id="telescopio" autocomplete />
    </td>
  </tr>
    <tr>
    <td>Instrumento:</td>
    <td>
      <input type="text" name="instrumento" id="instrumento" autocomplete />
    </td>
  </tr>
    <tr>
    <td>Filtro:</td>
    <td>
      <input type="text" name="filtro" id="filtro" autocomplete />
    </td>
  </tr>
  <tr><td> <br></td></tr>
  <tr>
    <td align='left'>
      <input type="reset" value="Limpiar formulario" />

    </td>
    <td align='center'>
      <input type="submit" name="enviar" id="enviar" value="Enviar consulta" />

    </td>
    <td align="right">
	
    </td>
  </tr>
</table>
</form>
<H2 align=center>Resultados</H2>
<form id="form2" name="form2" method="get" action="download.php" align="right">
<input type="submit" class ="button" name="descargar" value="descargar" />
</form>

<?php
//Recibir
$idnum = strip_tags($_POST['idnum']);
$fecha_mod1 = strip_tags($_POST['fecha_mod1']);
$fecha_mod2 = strip_tags($_POST['fecha_mod2']);
$typeimg = strip_tags($_POST['typeimg']);
$nombre_obj= strip_tags($_POST['nombre_obj']);
$fecha_obs1= strip_tags($_POST['fecha_obs1']);
$fecha_obs2= strip_tags($_POST['fecha_obs2']);
$tiempo_obs1= strip_tags($_POST['tiempo_obs1']);
$tiempo_obs2= strip_tags($_POST['tiempo_obs2']);
$exptime1= strip_tags($_POST['exptime1']);
$exptime2= strip_tags($_POST['exptime2']);
$observatorio= strip_tags($_POST['observatorio']);
$telescopio= strip_tags($_POST['telescopio']);
$instrumento= strip_tags($_POST['instrumento']);
$filtro= strip_tags($_POST['filtro']);







$prefijo = "SELECT id, moddate, imgtype, object, dateobs, timeobs, exptime, observatory, telescope, instrument, filter, rute FROM tablaobs";
$sufijo = '';


if (strlen($idnum) != 0) {
  $sufijo = $sufijo . sprintf(" id like '%%%s%%'",$idnum) ." and";
  }

if ((strlen($fecha_mod1) != 0) && (strlen($fecha_mod2) != 0)) {
  $sufijo = $sufijo . sprintf(" (moddate BETWEEN '%s' AND '%s')", $fecha_mod1, $fecha_mod2) . " and";
  }

if (strlen($typeimg) != 0) {
  $sufijo = $sufijo . sprintf(" imgtype like '%%%s%%'",$typeimg) . " and";
  }

if (strlen($nombre_obj) != 0) {
  $sufijo = $sufijo . sprintf(" object like '%%%s%%'",$nombre_obj) . " and";
  }

if ((strlen($fecha_obs1) != 0) && (strlen($fecha_obs2) != 0)) {
  $sufijo = $sufijo . sprintf(" (dateobs BETWEEN '%s' AND '%s')", $fecha_obs1, $fecha_obs2) . " and";
  }

if ((strlen($tiempo_obs1) != 0) && (strlen($tiempo_obs2) != 0)) {
  $sufijo = $sufijo . sprintf(" (timeobs BETWEEN '%s' AND '%s')", $tiempo_obs1, $tiempo_obs2) . " and";
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

if ((strlen($idnum) != 0) || (strlen($fecha_mod1) != 0) || (strlen($fecha_mod2) != 0) || (strlen($typeimg) != 0) || (strlen($nombre_obj) != 0) || (strlen($fecha_obs1) != 0) || (strlen($fecha_obs2) != 0) || (strlen($tiempo_obs1) != 0) || (strlen($tiempo_obs2) != 0) ||(strlen($exptime1) != 0) ||(strlen($exptime2) != 0) || (strlen($observatorio) != 0) || (strlen($telescopio) != 0) || (strlen($instrumento) != 0) || (strlen($filtro) != 0)) {
  $montamos = $prefijo . " WHERE" . $sufijo;
  $peticion = preg_replace('/and$/', '', $montamos);
  echo "<table width='500' align='left'><tr><td>Se muestra la siguiente petición:</td><td> </td></tr>";
  echo "<tr><td>ID:</td><td>" . $idnum . "</td></tr>";
  echo "<tr><td>Modificado entre:</td><td>" . $fecha_mod1 . " y " . $fecha_mod2 . "</td></tr>";
  echo "<tr><td>Tipo de de imagen:</td><td>" . $typeimg . "</td></tr>";
  echo "<tr><td>Nombre del objeto:</td><td>" . $nombre_obj . "</td></tr>";
  echo "<tr><td>Fecha de observación entre:</td><td>" . $fecha_obs1 . " y " . $fecha_obs2 . "</td></tr>";
  echo "<tr><td>Hora de la observación entre:</td><td>" . $tiempo_obs1 . " y " . $tiempo_obs2 . "</td></tr>";
  echo "<tr><td>Tiempo de exposición entre:</td><td>" . $exptime1 . " y " . $exptime2 . "</td></tr>";
  echo "<tr><td>Observatorio:</td><td>" . $observatorio . "</td></tr>";
  echo "<tr><td>Telescopio:</td><td>" . $telescopio . "</td></tr>";
  echo "<tr><td>Instrumento:</td><td>" . $instrumento . "</td></tr>";
  echo "<tr><td>Filtro:</td><td>" . $filtro . "</td></tr>";  
  echo "</table>";
  echo "<br>";
  }
else {
  $peticion = "SELECT id, moddate, imgtype, object, dateobs, timeobs, exptime, observatory, telescope, instrument, filter, rute FROM tablaobs WHERE DATE_SUB(CURDATE(), INTERVAL 31 DAY) <= dateobs ORDER BY dateobs DESC";
  echo "<p>Se muestran las observaciones realizadas en los últimos 31 días.</p>";
  }

  
  

$conexion = new mysqli("127.0.0.1", "pablo", "halconmilenario", "pruebasdb");

$resultado = $conexion->query($peticion);
$resultado -> data_seek(0);
$archivos = array();
?>
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
$archivosbuenos = array();
$archivosbuenos = array_values($archivos);
file_put_contents('sesion/fitsdb_' . session_id(),print_r($archivosbuenos, TRUE));

?>
</table>


<?php
if(isset($_GET['descargar'])){
	descargar();
	/*$archivosbuenos = array_values($archivos);
        $m = count($archivos);
        echo $m;
        for ($j=0;$j<$m;$j++){
  echo $archivosbuenos[$j];// . "<br>";
}*/
        
    }

function descargar(){
// echo "<H1>hola!!</H1>";
$files = file('sesion/fitsdb_' . session_id());
$m = count($files);
// foreach ($files as $ey){
// echo $ey;
// }
echo "<H1>hola2!!</H1>";
// for ($j=0;$j<$m;$j++)
// {
//   echo $files[$j];// . "<br>";
// }
// echo "<H1>hola3!!</H1>";
// $zipname = 'archivosfits.zip';
// $zip = new ZipArchive;
// $zip->open($zipname, ZipArchive::OVERWRITE);
// if (is_array($files)){
// foreach ($files as $file) {
//   echo $file;
//   $zip->addFile($file);
// }
// }
// $zip->close();

//Then download the zipped file.
// header('Content-Type: application/zip');
// header('Content-disposition: attachment; filename='.$zipname);
// header('Content-Length: ' . filesize($zipname));
// readfile($zipname);
}
?>


</body>
</html>

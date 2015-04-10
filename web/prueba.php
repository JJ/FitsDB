<html>
<title>
FitsDB v0.1.1-1
</title>
<link href="prueba.css" rel="stylesheet" type="text/css">
<body>
<form id="form1" name="form1" method="post" action="index.php" align="right">
  <table width="500" border="1" align="center">
  <tr>
    <td width="200">Nombre del objeto:</td>
    <td width="300">
      <label for="nombre"></label>
      <input type="text" value="Eris" name="nombre" id="nombre" />

    </td>
  </tr>
  <tr>
    <td>Nick:</td>
    <td><label for="nick"></label>
    <input type="text" name="nick" id="nick" /></td>
  </tr>
  <tr>
    <td><input type="reset" value="Limpiar formulario" /></td>
    <td align="right">
    <input type="submit" name="enviar" id="enviar" value="Enviar consulta" />
    </td>
  </tr>
</table>
</form>

<H1 align=center>Resultados</H1>
<table border=0 align=center width=1250 class='zebra'>
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
      <th width=7%>
	Tipo Img.
      </th>
      <br>
      <th width=13%>
	Nombre
      </th>
      <br>
      <th width=8%>
	Fecha Obs.
      </th>
      <br>
      <th width=8%>
	Tiempo Obs.
      </th>
      <br>
      <th width=4%>
	Exp.
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
$idnum = strip_tags($_POST['id']);
$fecha_mod = strip_tags($_POST['fecha_mod']);
$typeimg = strip_tags($_POST['typeimp']);
$nombre_obj= strip_tags($_POST['nombre_obj']);
$fecha_obs= strip_tags($_POST['fecha_obs']);
$tiempo_obs= strip_tags($_POST['tiempo_obs']);
$exptime= strip_tags($_POST['exptime']);




$conexion = new mysqli("127.0.0.1", "pablo", "halconmilenario", "pruebasdb");
$peticion = "SELECT id, moddate, imgtype, object, dateobs, timeobs, exptime, rute FROM tablaobs Where";
$resultado = $conexion->query("SELECT id, moddate, imgtype, object, dateobs, timeobs, exptime, rute FROM tablaobs");
$resultado -> data_seek(0);
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
}
?>
</table>

</body>
</html>
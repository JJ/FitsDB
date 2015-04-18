<?php
session_start();
$files = array();
$files = file('sesion/fitsdb_' . session_id());

$zip = new ZipArchive(); // Aquí hay que especificar que es un TAR y esas cositas
if (!file_exists('descargas/')){
  mkdir('descargas/',0777);
  if(!file_exists(date('d'))){
    mkdir('descargas/' . date('d') ,0777);
  }
}
$path = 'descargas/' . date('d') . '/';
$num = 0;
$zipname = 'archivosfits' . $num . '.zip';

while (file_exists($path . $zipname)){
  $num++;
  $zipname = 'archivosfits' . $num . '.zip';
}

$zip->open($path . $zipname, ZipArchive::CREATE);
 foreach ($files as $file) {
 $bueno = trim($file);
  if (is_readable($bueno)){
    $zip->addFile($bueno);
  }
}

$zip->close();


header('Content-Type: application/zip');
header('Content-disposition: attachment; filename=' . $zipname);
//$size = filesize('archivosfits.zip');
//header('Content-Length: ' . $size);

readfile($path . $zipname);

?>

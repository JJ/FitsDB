
<?php
session_start();
//$files = file('sesion/fitsdb_' . session_id());
$files = array('23dec12_017.fit','prueba.php');
$zipname = 'archivosfits.zip';
$zip = new ZipArchive();
$zip->open($zipname, ZipArchive::CREATE);
foreach ($files as $file) {
  $zip->addFile($file);
}
$zip->close();


header('Content-Type: application/zip');
header('Content-disposition: attachment; filename=archivosfits.zip');
//$size = filesize('archivosfits.zip');
//header('Content-Length: ' . $size);

readfile('archivosfits.zip');

// $files = file('sesion/fitsdb_' . session_id());
// $m = count($files);
// echo $m . "<br>";
// foreach ($files as $ey){
// echo $ey;
// }
// echo $files[0];
?>


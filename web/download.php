
<?php
session_start();
$files = file('sesion/fitsdb_' . session_id());
$zipname = 'archivosfits.zip';
$zip = new ZipArchive;
$zip->open($zipname, ZipArchive::OVERWRITE);
foreach ($files as $file) {
  $zip->addFile($file);
}
$zip->close();


header('Content-Type: application/zip');
header('Content-disposition: attachment; filename=archivosfits.zip');
header('Content-Length: ' . filesize('archivosfits.zip'));
readfile('archivosfits.zip');

// $files = file('sesion/fitsdb_' . session_id());
// $m = count($files);
// echo $m . "<br>";
// foreach ($files as $ey){
// echo $ey;
// }
// echo $files[0];
?>


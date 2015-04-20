
<?php
// session_start();
// $files = array();
// $files = file('sesion/fitsdb_' . session_id());
// $files = array('23dec12_017.fit','ImagenesPrueba/2003EL61-010R.fit');

$files = ($_POST['selector']);
if (!file_exists('descargas/')){
  mkdir('descargas/',0777);
  if(!file_exists(date('d'))){
    mkdir('descargas/' . date('d') ,0777);
  }
}
$path = 'descargas/' . date('d') . '/';




if ($_POST['descargazip']){
  $zip = new ZipArchive();
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
      $lista = explode('/',$file);
      $p = 4; //Profundidad
      $n = count($lista);
      $nuevo = '';
      for ($j=$p;$j>0;$j--){
	$nuevo= $nuevo.$lista[$n-$j].'/';
      }
      $zip->addFile($bueno,$nuevo);
    }
  }
  $zip->close();
  header('Content-Type: application/zip');
  header('Content-disposition: attachment; filename=' . $zipname);
  //$size = filesize('archivosfits.zip');
  //header('Content-Length: ' . $size);

  readfile($path . $zipname);
}

// if ($_POST['descargatar']){
//   $num = 0;
//   $tarname = 'archivosfits' . $num . '.tar';
// 
//   while (file_exists($path . $tarname)){
//     $num++;
//     $tarname = 'archivosfits' . $num . '.tar';
//   }
//   $tar = new PharData($tarname);
//   foreach ($files as $file) {
//   $bueno = trim($file);
//     if (is_readable($bueno)){
//       $tar->addFile($bueno);
//     }
//   }
//   header('Content-Type: application/tar');
//   header('Content-disposition: attachment; filename=' . $tarname);
//   readfile($path . $tarname);
// }

?>


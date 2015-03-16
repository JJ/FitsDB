#!/bin/bash
dfits ImagenesPrueba/*.fits| grep -v "===" | tr " " "_" | tr "/" " " | tr "=" " " | awk '{print $1 " -> " $3}' | tr "_" " " > descripciones 
dfits ImagenesPrueba/*.fit| grep -v "===" | tr " " "_" | tr "/" " " | tr "=" " " | awk '{print $1 " -> " $3}' | tr "_" " " >> descripciones
dfits ImagenesPrueba/*.fts| grep -v "===" | tr " " "_" | tr "/" " " | tr "=" " " | awk '{print $1 " -> " $3}' | tr "_" " " >> descripciones
sort descripciones | uniq > descripciones_ordenadas
rm descripciones

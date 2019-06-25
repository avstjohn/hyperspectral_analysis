#! /bin/sh

##! /bin/bash
##for ((num=0; num<114 ; num++))

for num in $(seq 90 100)
do	
	python loadVNIR.py ../04-05/manual-$num/*.bil.hdr ../04-05/manual-$num/*.bil $num
#	python geotagJPG.py ../04-05/manual-$num/*.lcf rgb$num.jpg $num
done


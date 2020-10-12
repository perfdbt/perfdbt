#########################################################################
# File Name: split_c.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Thu 07 May 2020 04:31:15 AM EDT
#########################################################################
#!/bin/bash
file_num=0
rm -f c_auto/*
IFS='\n'
cat auto.c|while read -r line
do
	echo  "$line">>c_auto/auto_$file_num.c
	if [[ $line =~ "FILE" ]];then
		let file_num++
	fi
done

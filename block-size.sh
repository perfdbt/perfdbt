#########################################################################
# File Name: proc_log.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Tue Apr 28 15:04:27 2020
#########################################################################
#!/bin/bash
file=600.perlbench_s.asm
cur_size=0
cat $file|while read line
do
	if [ ${#line} -lt 2 ];then
		echo $cur_size
		cur_size=0
		continue
	fi
	let cur_size++
done

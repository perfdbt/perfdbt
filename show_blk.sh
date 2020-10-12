#########################################################################
# File Name: proc_log.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Tue Apr 28 15:04:27 2020
#########################################################################
#!/bin/bash
block_num=0
#file=600.perlbench_s.asm
file=605.mcf_s.asm
#file=625.x264_s.asm
#file=631.deepsjeng_s.asm
#file=648.exchange2_s.asm

line_count=0
cat $file|while read line
do
	if [ $1 -eq $block_num ];then
#		if [ ${#line} -lt 2 ];then
#			exit
#		fi
		echo $line_count
		echo $line
	fi

	if [ ${#line} -lt 2 ];then
		let block_num++
	fi
#	echo $block_num
	let line_count++
done

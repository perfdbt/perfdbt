#########################################################################
# File Name: exec-all.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Thu 07 May 2020 05:08:26 PM EDT
#########################################################################
#!/bin/bash
qemu_exec=""
if [[ $1 == "" ]];then
	qemu_exec="qemu-4.2.0"
else
	qemu_exec=$1
fi
#ls|grep run|while read line
ls|grep run_auto_|while read line
do
	echo $line
#	unbuffer time -p ~/qemu/$qemu_exec/aarch64-linux-user/qemu-aarch64 ./$line
#	perf stat -e LLC-load-misses -e LLC-loads ~/qemu/$qemu_exec/aarch64-linux-user/qemu-aarch64 ./$line
	
	perf stat -e cache-misses,cache-references,page-faults,branches,branch-misses ~/qemu/$qemu_exec/aarch64-linux-user/qemu-aarch64 ./$line
	perf stat -e dTLB-loads,dTLB-load-misses ~/qemu/$qemu_exec/aarch64-linux-user/qemu-aarch64 ./$line
	if [ $? -ne 0 ];then
		echo "Shell: Error!"
		exit
	fi
	echo ""
done

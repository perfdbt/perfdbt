#########################################################################
# File Name: test.a.out.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Wed 06 May 2020 02:57:57 AM EDT
#########################################################################
#!/bin/bash
count=0
loop_limit=1
while :
do
	echo ""
	echo "Round: $count"
	cat ~/qemu/versions.list|while read line
	do
		echo ""
		echo "$line"
		start=$(date +%s)
		time -p bash ./exec.sh "$line"
		end=$(date +%s)
		time=$(( $end - $start ))
		echo "EXEC: $time"
	done
	if [ $count -eq $loop_limit ];then
		exit
	fi
	let count++
done

#time ~/qemu/qemu-2.3.0/aarch64-linux-user/qemu-aarch64 ./a.out

#########################################################################
# File Name: test.a.out.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Wed 06 May 2020 02:57:57 AM EDT
#########################################################################
#!/bin/bash
count=0
while :
do
	echo ""
	echo "Round: $count"
	cat qemu.version|while read line
	do
		echo ""
		echo "$line"
		unbuffer time -p ~/qemu/$line/aarch64-linux-user/qemu-aarch64 ./a.out
	done
	if [ $count -eq 5 ];then
		exit
	fi
	let count++
done

#time ~/qemu/qemu-2.3.0/aarch64-linux-user/qemu-aarch64 ./a.out

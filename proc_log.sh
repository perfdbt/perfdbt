#########################################################################
# File Name: proc_log.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Tue Apr 28 15:04:27 2020
#########################################################################
#!/bin/bash
block_num=0
in_block=0
rm -rf /run/shm/hot_blk
mkdir /run/shm/hot_blk
rm -f $1.processed
cat $1|while read line
do
	if [ $in_block -eq 0 ];then
		echo $line|grep 'IN:' > /dev/null
		if [ $? -eq 0 ];then
			in_block=1
		fi
		continue
	else
		if [ "$line" = "" ];then
			in_block=0
			((block_num++))
		fi
		echo $line|awk '{$1="";$2="";print $0}' >> $1.processed
	fi
#	echo $block_num
done

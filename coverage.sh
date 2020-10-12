#########################################################################
# File Name: coverage.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Fri 12 Jun 2020 10:56:59 PM EDT
#########################################################################
#!/bin/bash
ls *.asm|while read line
do
	#echo $line
	#benchmark=`echo $line|awk -F. '{print $1.$2}'`
	#echo "FULL INSTRUCTIONS:"
	#full=`cat $line|grep -v -E '^$'|awk '{print $1}'|sort|uniq -c|sort -nr|head -n 5|awk '{print $2}'`
	full=`cat $line|grep -v -E '^$'|awk '{print $1}'|sort|uniq -c|sort -nr|wc -l`
	#echo "HOTTEST 2000 INSTRUCTIONS:"
	#hot=`./output_blk.sh 8000 "$line"|grep -v -E '^$'|awk '{print $1}'|sort|uniq -c|sort -nr|head -n 5|awk '{print $2}'`
	hot=`./output_blk.sh 8000 "$line"|grep -v -E '^$'|awk '{print $1}'|sort|uniq -c|sort -nr|wc -l`
	out=`awk 'BEGIN{printf "%.2f%\n",('$hot'/'$full')*100}'`
	echo $out
	continue
	echo 'FULL:'
	echo "$full"
	echo ""
	echo 'HOT:'
	echo "$hot"
	echo ""
done

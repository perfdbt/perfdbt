#########################################################################
# File Name: compile-all.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Thu 07 May 2020 04:59:25 PM EDT
#########################################################################
#!/bin/bash
rm -f run_auto*
ls ../c_auto|grep -E 'auto_0'|while read line
do
	echo $line
	echo $(echo $line | cut -d . -f1)
	aarch64-linux-gnu-gcc -O2  -o run_$(echo $line | cut -d . -f1) ../c_auto/$line -static 
	#aarch64-linux-gnu-gcc -g -O2 -o run_$(echo $line | cut -d . -f1) ../c_auto/$line -static 
done

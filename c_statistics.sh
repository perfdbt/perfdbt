#########################################################################
# File Name: c_statistics.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Sat 06 Jun 2020 02:08:21 PM EDT
#########################################################################
#!/bin/bash
malloc_objs=`cat auto.c |grep free|wc -l`
echo "malloc_objs: $malloc_objs"
cat auto.c |grep cur_malloc_size|awk '{print $2}'|awk '{sum+=$1} END {print "Average malloc size = ", sum/NR}'
cat auto.c |grep insert_list|head|awk '{print $2}'|awk '{sum+=$1} END {print "Average added inst = ", sum/NR}'
cat auto.c |grep all_reg_list_length|awk '{print $2}'|awk '{sum+=$1} END {print "Reg per block = ", sum/NR}'
blk_num=`cat auto.c |grep Block|awk '{print $2}'|tail -n 1`
echo "Block count: $blk_num"
loc=`cat auto.c |grep -v "//"|wc -l`
echo "lines of C file: $loc"
cat auto.c |grep instructions|awk '{print $2}'|awk '{sum+=$1} END {print "Average block size = ", sum/NR}'
mem_access=`cat auto.c |grep "\["|grep -v input|wc -l`
echo "mem access instructons: $mem_access"

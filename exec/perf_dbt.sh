#########################################################################
# File Name: get_rst.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Sat 23 May 2020 08:53:02 PM EDT
#########################################################################
#!/bin/bash
echo "run gen_mem_only"
cd ..;
echo "Generating mem only...";
time -p ./gen_mem_only.py >auto.c ;
./split_c.sh ;
cd -;
echo "Compiling mem only...";
./compile-all.sh;
echo "Executing mem only...";
./exec-all.sh >mem.log 2>&1;
echo "run gen_asm"

cd ..;
echo "Generating qps...";
time -p ./gen_asm.py >auto.c ;
./split_c.sh ;
cd -;
echo "Compiling qps...";
./compile-all.sh;
echo "Executing qps..."; 
./exec-all.sh >qps.log 2>&1;

echo ""
echo "Mem EXEC time:"
cat mem.log |grep tv_sum|awk '{print $3$6}'|sed 's/,/./'|tac
echo ""
echo "QPS EXEC time:"
cat qps.log |grep tv_sum|awk '{print $3$6}'|sed 's/,/./'|tac

#########################################################################
# File Name: code-analisys.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Wed 27 May 2020 06:56:59 PM EDT
#########################################################################
#!/bin/bash
cd ..;./gen_mem_only.py >auto.c ;./split_c.sh ;cd -;./compile-all.sh
echo "gen-mem-only:"
aarch64-linux-gnu-objdump -d run_auto_0|grep -Ev '^$|>:|Disassembly|\.word|\.\.\.|file format' |wc -l
cd ..;./gen_asm.py >auto.c ;./split_c.sh ;cd -;./compile-all.sh
echo "gen-asm:"
aarch64-linux-gnu-objdump -d run_auto_0|grep -Ev '^$|>:|Disassembly|\.word|\.\.\.|file format' |wc -l

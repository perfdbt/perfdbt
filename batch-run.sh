####################
#####################################################
# File Name: batch-run.sh
# Author: Jin Wu
# mail: jw0212@gmail.com
# Created Time: Thu 07 May 2020 02:57:05 AM EDT
#########################################################################
#!/bin/bash
./gen_asm.py >auto.c
time aarch64-linux-gnu-gcc auto.c -static
time ~/qemu/qemu-4.2.0/aarch64-linux-user/qemu-aarch64 ./a.out

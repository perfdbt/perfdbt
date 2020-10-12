#!/usr/bin/python
#benchmark="600.perlbench_s"
#benchmark="605.mcf_s"
#benchmark="625.x264_s"
#benchmark="631.deepsjeng_s"
#benchmark="641.leela_s"
#benchmark="648.exchange2_s"
benchmark="657.xz_s"
f_asm = open("%s.asm" % benchmark)
f_hotness = open("%s.hotness" % benchmark)
f_asm_new = open(("%s-new.asm" % benchmark), "w")
f_hotness_new  = open(("%s-new.hotness" % benchmark), "w")
asm_list = []
blk_size = 15
in_blk = False
while 1:
    line_asm = f_asm.readline()
    if not line_asm:
        break
    if len(line_asm) > 2:
        in_blk = True
        asm_list.append(line_asm)
    else:
        if not in_blk:
            continue
        #print '\n'.join(asm_list)
        line_hotness = int(f_hotness.readline())
        divided = [asm_list[i:i+blk_size] for i in range(0,len(asm_list),blk_size)]
        for sub_list in divided:
            #print ''.join(sub_list)
            f_asm_new.write(''.join(sub_list))
            f_asm_new.write('\n')
            f_hotness_new.write(str(line_hotness) + '\n')
        asm_list[:] = []
        in_blk = False
f_asm.close()
f_hotness.close()
f_asm_new.close()
f_hotness_new.close()



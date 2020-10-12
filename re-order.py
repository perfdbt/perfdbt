#!/usr/bin/python
import random
benchmark = "631.deepsjeng_s"
f_asm = open("%s.asm" % benchmark)
f_hotness = open(("%s.hotness") % benchmark)
f_asm_new = open(("test.asm"), "w")
f_hotness_new  = open(("test.hotness"), "w")
#f_asm_new = open(("%s-reorder.asm" % benchmark), "w")
#f_hotness_new  = open(("%s-reorder.hotness"  % benchmark), "w")
asm_list = []
blk_list = []
hotness_list = []
kv_blk_list = []
in_blk = False
blk_count = 0

class key_value:
    def __init__(self, key_in, value_in):
        self.key = key_in
        self.value = value_in

    def copy(self):
        return key_value(self.key, self.value)

    def p_key(self):
        print ''.join(self.key)

while blk_count < 2000:
    line_asm = f_asm.readline()
    if not line_asm:
        break
    if len(line_asm) > 2:
        in_blk = True
        asm_list.append(line_asm)
    else:
        if not in_blk:
            continue
        kv_blk_list.append(key_value(list(asm_list), f_hotness.readline()))
        asm_list[:] = []
        in_blk = False
        blk_count += 1
random.shuffle(kv_blk_list)
for i in reversed(range(len(kv_blk_list))):
#    print i
    f_asm_new.write(''.join(kv_blk_list[i].key))
    f_asm_new.write('\n')
    f_hotness_new.write(kv_blk_list[i].value)
f_asm.close()
f_hotness.close()
f_asm_new.close()
f_hotness_new.close()



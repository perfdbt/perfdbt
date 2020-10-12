#!/usr/bin/python
from __future__ import print_function
import re
import types
import random
from numpy import *
import gc as ggcc

class key_value:
    def __init__(self, key_in, value_in):
        self.key = key_in
        if value_in == '':
            value_in = '#1'
        if type(value_in) == type(1):
            self.value = value_in
        else:
            tmp = value_in.replace('#', '')
            self.value = int(value_in.replace('#', ''))


#    def get_last_index(self, kv_list):
#        for item in reversed(kvelist):
#            if item.key == self.key:
#                return kv_list.index(item)
#        return -1
#    @classmethod
    def get_last_index(self, kv_list):
        for item_index in range(len(kv_list)-1,-1,-1):
            if kv_list[item_index].key == self.key:
                return item_index
        return -1
    def get_first_index(self, kv_list):
        for item_index in range(len(kv_list)):
            if kv_list[item_index].key == self.key:
                return item_index
        return -1

    def key_in_list(self, kv_list):
        index = self.get_first_index(kv_list)
        if index == -1:
            return False
        else:
            return True

    def add_to_list_max(self, kv_list):
        index = self.get_last_index(kv_list)
        if index != -1:
            if self.value < 0:
                self.value = -1 * self.value
            if self.value > kv_list[index].value:
                kv_list[index].value = self.value
        else:
            kv_list.append(self.copy())
    def add_to_list(self, kv_list):
        kv_list.append(self.copy())
    def add_to_list_inc(self, kv_list):
        index = self.get_last_index(kv_list)
        if index != -1:
            kv_list[index].value += 1
        else:
            kv_list.append(self.copy())
    @classmethod
    def show_list(self, kv_list):
        if len(kv_list) == 0:
            print('Empty list!')
            return
        index = 0
        for i in kv_list:
            if index < 10:
                space = ' '
            else:
                space = ''
            print('[%d]%s "%s" : %d' % (index, space, i.key, i.value))
            index += 1
    def copy(self):
        return key_value(self.key, self.value)

class asm_operand:
    ext_ins = ('lsl', 'sxtw')
    def __init__(self, op_str):
        self.op = op_str
        self.base = '0'
        self.offset = '0'
        self.scale = '1'
        self.op_num = 1
        self.parse()
    def parse(self):
        if self.op == '':
            self.type = 'empty'
            return
        if ('[' in self.op):
            self.type = 'addr'
            op_addr = self.op
            op_addr = op_addr.replace('[', '')
            op_addr = op_addr.replace('] ', '').replace(']', '')
            op_addr = op_addr.replace('%', '')
            op_addr_elements = op_addr.split(', ')
            self.op_num = len(op_addr_elements)
            if self.op_num >= 1:
                self.base = op_addr_elements[0]
            if self.op_num >= 2:
                self.offset = op_addr_elements[1]
            if self.op_num >= 3:
                self.scale = op_addr_elements[2]
            self.addr_elements = []
            for i in op_addr_elements:
                ao_tmp = asm_operand(i.replace(' ', ''))
#                if 'input' in ao_tmp.op:
#                    print(ao_tmp.op)
                self.addr_elements.append(ao_tmp)
        elif self.op.split()[0] in asm_operand.ext_ins:
            self.type = 'ext'
        elif '#' in self.op or self.op.isdigit():
            self.type = 'num'
        elif 'input' in self.op:
            self.type = 'c_input'
        elif ('pc' in self.op):
            self.type = 'pc'
        else:
            self.op = self.op.replace(' ', '')
            self.type = 'reg'
    def is_addr(self):
#        print('"%s"' % self.op)
        return self.type == 'addr'
    def copy(self):
        return asm_operand(self.op)

class asm_arm:
#    instructions = ('mov', 'sub', 'ldr', 'add', 'smaddl', 'lsl', 'str', 'smull', 'cmp', 'nop', 'b.le', 'OUT:')
    instructions = []
    def __init__(self, instr_str):
        self.str = instr_str
        self.op_list = []
        self.src_list = []
        self.instr = ''
        self.reg_dist = ''
        self.reg_dist2 = 'None'
        self.addr_op_index = -1
        self.get_iset_arm()
        self.parse()
    def get_iset_arm(self):
        if len(asm_arm.instructions) != 0:
            return
        f = open('isa-arm.dat')
        line = f.readline().replace('\n', '')
        ins_list = []
        while line:
            asm_arm.instructions.append(line)
            line = f.readline().replace('\n', '')
        f.close()
    def copy(self):
        return asm_arm(self.str)
    def parse(self):
        ins_elements = self.str.split(', ')
#        print(ins_elements)
        op_tmp = ins_elements[0].split()
        if op_tmp[0] in self.instructions:#get instruction name here
            self.instr = op_tmp[0]
            op_tmp.remove(op_tmp[0])
            ins_elements.remove(ins_elements[0])
            ins_elements = op_tmp + ins_elements
            if len(op_tmp) > 0:
                self.reg_dist = op_tmp[0]
                if len(ins_elements) > 1:
                    self.reg_dist2 = ins_elements[1]
                join_flag = 0
                i = 0
                while 1:
                    cur_op = ins_elements[i]
#                    print(cur_op)
                    if join_flag == 1:
                        ins_elements[i-1] = ins_elements[i-1] + ', ' + ins_elements[i]
                        ins_elements.remove(ins_elements[i])
                    else:
                        i += 1
                    if ']' in cur_op:
                        join_flag = 0
                        self.addr_op_index = i
                    if i>=len(ins_elements):
                        break;
                    if '[' in cur_op:
                        join_flag = 1
        elif 'OUT' not in self.str:
            print(self.instr)
            print('Do not support instruction: %s' % self.str)
            exit()
        self.op_num = len(ins_elements)

        for i in range(len(ins_elements)):
            self.op_list.append(asm_operand(ins_elements[i]))
            if i > 0:
                self.src_list.append(asm_operand(ins_elements[i]))
    def get_addr_op_index(self):
        return self.addr_op_index
    def show(self):
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print('Assembly:')
        print('\t%s' % self.str)
        print('Number of operands:')
        print('\t%s' % self.op_num)
        print('Instruction:')
        print('\t%s' % self.instr)
        print('Destination:')
        print('\t%s' % self.reg_dist)
        print('Operands:')
        for i in self.op_list:
            print('\t%s <-- %s' % (i.op, i.type))
            if i.is_addr():
                print('\t\tBase: %s, offset: %s, scale: %s' % (i.base, i.offset, i.scale))
                for j in i.addr_elements:
                    print('\t\t%s <-- %s' % (j.op, j.type))
        print('--------------------------------')

    def get_reg_list(self):
        reg_list = []
        reg_list.append(self.reg_dist)
        for i in self.op_list:
            if i.type == 'reg':
                reg_list.append(i.op)
            elif i.is_addr():
                for j in i.addr_elements:
                    if j.type == 'reg':
                        reg_list.append(j.op)
        return reg_list


class asm_block:
    def __init__(self, file_path):
        self.dist_list = []
        self.dist_list2 = []
        self.src_reg_list = []
        self.base_reg_list = []
        self.offset_reg_list = []
        self.scale_reg_list = []
        self.dist_reg_cursor_list = []
        self.malloc_reg_list = []
        self.all_w_reg_list = []
        self.all_x_reg_list = []
        self.insert_list = []
        self.replacement_list = []
        self.block_num = 0
        self.hotness = 3
        self.offset_step = 1024
        #for statistics
#        self.malloc_size_list = []
        for i in range(0, 29):
            x_reg = ("x%d" % i)
            w_reg = ("w%d" % i)
            key_value(x_reg, 0).add_to_list(self.all_x_reg_list)
            key_value(w_reg, 0).add_to_list(self.all_w_reg_list)
        self.asm_list = []
        self.path = file_path
        if self.path == None:
            return
        f = open(file_path)
        line = f.readline()
        ins_list = []
        while line:
            line = re.sub(u"\\(.*?\\)", "", line).replace('\n', '') 
            ins_list.append(line.lstrip())
            line = f.readline()
        self.load_list(ins_list)
        f.close()

    def load_list(self, instruction_list):
        for i in instruction_list:
            self.asm_list.append(asm_arm(i))
        #put the following methods in order!
        self.gen_instrument()
        self.instrument_asm()
        self.scan_reg()
        self.replace29sp()
        self.gen_prep_mem()
        self.gen_free_mem()

    def asm_list_remove(self, index):
        self.asm_list.pop(index)

    def asm_list_insert(self, index, value):
        self.asm_list.insert(index, asm_arm(value))

    def insert_asm_kv(self, kv):
#        print('insert "%s" to %d' % (kv.key, kv.value))
#        print 'kv.value:'
#        print kv.value
#        print 'len:'
#        print len(self.asm_list)
        if kv.value >= len(self.asm_list):
#            print 'XXXXXXXXXXXX'
#            print kv.key
            self.asm_list.append(asm_arm(kv.key))
        else:
            self.asm_list.insert(kv.value, asm_arm(kv.key))

    def show(self):
        for i in self.asm_list:
            i.show()

#    def copy(self):
#        return asm_block(self.path)

    def print_asm(self):
        for asm in self.asm_list:
#            if 'fmov' in asm.str:
#                print('xxxxxxxx')
#                continue
            ########## DO NOT SUPPORT BSL ###########
            if 'bsl' in asm.str or ('.' in asm.str and 'v' in asm.str and ('fmov' not in asm.str)):
                print('\t\t"nop\\n\\t"')
                continue
            if 'dc zva' in asm.str:
                print('\t\t"nop\\n\\t"')
                continue
            ########## DO NOT SUPPORT mrs AND msr ###########
#            if 'mrs' in asm.str or ('msr' in asm.str):
#                continue
            ########## DO NOT SUPPORT pc ###########
#            if 'pc' in asm.str:
#                continue
            ########## DO NOT SUPPORT fmov ###########
            print('\t\t"%s\\n\\t"' % (asm.str))

    def gen_prep_mem(self):
        ret_list=[]
        for item in self.malloc_reg_list:
            ######## DO NOT SUPPORT VECTORS ##########
            if '.' in item.key or 'v' in item.key:
                continue
        #    ret_list.append('\t//Block_num: %d' % self.block_num)
            malloc_str = ('\tlong *ptr_%s_%d = malloc(sizeof(long) * %d);\n' % (item.key, self.block_num, item.value)) \
                    + ('\tlong *ptr_%s_%d_in = ptr_%s_%d;\n' % (item.key, self.block_num, item.key, self.block_num)) 
#                    + ('\tfor(int i = 0; i < %d; i++)\n\t{\n\t\tptr_%s_%d[i] = rand();\n\t}\n' % (item.value, item.key, self.block_num))
            ret_list.append(malloc_str)
#            print('\tlong *ptr_%s_%d = malloc(sizeof(long) * %d);' % (item.key, self.block_num, item.value))
#            print('\tfor(int i = 0; i < %d; i++)\n\t{\n\t\tptr_%s_%d[i] = rand();\n\t}' % (item.value, item.key, self.block_num))
#        print('')
        gen_code.add_gen_malloc(ret_list)

    def gen_free_mem(self):
        ret_list=[]
        for item in self.malloc_reg_list:
            ######## DO NOT SUPPORT VECTORS ##########
            if '.' in item.key or 'v' in item.key:
                continue
        #    ret_list.append('\t//Block_num: %d' % self.block_num)
            ret_list.append('\tfree(ptr_%s_%d);' % (item.key, self.block_num))
        gen_code.add_gen_free(ret_list)
#            print('\tfree(ptr_%s_%d);' % (item.key, self.block_num))

    def find_next_dist_reg(self, dist, index):
        for i in range(len(self.asm_list)):
            if self.asm_list[i].reg_dist == dist and i >= index:
                return i

    def find_next_base_reg(self, base, index):
        for i in range(len(self.asm_list)):
            for op in self.asm_list[i].op_list:
                if op.is_addr():
#                    print op.base
                    if base == op.base and i >= index:
                        return i

    def find_next_offset_reg(self, offset, index):
        for i in range(len(self.asm_list)):
            for op in self.asm_list[i].op_list:
                if op.is_addr():
#                    print op.offset
                    if offset == op.offset and i >= index:
                        return i

    def add_to_all_reg_list(self, kv):
        if 'zr' in kv.key:
            return
        if 'x' in kv.key and '#' not in kv.key:
            kv.add_to_list_inc(self.all_x_reg_list)
        elif 'w' in kv.key:
            kv.add_to_list_inc(self.all_w_reg_list)

        #for statistics
#    def get_all_reg_list_len(self, kv_list):
#        length = 0
#        for item in kv_list:
#            if item.value != 0:
#                length += 1
#        return length

    def scan_reg(self):
#        print('scan_reg:')
        self.dist_list = []
        self.dist_list2 = []
        for asm in self.asm_list:
#            print(asm.str)
            if 'b.' in asm.instr or 'bl' in asm.instr:
                break
            if 'stp' in asm.instr or 'ldp' in asm.instr:
                key_value(asm_operand(asm.reg_dist2).op, '-1').add_to_list(self.dist_list2)
            if asm.reg_dist != '' and 'OUT' not in asm.reg_dist:
                kv_reg_dist = key_value(asm_operand(asm.reg_dist).op, '-1')
                kv_reg_dist.add_to_list(self.dist_list)
                kv_reg_dist.value = 1
                self.add_to_all_reg_list(kv_reg_dist)
            for op in asm.src_list:
                if op.is_addr():
#                    print('op.is_addr():')
                    if asm_operand(op.base).type == 'reg':
                        reg_base = key_value(op.base, '-1')
                        reg_base.add_to_list(self.base_reg_list)
                        reg_base.value = 1
#                        print(reg_base.key)
                        self.add_to_all_reg_list(reg_base)
                        reg_base.add_to_list_inc(self.src_reg_list)
                    if asm_operand(op.offset).type == 'reg':
                        reg_offset = key_value(op.offset, '-1')
                        reg_offset.add_to_list(self.offset_reg_list)
                        reg_offset.value = 1
#                        print(reg_offset.key)
                        self.add_to_all_reg_list(reg_offset)
                        reg_offset.add_to_list_inc(self.src_reg_list)
                    if asm_operand(op.scale).type == 'reg':
                        reg_scale = key_value(op.scale, '-1')
                        reg_scale.add_to_list(self.scale_reg_list)
                        reg_scale.value = 1
#                        print(reg_scale.key)
                        self.add_to_all_reg_list(reg_scale)
                        reg_scale.add_to_list_inc(self.src_reg_list)
                else:
                    if op.type == 'reg':
#                        print('reg_src')
                        reg_src = key_value(op.op, '1')
#                        print(reg_src.key)
                        self.add_to_all_reg_list(reg_src)
                        reg_src.add_to_list(self.scale_reg_list)
                        reg_src.add_to_list_inc(self.src_reg_list)
#                key_value.show_list(self.all_reg_list)
#                key_value.show_list(self.src_reg_list)
#        key_value.show_list(self.all_x_reg_list)
#        key_value.show_list(self.all_w_reg_list)


        #for statistics
        #print('//all_reg_list_length: %d' % (self.get_all_reg_list_len(self.all_x_reg_list) + self.get_all_reg_list_len(self.all_w_reg_list)))

    def find_replacement(self):
        for i in reversed(range(0, 29)):
            if self.all_x_reg_list[i].value == 0 and self.all_w_reg_list[i].value == 0:
                if i in self.replacement_list:
                    continue
                else:
                    self.replacement_list.append(i)
                    return i
        print(self.block_num)
        print('No alternitave registers available!')
        exit()
        return -1

    def replace29_str(self, asm_str, rep_index_29, rep_index_sp):
        replace_start = ('[', 'input_', ' ')
        replace_end = (',', ']', '_', ' ')
        replace_width = ('x', 'w')
        ret = asm_str
        #turn pc+123 to [sp] first
        if 'pc+' in asm_str:
            op_pc = ret.split()[2]
            ret = ret.replace(op_pc, '[sp]')
        for start in replace_start:
            for end in replace_end:
                for width in replace_width:
                    before_29 = ('%s%s29%s' % (start, width, end))
                    after_29 = ('%s%s%d%s' % (start, width, rep_index_29, end))
                    ret = ret.replace(before_29, after_29)
                before_sp = ('%ssp%s' % (start, end))
                after_sp = ('%s%s%d%s' % (start, 'x', rep_index_sp, end))
                ret = ret.replace(before_sp, after_sp)
        return ret

    def is_gp_reg(self, reg_str):
        if (len(reg_str) < 2) or (len(reg_str) > 3):
            return False
        if (reg_str[0] != 'x') and (reg_str[0] != 'w'):
            return False
        if reg_str[1:].isdigit():
            if int(reg_str[1:]) == 29:
                return False
            else:
                return True
        return False
    def replace_nzcv(self, instr_in):
        if '#' in instr_in and ('v' in instr_in or 'V' in instr_in):
            nzcv_to_num = random.randint(0, 15)
            return re.sub('nzcv', str(nzcv_to_num), instr_in, flags=re.IGNORECASE)
        else:
            return instr_in

    #replace registers x29, w29 and sp with unused registers
    #replace register reg_used, with a used dist register
    #replace wzr and xzr with gp regs
    #replace #nzcv with number
    def replace29sp(self):
#        self.show()
        rep29 = self.find_replacement()
        rep_sp = self.find_replacement()
        rep_zr = '7'
        rep_ret = ''
        for dist in self.all_x_reg_list:
            if dist.key != 'x29' \
                    and self.reg_num_in_list(dist, self.dist_reg_cursor_list) == -1 \
                    and dist.key != rep29 and dist.key != rep_sp:
                        rep_ret = dist.key
                        break

        if len(rep_ret) == 0:
            print('rep_ret: lenth = 0')
            exit()

        for asm_index in range(len(self.asm_list)):
            ##for replace xzr and wzr, DO NOT use regs that affect malloced ptrs
            #regs is reg set of this line of instruction
            regs = self.asm_list[asm_index].get_reg_list()
            for reg_index in range(len(regs)-1, -1, -1):
                kv_tmp = key_value(regs[reg_index], 0)
                #only keep x regs and w regs, others will be popped out of the list
                if not ((kv_tmp.key_in_list(self.all_x_reg_list)) or (kv_tmp.key_in_list(self.all_w_reg_list))):
                    regs.pop(reg_index)
                else:
                    #remove x and w, only keep reg number
                    regs[reg_index] = regs[reg_index].replace('x', '').replace('w', '')
#            key_value.show_list(self.dist_list)
            #we need to find a reg in dist_list but not in self.dist_reg_cursor_list
            for dist in self.dist_list:
                if not self.is_gp_reg(dist.key):
                    continue
                if dist.key.replace('x', '').replace('w', '') not in regs:
                    if self.reg_num_in_list(key_value(dist.key, -1), self.dist_reg_cursor_list) != -1:
                        continue
                    rep_zr = dist.key.replace('x', '').replace('w', '')
                    break
            ##end of for replace xzr and wzr
            replaced = self.replace29_str(self.asm_list[asm_index].str, rep29, rep_sp).replace('reg_used', rep_ret)
            #replace unsupported zero register with a used register
            replaced = replaced.replace('wzr', ('w%s' % rep_zr)).replace('xzr', ('x%s' % rep_zr))
            replaced = self.replace_nzcv(replaced)
            #replace negtive values with positive ones
            if '#' in replaced and ('0x' not in replaced):
                replaced_element_list = replaced.split()
                for i in range(len(replaced_element_list)):
                    if '#' in replaced_element_list[i] and ('0.0' not in replaced_element_list[i]):
                        num = int(replaced_element_list[i].replace('#', '')
                                .replace(',', '').replace(']', '').replace('[', '').replace('!', ''))
                        if num <= -255 and (('ldur' in replaced) or ('stur' in replaced)):
                            num += 2
                        if num < 0:
                            num *= -1
                        new_item = '#' + str(num)
                        if (',' in replaced_element_list[i]):
                            new_item = new_item + ','
                        if ('[' in replaced_element_list[i]):
                            new_item = '[' + new_item
                        if ('!]' in replaced_element_list[i]):
                            new_item = new_item + '!]'
                        elif (']!' in replaced_element_list[i]):
                            new_item = new_item + ']!'
                        elif (']' in replaced_element_list[i]):
                            new_item = new_item + ']'
                        replaced_element_list[i] = new_item
                replaced = ' '.join(replaced_element_list)
                #print(replaced)
            #replaced = replaced.replace('#-', '#')
            if replaced != self.asm_list[asm_index].str:
                self.asm_list[asm_index] = asm_arm(replaced)
        for kv_reg in self.malloc_reg_list:
            kv_reg.key = kv_reg.key.replace('29', str(rep29))
            kv_reg.key = kv_reg.key.replace('sp', ('x%s' % str(rep_sp)))
        for kv_reg in self.dist_list:
            kv_reg.key = kv_reg.key.replace('29', str(rep29))
            kv_reg.key = kv_reg.key.replace('sp', ('x%s' % str(rep_sp)))
            kv_reg.key = kv_reg.key.replace('reg_used', rep_ret).replace('wzr', ('w%s' % rep_zr)).replace('xzr', ('x%s' % rep_zr))
        for kv_reg in self.dist_list2:
            kv_reg.key = kv_reg.key.replace('29', str(rep29))
            kv_reg.key = kv_reg.key.replace('sp', ('x%s' % str(rep_sp)))
            kv_reg.key = kv_reg.key.replace('reg_used', rep_ret).replace('wzr', ('w%s' % rep_zr)).replace('xzr', ('x%s' % rep_zr))
        for kv_reg in self.dist_reg_cursor_list:
            kv_reg.key = kv_reg.key.replace('29', str(rep29))
            kv_reg.key = kv_reg.key.replace('sp', ('x%s' % str(rep_sp)))
            kv_reg.key = kv_reg.key.replace('reg_used', rep_ret).replace('wzr', ('w%s' % rep_zr)).replace('xzr', ('x%s' % rep_zr))

    def instrument_asm(self):
        #for statistics
        #print('//insert_list.length: %d' % len(self.insert_list))
        for item in reversed(self.insert_list):
            self.insert_asm_kv(item)

    def scale_to_num(self, scale_str):
        if 'lsl #' in scale_str:
            return pow(2, int(scale_str.replace('lsl #', '')))
        elif 'sxt' in scale_str:
            item_list = scale_str.split()
            if len(item_list) == 1:
                return 1
            return int(item_list[1].replace('#', ''))
        elif scale_str.isdigit():
            return int(scale_str)
        else: 
            print('//not supported scale: %s' % scale_str)
            exit()
            return -1

    def get_rand_offset(self):
        return random.randint(1, 1023)

    def get_malloc_size(self, offset, scale):
        if offset < 0:
            offset = -1 * offset
        return (offset + 64) * scale

    def gen_instrument(self):
        adrp_handled = False
        for asm_index in range(len(self.asm_list)):
            #print('')
            #print(self.asm_list[asm_index].str)
            #instrument ret instruction:
            cur_instr = self.asm_list[asm_index].instr
            if cur_instr == 'ret':
                ble_ins_str = ('ldr reg_used, =OUT_RET_%d' % self.block_num)
                #replace b.le #+0x2b40 with b.le OUT
                self.asm_list_insert(asm_index, ble_ins_str)
                self.asm_list_remove(asm_index + 1)
                ins_kv_out = key_value('br reg_used', asm_index + 1)
                self.insert_list.append(ins_kv_out)
                ins_kv_nop = key_value(('mov x17, #0xfffff'), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value((('OUT_RET_%d:') % self.block_num), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value('nop', asm_index + 1)
                self.insert_list.append(ins_kv_nop)
            elif cur_instr == 'br' or cur_instr == 'blr':
                ble_ins_str = ('ldr reg_used, =OUT_%d' % self.block_num)
                self.asm_list_insert(asm_index, ble_ins_str)
                self.asm_list_remove(asm_index + 1)
                ins_kv_out = key_value(('%s reg_used' % cur_instr), asm_index + 1)
                self.insert_list.append(ins_kv_out)
                ins_kv_nop = key_value(('mov x17, #0xfffff'), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value(('OUT_%d:' % self.block_num), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value('nop', asm_index + 1)
                self.insert_list.append(ins_kv_nop)
            elif cur_instr == 'adrp' or cur_instr == 'adr':
                ble_ins_str = ('%s reg_used, OUT_ADRP_%d' % (cur_instr, self.block_num))
                self.asm_list_insert(asm_index, ble_ins_str)
                self.asm_list_remove(asm_index + 1)
                if not adrp_handled:
                    ins_kv_nop = key_value(('mov x17, #0xfffff'), asm_index + 1)
                    self.insert_list.append(ins_kv_nop)
                    ins_kv_nop = key_value(('OUT_ADRP_%d:' % self.block_num), asm_index + 1)
                    self.insert_list.append(ins_kv_nop)
                    adrp_handled = True
            elif cur_instr == 'tbz' or cur_instr == 'tbnz':
                instr_list = self.asm_list[asm_index].str.split()
                instr_list[3] = ('OUT_TBZ_%d' % self.block_num)
                ble_ins_str = ' '.join(instr_list)
                self.asm_list_insert(asm_index, ble_ins_str)
                self.asm_list_remove(asm_index + 1)
                ins_kv_nop = key_value(('mov x17, #0xfffff'), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value(('OUT_TBZ_%d:' % self.block_num), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value('nop', asm_index + 1)
                self.insert_list.append(ins_kv_nop)
            elif cur_instr == 'cbz' or cur_instr == 'cbnz':
                instr_list = self.asm_list[asm_index].str.split()
                instr_list[2] = ('OUT_CBZ_%d' % self.block_num)
                ble_ins_str = ' '.join(instr_list)
                self.asm_list_insert(asm_index, ble_ins_str)
                self.asm_list_remove(asm_index + 1)
                ins_kv_nop = key_value(('mov x17, #0xfffff'), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value(('OUT_CBZ_%d:' % self.block_num), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value('nop', asm_index + 1)
                self.insert_list.append(ins_kv_nop)
            elif cur_instr == 'bl' or cur_instr == 'b':
                ble_ins_str = ('%s OUT_BL_%d' % (cur_instr, self.block_num))
                self.asm_list_insert(asm_index, ble_ins_str)
                self.asm_list_remove(asm_index + 1)
                ins_kv_nop = key_value(('mov x17, #0xfffff'), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value(('OUT_BL_%d:' % self.block_num), asm_index + 1)
                self.insert_list.append(ins_kv_nop)
                ins_kv_nop = key_value('nop', asm_index + 1)
                self.insert_list.append(ins_kv_nop)
            elif '#' in (self.asm_list[asm_index].str) and cur_instr == 'fmov':
                #and ('#' in cur_instr):
                cur_instr_list = self.asm_list[asm_index].str.split()
                fmov_op_float = cur_instr_list[2]
                cur_instr_list[2] = '1.0e+1'
                ble_ins_str = ' '.join(cur_instr_list)
                self.asm_list_insert(asm_index, ble_ins_str)
                self.asm_list_remove(asm_index + 1)
#            elif cur_instr == 'ldp' or cur_instr == 'stp':#they have 2 dist ops
#                reg_dist2 = key_value(asm_operand(self.asm_list[asm_index].reg_dist2).op, '-1')
#                reg_dist2.add_to_list(self.dist_list2)

            kv_reg_dist = key_value(asm_operand(self.asm_list[asm_index].reg_dist2).op, '-1')
            kv_reg_dist.add_to_list(self.dist_list2)

            kv_reg_dist = key_value(asm_operand(self.asm_list[asm_index].reg_dist).op, '-1')
            kv_reg_dist.add_to_list(self.dist_list)
            for op in self.asm_list[asm_index].op_list:
                #asign value for addr regs
                base_val = 0
                offset_val = 0
                scale_val = 1
                if op.is_addr():
                    #print('xxxxxx\nbase = %s, offset = %s, scale = %s' % (op.base, op.offset, op.scale))
                    addr_op_list = []
                    base_type = asm_operand(op.base).type
                    offset_type = asm_operand(op.offset).type
                    scale_type = asm_operand(op.scale).type
                    if base_type == 'reg':
                        addr_op_list.append(op.base)
                    if offset_type == 'reg':
                        addr_op_list.append(op.offset)
                        offset_val = self.get_rand_offset()
                    elif offset_type == 'num':
                        offset_val = int(op.offset.replace('#', '').replace('!', ''))
                    if scale_type == 'reg':
                        print('//Not support scale of reg')
#                        exit()
                    elif scale_type == 'ext':
                        scale_val = self.scale_to_num(op.scale)
                    #print('base.val = %s, offset.val = %s, scale.val = %s' % (base_val, offset_val, scale_val))
                    cur_malloc_size = self.get_malloc_size(offset_val, scale_val)
#                    print cur_malloc_size
                    if cur_malloc_size != 0:
                        #add more pages to produce cache miss

        #for statistics
        #                print('//cur_malloc_size: %d'  % cur_malloc_size)
        #                self.malloc_size_list.append(cur_malloc_size)
                        kv_tmp = key_value(op.base, cur_malloc_size + 1024*1024)
                        kv_tmp.add_to_list_max(self.malloc_reg_list)

                    #self.dist_list: dist registers
                    #self.dist_reg_cursor_list: last index value seen of a certain src register
                    count = 0
                    for op_str in addr_op_list:
                        #print(op_str)
                        if count == 0:
                            cur_type = 'base'
                            reg_value = ('%%[input_%s_%d]' % (op.base, self.block_num))
                        elif count == 1:
                            cur_type = 'offset'
                            reg_value = ('#%d' % offset_val)
                        elif count == 2:
                            cur_type = 'scale'
                            print('ERROR: scale not supported!')
                        count += 1
                        if cur_type == 'offset':
                            ins_str = ('mov %s, %s' % (op_str, reg_value))
                            ins_kv = key_value(ins_str, asm_index)
                            ins_kv.add_to_list(self.insert_list)
                            continue
                        handled = False
                        kv_tmp = key_value(op_str, -1)
                        #key_value.show_list(self.dist_reg_cursor_list)
                        #last_index = kv_tmp.get_first_index(self.dist_reg_cursor_list)
                        last_index = self.reg_num_in_list(kv_tmp, self.dist_reg_cursor_list)
                        if last_index != -1:
                            #print('no insert')
                            last_index = self.dist_reg_cursor_list[last_index].value
                        else:
                            ins_str = ('mov %s, %s' % (op_str, reg_value))
                            #print('insert:')
                            #print(ins_str)
                            ins_kv = key_value(ins_str, asm_index)
                            ins_kv.add_to_list(self.insert_list)
                            handled = True
#                        list_tmp = self.dist_list[(last_index + 1):asm_index]
                        #base_index: shows if the dist_reg was modified between last seen and current asm
#                        base_index = kv_tmp.get_first_index(self.dist_list[(last_index):asm_index])
                        #print('\nsdfwegeawfw')
                        #print(self.asm_list[asm_index].str)
                        #print(op_str)
                        #key_value.show_list(self.dist_list[(last_index):asm_index])
                        reg_modified = self.reg_num_in_list(kv_tmp, self.dist_list[(last_index):asm_index])
                        #print('modified')
                        #print(reg_modified)
                        if reg_modified != -1 and handled == False:
                            ins_str = ('mov %s, %s' % (op_str, reg_value))
                            ins_kv = key_value(ins_str, asm_index)
                            ins_kv.add_to_list(self.insert_list)
                        kv_tmp.value = asm_index
                        kv_tmp.add_to_list_max(self.dist_reg_cursor_list)
                elif 'b.' in self.asm_list[asm_index].instr:
                    ble_ins_str = ('%s OUT_%d' % (self.asm_list[asm_index].instr, self.block_num))
                    #replace b.le #+0x2b40 with b.le OUT
                    self.asm_list_insert(asm_index, ble_ins_str)
                    self.asm_list_remove(asm_index + 1)
                    ins_kv_out = key_value(('OUT_%d:' % self.block_num), asm_index + 1)
                    self.insert_list.append(ins_kv_out)
                    ins_kv_nop = key_value('nop', asm_index + 1)
                    self.insert_list.append(ins_kv_nop)
        #key_value.show_list(self.dist_list)
        #print('//average malloc size: %f' % mean(self.malloc_size_list))

    def reg_num_in_list(self, kv_cur_reg, sub_dist_list):
        kv_tmp = key_value(kv_cur_reg.key.replace('w', 'x'), kv_cur_reg.value)
        base_index_x = kv_tmp.get_first_index(sub_dist_list)
        if base_index_x != -1:
            return base_index_x
        kv_tmp.key = kv_tmp.key.replace('x', 'w')
        base_index_w = kv_tmp.get_first_index(sub_dist_list)
        if base_index_w != -1:
            return base_index_w
        return -1




    def gen_output(self):
        print('\t\t:')

    def gen_input(self):
        print('\t\t:', end = '')
        is_first = True
        for item in self.malloc_reg_list:
            ######## DO NOT SUPPORT VECTORS ##########
            if '.' in item.key or 'v' in item.key:
                continue
            if is_first:
                sym = ''
                is_first = False
            else:
                sym = ','
            print(sym,end='')
            print('[input_%s_%d] "r" (ptr_%s_%d_in)' % (item.key, self.block_num, item.key, self.block_num), end='')
        print('')

    def gen_clobbers(self):                
        dist_set = set([])
        print('\t\t',end='')
        #print('gen_clobbers')
        #key_value.show_list(self.dist_list)
        for item in self.dist_list:
            dist_set.add(item.key)
        for item in self.dist_list2:
            dist_set.add(item.key)
        is_colon = True
        for item in dist_set:
            ######## DO NOT SUPPORT VECTORS ##########
            if not (('x' in item) or ('w' in item)):
                continue
            if '#' in item:
                continue
            if is_colon:
                sym = ':'
                is_colon = False
            else:
                sym = ','
            print(sym,end='')
            print('"%s"' % item, end='')
        print('')

    def gen_asm_tail(self):
        self.gen_output()
        self.gen_input()
        self.gen_clobbers()

    def gen_inline_asm(self):
#        print('\tgettimeofday(&tv_begin, NULL);')
        print('\tfor(long i = 0;i < %d;i++)\n\t{' % self.hotness)
        print('\tasm volatile(')
        self.print_asm()
        self.gen_asm_tail()
        print('\t);')
        for item in self.malloc_reg_list:
            ######## DO NOT SUPPORT VECTORS ##########
            if ('v' not in item.key) and ('.' not in item.key):
                print('\t\t}{static long long offset_%s_%d = 0;' % (item.key, self.block_num))
                print('\t\toffset_%s_%d = (offset_%s_%d + %d) %% (%d - 8192);' % (item.key, self.block_num, item.key, self.block_num,self.offset_step, item.value))
                print('\t\tptr_%s_%d_in = ptr_%s_%d + offset_%s_%d;' % (item.key, self.block_num, item.key, self.block_num, item.key, self.block_num))
        print('\t}')
#        print('\tgettimeofday(&tv_end, NULL);')
#        print('\ttimersub(&tv_end, &tv_begin, &tv_sub);')
#        print('\ttimeradd(&tv_sum, &tv_sub, &tv_sum);')


class gen_code:
    gen_malloc = []
    gen_free = []
    exclude_blk = (999999,)
#    exclude_blk = (1877,)
    exclude_blk = (1931,)#641
    def __init__(self):
        self.ab_loaded = False
        self.ab_list = []
        self.exclude_blk = gen_code.exclude_blk
        self.start_blk = 0
        self.count_limit = 50000
        self.print_flag = False
        #number of blocks in a single c file:
        self.split_size = 3
        self.fixed_hotness = 1
        self.full_loop = 1
        self.asm_loop_scale = 1/float(10000)
        self.offset_step = 1024

    @classmethod
    def add_gen_malloc(self, gen_malloc_list):
        gen_code.gen_malloc = gen_code.gen_malloc + gen_malloc_list
    
    @classmethod
    def add_gen_free(self, gen_free_list):
        gen_code.gen_free = gen_code.gen_free + gen_free_list

    #load asm file, asm orgnized as blocks seperated by empty lines
    #There must be at least one empty line at the end of asm file
    def load_asm(self, bench_name):
        f = open('%s.asm' % bench_name)
        f_hotness = open('%s.hotness' % bench_name)
        ins_list = []
        line = f.readline()
        block_count = 0
        while line:
            if len(line) <= 2 or (not line):
                if (block_count < self.start_blk):
                    block_count += 1
                    ins_list = []
                    line = f.readline()
                    continue
                ab_item = asm_block(None)
                ab_item.block_num = block_count
                ab_item.load_list(ins_list)
                ab_item.offset_step = self.offset_step
                line_hotness = f_hotness.readline()
                #print(line_hotness)
                ab_item.hotness = float(line_hotness) * self.asm_loop_scale + 1
#                ab_item.hotness = self.fixed_hotness
                self.ab_list.append(ab_item)
                if (block_count >= self.start_blk + self.count_limit - 1):
                    break
                block_count += 1
        #for statistics
        #        print('//instructions: %d' % len(ins_list))
                ins_list = []
#                ggcc.collect()
                line = f.readline()
                continue
            #msr and mrs are handled here, because they look like this:mrs x20, (unknown)
            line = line.replace('(unknown)', 'fpcr')
            line = re.sub(u"\\(.*?\\)", "", line).replace('\n', '') 
            #pc is handled here, because it's hard to put it anywhere else
            if 'pc+' in line:
                pc_line_list = line.split()
                for i in range(len(pc_line_list)):
                    if 'pc+' in pc_line_list[i]:
                        pc_line_list[i] = '[sp, #17]'
                line = ' '.join(pc_line_list)

            ins_list.append(line.lstrip())
            line = f.readline()
        f.close()
        f_hotness.close()
        self.ab_loaded = True

    def gen_c_file_head(self):
        print('#include <stdio.h>\n#include <stdlib.h>\n#include <sys/time.h>\nint main(void)\n{')
        print('\tsrand((unsigned)time(NULL));\n\tstruct timeval tv_begin, tv_end, tv_sum, tv_sub;')
        print('\ttv_sum.tv_sec = 0;\n\ttv_sum.tv_usec = 0;')
    def gen_c_file_tail(self):
        print('\tprintf("Finished!\\n");')
        print('\tprintf("Total time:\\n\\ttv_sum.tv_sec = %ld, tv_sum.tv_usec = %ld\\n", tv_sum.tv_sec, tv_sum.tv_usec);')
        print('\treturn 0;\n}')
        print('/////////////////// END OF FILE ///////////////////')
    def gen_c_file(self, start, count):
        self.start_blk = start
        self.count_limit = count
        self.gen_c_file_head()
        end_of_file = True
        for item in gen_code.gen_malloc:
            blk_num = int(item.split('_')[2].split()[0])
            if blk_num < self.start_blk:
                continue
            if (blk_num > self.start_blk + self.count_limit - 1):
                break
            print(item)
        print('\tgettimeofday(&tv_begin, NULL);')
        print('for(int full_loop = 0;full_loop < %d;full_loop++)\n{' % self.full_loop)
        blk_count = 0
        for item in self.ab_list:
            if blk_count < self.start_blk:
                blk_count += 1
                continue
            ########## DO NOT SUPPORT 339th block ###########
            if blk_count in self.exclude_blk:
                blk_count += 1
                continue
            if (blk_count > self.start_blk + self.count_limit - 1):
                end_of_file = False
                break

            if self.print_flag:
                print('\tprintf("Block: %d \\n");' % blk_count)
            else:
                print('\t//printf("Block: %d \\n");' % blk_count)

#            item.gen_prep_mem()
            item.gen_inline_asm()
#            item.gen_free_mem()
            blk_count += 1
        print('}////// END OF FULL_LOOP')
        print('\tgettimeofday(&tv_end, NULL);')
        print('\ttimersub(&tv_end, &tv_begin, &tv_sub);')
        print('\ttimeradd(&tv_sum, &tv_sub, &tv_sum);')
        for item in gen_code.gen_free:
            blk_num = int(item.split('_')[2].split(')')[0])
            if blk_num < self.start_blk:
                continue
            if (blk_num > self.start_blk + self.count_limit - 1):
                break
            print(item)
        self.gen_c_file_tail()
        #if it is the end of file, read cannot be continued, return False, otherwise return True
        return (not end_of_file)

    

gc = gen_code()
gc.offset_step = 1024
#gc.fixed_hotness = 800
gc.full_loop = 20
gc.asm_loop_scale = 1/float(5000)
gc.start_blk = 0
gc.load_asm('600.perlbench_s')
#gc.load_asm('602.gcc_s')
#gc.load_asm('605.mcf_s')
#gc.load_asm('620.omnetpp_s')
#gc.load_asm('623.xalancbmk_s')
#gc.load_asm('625.x264_s')
#gc.load_asm('631.deepsjeng_s')
#gc.load_asm('641.leela_s')
#gc.load_asm('648.exchange2_s')
#gc.load_asm('657.xz_s')
#gc.load_asm('test')
#blk_start = 0
#blocks per file, 2000 is the maximum number:
blk_count = 5000
file_count = 100
gc.print_flag = False
#gc.print_flag = True

blk_start = gc.start_blk
#blk_count = 1
#file_count = 1

#do not modify loop_count
loop_count = 0
while True:
    if loop_count >= file_count:
        break
    have_next = gc.gen_c_file(blk_start, blk_count)
    if not have_next:
        break
    blk_start += blk_count
    loop_count += 1
#print(len(gc.ab_list))
#gc.load_asm('test.asm')
#gc.ab.show()

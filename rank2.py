import sys
import math

filename = sys.argv[1]
#filename = filename[:-5]+'.hotness'




print(filename)

total_count = 0
block_count = 0
with open(filename,'r') as f:
    for line in f:
        line = int(line.strip('\n'))
        total_count+=line
        block_count+=1

#total_count: all the blocks execution time
#block_count: total blocks
#part_limit: how many blocks in 1%
#part_sum: sum of execution time in a part
#inpart_count: (1,part_limit)
#baseline: the sum of the first part's execution time
#ranklog: output file

part_limit = int(block_count/100)
part_sum = 0
inpart_count = 0
part_count = 0
print(total_count)
baseline = 0
ranklog = open(filename[:-8]+'.rank2','w')

with open(filename,'r') as f:
    for line in f:
        inpart_count+=1
        line = int(line.strip('\n'))
        part_sum+=line
        if inpart_count==part_limit:
            #print(float(part_sum)/total_count)
            part_count+=1
            #part_sum = math.log10(part_sum)
            if part_count == 1:
                baseline = part_sum     
                ranklog.write(str(1)+' '+str(part_count)+' '+str(1)+'\n')
            else:
               # print(float(math.log10(1+float(part_sum)/baseline)))
                print(float(float(part_sum)/baseline))
                ranklog.write(str(1)+' '+str(part_count)+' ')
                ranklog.write("%.2f\n" % round(float(part_sum)/baseline, 2))
            part_sum=0
            inpart_count = 0


ranklog.write('\n')
part_sum=0
unpart_count=0
part_count=0
inpart_count=0

with open(filename,'r') as f:
    for line in f:
        inpart_count+=1
        line = int(line.strip('\n'))
        part_sum+=line
        if inpart_count==part_limit:
            #print(float(part_sum)/total_count)
            part_sum = math.log10(part_sum)
            part_count+=1
            inpart_count=0
            ranklog.write(str(2)+' '+str(part_count)+' ')
            ranklog.write("%.2f\n"% round(math.log1p(float(part_sum)/baseline), 2))
            part_sum=0 



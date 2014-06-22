import sys
import os
from operator import itemgetter

def order_chromes(fin):
	f_arr = []
	c_step = []
	old_line = ''
	chr_arr = []
	iloop = False
	thirst = False
	for line in fin:
		f_arr.append(line.split('\t'))
	f_arr = sorted(f_arr, key=itemgetter(0))
	for line in f_arr:
		if thirst == False:
			old_line = line[0]
			c_step.append(line)
			thirst = True
		else:
				if line[0] == old_line:
					c_step.append(line)
				if line[0] != old_line or line == f_arr[-1]:
					old_line = line[0]
					chr_arr.append(c_step)			
					c_step = []
					c_step.append(line)
	for gene in chr_arr:
		gene.sort(lambda x, y: cmp(int(x[3]), int(y[3])))
	return chr_arr
def manip(chr_arr, fout):
	for chr in chr_arr:
		overlapper(chr, fout)
	
	return 0 
def overlapper(chr, fout):
	for gene1 in chr:
		g1_start = int(gene1[3])
		g1_end = int(gene1[4])
		for gene2 in chr:
			if gene1 != gene2:
				g2_start = int(gene2[3])
				g2_end = int(gene2[4])
				if g2_start <= g1_end:
					over_len = (g1_end - g2_start)
					fout.write(gene1[0] + '\t' + gene1[8] + '\t' + gene2[8] + '\t' + `over_len` + '\t' + `g1_end - over_len` + '\t' + `g2_start + over_len ` + '\n')
				if g2_start > g1_end:
					break
	return 0
def real_main(fin, fout):
	chr_arr = order_chromes(fin)
	manip(chr_arr, fout)
	
if __name__ == '__main__':
	fin  = open(sys.argv[1], 'rb')
	fout = open(sys.argv[2], 'wb')
	real_main(fin, fout)
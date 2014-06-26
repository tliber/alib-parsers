import sys
import os
from operator import itemgetter
from optparse import OptionParser

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
def manip(chr_arr, fout, opts):
	for chr in chr_arr:
		overlapper(chr, fout, opts)
		print '1 more'
	return 0 
def overlapper(chr, fout, opts):
	
	for gene1 in chr:
		g1_start = int(gene1[3])
		g1_end = int(gene1[4])
		for gene2 in chr:
			if gene2[8] != gene1[8]:
				g2_start = int(gene2[3])
				g2_end = int(gene2[4])		
				if  g1_start <= g2_start <= g1_end:
					over_len = (g1_end - g2_start)
					if opts["o_len"] and over_len <= int(opts["o_len"]):
						# if over_len <= int(opts["o_len"]):	
							# fout.write(gene1[0] + '\t' + gene1[8] + '\t' + gene2[8] + '\t' + `over_len` + '\t' + `g1_end - over_len` + '\t' + `g2_start + over_len ` + '\n')
							# print gene1[0] + '\t' + gene1[8] + '\t' + gene2[8] + '\t' + `over_len` + '\t' + `g1_end - over_len` + '\t' + `g2_start + over_len ` + '\n'
							continue
					if opts["dup"]:
						if g1_start == g2_start and g1_end == g2_end:
							fout.write(gene1[0] + '\t' + gene1[8] + '\t' + gene2[8] + '\t' + `over_len` + '\t' + `g1_end - over_len` + '\t' + `g2_start + over_len ` + '\t' + 'OP' + '\n')
						else: 
							fout.write(gene1[0] + '\t' + gene1[8] + '\t' + gene2[8] + '\t' + `over_len` + '\t' + `g1_end - over_len` + '\t' + `g2_start + over_len ` + '\t' + '-' + '\n')
							continue
					else:
						fout.write(gene1[0] + '\t' + gene1[8] + '\t' + gene2[8] + '\t' + `over_len` + '\t' + `g1_end - over_len` + '\t' + `g2_start + over_len ` + '\n')
						# print gene1[0] + '\t' + gene1[8] + '\t' + gene2[8] + '\t' + `over_len` + '\t' + `g1_end - over_len` + '\t' + `g2_start + over_len ` + '\n'
				if g2_start > g1_end:
					break
	return 0
def parameters():
	opts = OptionParser()
	opts.add_option("-l", dest="o_len", help ="sets up a minimun overlap as overlab criteria")
	opts.add_option("-d", "--rem", action="store_true",dest="dup",default=False,help="add perfect duplicate flag to print to output")
	(opts, args) = opts.parse_args()
	return opts.__dict__, args
def real_main(fin, fout):
	chr_arr = order_chromes(fin)
	opts,args = parameters()
	manip(chr_arr, fout, opts)
if __name__ == '__main__':
	fin  = open(sys.argv[1], 'rb')
	fout = open(sys.argv[2], 'ab')
	
	real_main(fin, fout)
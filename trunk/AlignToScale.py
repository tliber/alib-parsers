import sys
import os
import re

def getQ(fin, query, N_dom):
	
	qseq = ''
	miss = False
	for line in fin:
		if miss == False:
			if re.match("(>%s)\sD(%d).*Query: start\s(\d+)\send\s(\d+).*\n(.*)" %(query,int(N_dom)), line):
				Qid = re.match("(>%s)\sD(%d).*Query: start\s(\d+)\send\s(\d+).*\n(.*)" %(query, int(N_dom)), line)
				miss = True
		else:		
				if line.startswith('>') == False:
					q_seq = line
				else:
					break
	return Qid, q_seq
def decompile(fin, Qid, q_seq, fout): 
	click = False
	for line in fin:
		if click == False:
			seq_set = re.match(">(\S+).*Query: start\s(\d+)\send\s(\d+).*\n",line)
			if seq_set:
				fout.write(seq_set.group())
				click = True
		else:
			if line.startswith('>') == False:
				ali_seq = truncate(line, Qid, q_seq)
				print ali_seq
				fout.write(ali_seq)
			if line.startswith('>'):
					click = False
	
	return 0 
def truncate(line, Qid, q_seq):
	seq_scan = []
	seq_main = []
	form = ''
	for char in line:
		seq_scan.append(char)
	if '\r' in seq_scan:
		seq_scan = seq_scan[:-2]
	else:
		seq_scan = seq_scan[:-1]
	for char in q_seq:
		seq_main.append(char)
	if '\r' in seq_main:
		seq_main = seq_main[:-2]	
	else:
		seq_main = seq_main[:-1]
	ali_seq = best_match(seq_scan, seq_main, p1, p2)
	for char in ali_seq:
		form = form + char
	form = form + '\n'
	return form
def best_match(seq_scan, seq_main, p1, p2):
	mover = 0
	count = 0
	best_score = 0
	best_slice = ''
	main_slice = seq_main[int(p1):int(p2)]
	if len(seq_scan) < len(main_slice):
		flank = (len(main_slice) - len(seq_scan))
		seq_scan.extend(['-' for i in range(flank)])
		seq_scan[:0] = ('-' * flank) 	
	max_range = len(seq_scan) - len(main_slice) 
	while count != max_range + 1:
		seq_slice = seq_scan[int(mover):len(main_slice) + mover]
		plus_score = 2 * (len([(i) for i,j in zip(main_slice, seq_slice) if i == j]))
		minus_score = (len([(i) for i,j in zip(main_slice, seq_slice) if i == j]))
		hit_score = plus_score - minus_score
		if hit_score > best_score:
			best_score = hit_score
			best_slice = seq_slice
		count = count + 1
		mover = mover + 1
	return best_slice
def mainFunx(fin, query, fout, N_dom):
	Qid, q_seq = getQ(fin, query, N_dom)
	decompile(fin,Qid, q_seq, fout)
	return 0
if __name__ == '__main__':
	fin = open(sys.argv[1], 'rb')
	fout = open(sys.argv[2], 'ab')
	query = sys.argv[3]
	N_dom = sys.argv[4]
	p1 = sys.argv[5]
	p2 = sys.argv[6]
	# print fin
	if os.stat(sys.argv[1])[6]==0:
		print "file empty"
	else:
		mainFunx(fin, query, fout,N_dom)
#!/usr/bin/env python


##########################
#      FASTA PARCER	     #
#      No filter(yet)	 #
#						 #
#						 #
#						 #
#						 #
#						 #
#By:Anatoliy Liberman    #
#For: Genome Center UCD  #
#Supervisor:             #
#    Alexander Kozik     #
#                        #
##########################

import sys
import re
import fileinput

def domain_hits(fin):
	hmm_FILE  = open(fin, "rb")
	for line in hmm_FILE:
		pos = line.find('Domain search space  ')
		if pos != -1:
			domainValueString = str(line)
			domainValue = re.findall('\d+',domainValueString)
			if domainValue:
				domainValue = int(domainValue[0])
			if domainValue == 0:
				sys.exit(1)
			return domainValue
def get_rows(fin):
	arr_rows = []
	arr_row = []
	finder = True
	hmm_f = open(fin, 'r')
	for line in hmm_f:
		if finder:
			pos= line.find('E-value  score  bias    E-value  score  bias    exp  N  Sequence   ')
			if pos !=-1:
				finder = False
				next(hmm_f)
		else:
			items = line.split()
			arr_rows.append(items)
			arr_row = []
			if line =='\n':
				break
	arr_rows = arr_rows[:-1]
	#INSERT FILTER OPTIONS
	return arr_rows

def get_ids(arr_rows):
	seq_ids = []
	for row in arr_rows:
		seq_ids.append(row[8])
	return seq_ids
def get_det(fin, ids):
	hmm_f = open(fin, 'r')
	finder = False
	maxstep = len(ids)
	all_desc = []
	arr_desc = []
	step = 0
	for line in hmm_f:
		if step != maxstep:
			if not finder:
				if line.find('>> ' + ids[step]) != -1:
					next(hmm_f)
					next(hmm_f)
					finder = True			
			else:
				if line != '\n':
						line = ids[step] + line
						line = line.split()
						all_desc.append(line)
				if line == '\n':
					step += 1
					finder = False
		else:
			break
	# print all_desc
	return all_desc	
def get_aminos(fin, desc_arr):
	hmm_f = open(fin, 'r')
	limit = len(desc_arr)
	sequence =''
	fasfa_arr = []
	step = 0
	d_num = ''
	found = False
	id_match = False
	for line in hmm_f:
		if step != limit:
			if not found:	
				if not id_match:
					if line.find('>> ' + desc_arr[step][0]) != -1:
						id_match = True
				else:
					if re.match('.*== domain (\d+).*', line):
						l = re.match('.*== domain (\d+).*', line)
						d_num = l.group(1)
						if d_num == desc_arr[step][1]:
							found = True
			if found:
				if not re.match('.*== domain (\d+).*', line):
					if re.match('.*%s[\s]+\d+\s+(.*)\s+\d+\s+.*' %desc_arr[step][0], line):
						fmatch = re.match('.*%s[\s]+\d+\s+(.*)\s+(\d+)\s+.*' %desc_arr[step][0], line)
						if fmatch.group(2) != desc_arr[step][11]:
							sequence = sequence + fmatch.group(1)
						else:
							sequence = sequence + fmatch.group(1)
							sequence = re.sub('-','',sequence)
							fasfa_arr.append('>' + desc_arr[step][0] + ' ' + 'D' + desc_arr[step][1] + ' ' + desc_arr[step][10]+ ' ' + desc_arr[step][11] + '\n' + sequence)
							step += 1
							sequence = ''
							if step == limit:
								break
							if desc_arr[step][0] != desc_arr[(step - 1)][0]:
								id_match = False
								found = False
	return fasfa_arr

def fasta_former(data):
	format = ''
	for line in data:
		format = format + line + '\n'
	return format
if __name__ == '__main__':
	if len(sys.argv) <3:
		print "1 = FASFA parser, 2 = Hmm_profile 3 = out_file"
		print "if 4 = f(ilter) 5 = e-value minimun threshold for match to query"
		print "optional 6th argv allows for minimal lenght"
		print len(sys.argv)
		sys.exit(1)

	fin = sys.argv[1]
	fout = sys.argv[2]
	hits = domain_hits(fin)
	if hits == 0:
		print 'no hits'
		sys.exit(1)
	rows = get_rows(fin)
	seq_ids = get_ids(rows)
	seq_det = get_det(fin, seq_ids)
	fasta_data = get_aminos(fin, seq_det) 
	fasta_format =fasta_former(fasta_data)
	f = open(fout, 'a')
	f.write(fasta_format)
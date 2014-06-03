#!/usr/bin/env python


##########################
#      FASTA PARCER	     #
#      					 #
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
import os
from optparse import OptionParser
from math import e
def domain_hits(fin):
	hmm_FILE  = open(fin, "rb")
	for line in hmm_FILE:
		pos = line.find('Domain search space  ')
		if pos != -1:
			domainValueString = str(line)
			domainValue = re.findall('\d+',domainValueString)
			if domainValue:
				domainValue = int(domainValue[0])
			return domainValue
def get_rows(fin, opts):
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
		# print str(line)
		format = format + line + '\n'
	return format
def options():
	opts = OptionParser()
	opts.add_option("-a","--acc", dest="o_acc", help ="sets a min accuaracy for sequence match(enter percentage)")
	opts.add_option("-l","--len", dest="o_len", help = "set min sequence lenght(enter lenght)")
	opts.add_option("-i","--ival", dest="ivalue",help="sets max for i-values(enter i-value)")
	opts.add_option("-c","--cval", dest="cvalue", help = "sets max for e-values(enter e-value")
    
	(opts, args) = opts.parse_args()

	return opts.__dict__, args
def opts_filter(fin, seq_det, opts):
	
	if opts["cvalue"]:
		for row in seq_det:
			if float(row[5]) >= float(opts["cvalue"]):
				seq_det.remove(row)
	if opts["ivalue"]:	
		for row in seq_det:
			if float(row[6]) >= float(opts["ivalue"]):
				seq_det.remove(row)
	if opts["o_acc"]:	
		for row in seq_det:
			if float(row[16]) <= float(opts["o_acc"]):
				seq_det.remove(row)
	if opts["o_len"]:
		reader = open(fin,'rb')
		finder = True
		for line in reader:
			if finder:
				found = re.match('Query:[\s\t]+(\S+)[\s\t]+\[(\w+)\=(\d+)\]',line)
				if found:
					for row in seq_det:
						if int(row[11]) - int(row[10]) <= int(opts["o_len"]):
							seq_det.remove(row)
					finder = False
			else:
				break
					
	print str(len(seq_det)) + ' sequence matches extracted from ' + str(fin)
	return seq_det
def real_main(fin, fout):
	hits = domain_hits(fin)
	if hits == 0:
		print "0 hits found " + fin
		return
	opts,args = options()
	rows = get_rows(fin, opts)
	
	seq_ids = get_ids(rows)
	seq_det = get_det(fin, seq_ids)
	if opts:
		opts_filter(fin, seq_det, opts)
	fasta_data = get_aminos(fin, seq_det) 
	fasta_format =fasta_former(fasta_data)
	f = open(fout, 'a')
	f.write(fasta_format)
if __name__ == '__main__':
	if len(sys.argv) <3:
		print "1 = FASFA parser, 2 = Hmm_profile 3 = out_file"
		print "for options input command arguements followed by -h"
		print len(sys.argv)
		sys.exit(1)
	fin = sys.argv[1]
	fout = sys.argv[2]
	if 	os.path.isdir(fin):
		for subdir, dirs, files in os.walk(fin):
			for file in files:
				path = os.path.join(subdir, file)
				real_main(path, fout)
	else:
		real_main(fin, fout)


	
#!/usr/bin/env python



##########################
#      FASTA PARCER	     #
#  	prints fasfa file	 #
#	for domain hit 		 #
#	match. Optional      #
#	matching parameters  #
#	allow for parameter  #
#	specific domain hit  #
#	results. Options	 #
#	allow for creation   #
#	of summary and 		 #
#	detail description	 #
#	as well				 #
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

def getProteinType(fin):
	hmm_FILE  = open(fin, "r")
	q_str = ''
	a_str = ''
	d_str = ''
	
	for line in hmm_FILE:
		query = re.match('Query:[\s\t]+(\S+)[\s\t]+\[(\w+)\=\d+\]',line)
		if query:
			q_str= query.group(1)
		acces = re.match("Accession:[\s\t]+(\S+)[\s\t\n]+",line)
		if acces:
			a_str = acces.group(1)
		desc = re.match("Description:[\s\t]+(.*)",line)
		if desc:
			d_str = desc.group(1)
			break
	proteinType = (q_str,a_str,d_str)
	# print protein
	return proteinType
			
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


def get_aminos(fin, desc_arr, proteinType):
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
							fasfa_arr.append('>' + desc_arr[step][0] + ' ' + 'D' + desc_arr[step][1] + ' ' + desc_arr[step][10]+ ' ' + desc_arr[step][11] + ' ' + ' '.join(proteinType[1:]) + '\n' + sequence)
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
	opts.add_option("-s","--out2", dest="o_sum", help = "returns a summary file of the domain hits")
	opts.add_option("-d","--out3", dest="dom", help = "prints domain details to outfile")
    
	(opts, args) = opts.parse_args()

	return opts.__dict__, args
def opts_filter(fin, seq_det,proteinType, sum_rows, opts):
	
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
					
	print str(len(seq_det)) + ' sequence matches extracted from ' + `fin`
	if opts["dom"]:
		dom_form = ''
		out_f2 = open(opts["dom"], 'a')
		dom_det = seq_det[:]

		if os.stat(opts["dom"])[6]==0:
			headers =  "ID # certainty score  bias  c-Evalue  i-Evalue hmmfrom  hmmto alitype alifrom  alito alitype envfrom  envto alitype acc".split()
			dom_det.insert(0, headers)
		for line in dom_det:
			line = '\t'.join(line)
			line = re.sub('\.\.','P',line)
			line = re.sub('\[\]','C',line)
			line = re.sub('\.\]','R',line)
			line = re.sub('\[\.','F',line)
			dom_form = dom_form + line + '\n'	
		out_f2.write(dom_form)
	
	if opts["o_sum"]:
		sum_mark = seq_det[:]
		sum_ids = []
		filt_sum = []
		fout_sum = ''
		out_f3 = open(opts["o_sum"], 'a')
		
		for line in sum_mark:
			sum_ids.append(line[0])
			
		for line in sum_rows:
			if line[8] in sum_ids:
				line[7] = sum_ids.count(line[8])
				filt_sum.append(line)
	
		for line in filt_sum:
			line[:0] = proteinType
			line[-4:] = [''.join(line[-4:])]
			line = '\t'.join(str(el) for el in line)
			fout_sum = fout_sum + line + '\n'
		if os.stat(opts["o_sum"])[6]==0 and fout_sum != 0:
			header =  "Query Accession Description E-value  score  bias    E-value  score  bias    exp  N  Sequence        Description".split()
			header = '\t'.join(header) + '\n'
			out_f3.write(header)
		out_f3.write(fout_sum)
	return seq_det

def real_main(fin, fout):
	hits = domain_hits(fin)
	if hits == 0:
		print "0 hits found " + fin
		return
	opts,args = options()
	proteinType = getProteinType(fin)
	sum_rows = get_rows(fin, opts)	
	seq_ids = get_ids(sum_rows)
	seq_det = get_det(fin, seq_ids)
	if opts:
		opts_filter(fin, seq_det, proteinType, sum_rows, opts)
	fasta_data = get_aminos(fin, seq_det, proteinType) 
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
	len(sys.argv)
	if 	os.path.isdir(fin):
		for subdir, dirs, files in os.walk(fin):
			for file in files:
				path = os.path.join(subdir, file)
				real_main(path, fout)
	else:
		real_main(fin, fout)


	
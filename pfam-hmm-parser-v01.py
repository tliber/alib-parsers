#!/usr/bin/env python


##########################
#By:Anatoliy Liberman    #
#For: Genome Center UCD  #
#Supervisor:             #
#    Alexander Kozik     #
#                        #
##########################

import sys
import os
import fileinput
import re

opts = None

#Returns the number of domain hits found
def domain_HITS(fin):
	hmm_FILE  = open(fin, "rb")
	EVal_FILE  = open(fout, "a")
	for line in hmm_FILE:
		pos = line.find('Domain search space  ')
		if pos != -1:
			domainValueString = str(line)
			domainValue = re.findall('\d+',domainValueString)
			if domainValue:
				domainValue = int(domainValue[0])
				print str(domainValue) + ' Domain hits found'
			if domainValue == 0:
				sys.exit(1)
			return domainValue
#goes through every char in line and seperate by spaces
def get_space_array(line):
	arr = []
	in_word = False
	
	for c in line:
		
		if c == ' ':
			in_word = False
		elif in_word == False:
			arr.append('')
			in_word = True
		
		
		if in_word:
			arr[len(arr) - 1] = arr[len(arr) - 1] + c
	return arr

#tab delimiter
def tab_separate_from_array(arr):
	result = ''
	for word in arr:
		result = result + word
		result = result + '\t'
	result = result[:-1] #chop off the extra tab
	return result
#find line of id and append

def seq_get_id(fin, identifier, count):
	f = open(fin, 'rb')

	arr = []
	found = False
	for line in f:
		if not found:
			if line.find('>> ' + identifier) != -1:
				next(f)
				next(f)
				found = True
		else:
			line = re.sub('\.\.','P',line)
			line = re.sub('\[\]','C',line)
			line = re.sub('\.\]','R',line)
			line = re.sub('\[\.','F',line)
			
			arr.append(line)
			count = count - 1
			if count == 0:
				break
	f.close()
	return arr
#calls id and seq
def seq_get_all_ids(fin, lines, opt):
	result = ''
	offset = 0
	if opts and 'g' in opts:
		offset = 3
	for line in lines:
		identifier = line[8 + offset]
		count = int(line[7 + offset])
		seqs = seq_get_id(fin, identifier, count)
		
		for seq in seqs:
			result = result + identifier + seq
	return result
def tab_separated_evals(evalues):
	result = ''
	for evalue in evalues:		
		result = result + tab_separate_from_array(evalue)
	return result

#writes header to file and return array of E-Values which follow it(2nd function)
def eval_get_array (ecount, fin, fout, opt):
	check = True
	hmm_FILE  = open(fin, "rb")
	EVal_FILE  = open(fout, "a")
	lines = []
	for line in hmm_FILE:
		if check:
			pos= line.find('E-value  score  bias    E-value  score  bias    exp  N  Sequence   ')
			if opt and 'g' in opt:
				line = 'Query	Accession	Description' + line
			if pos != -1:
				check = False
				if ecount != 0:	
					if opt and 'h' in opt:
						to_print = tab_separate_from_array(get_space_array(line))
						EVal_FILE.write(to_print)
					next(hmm_FILE)
		else:
			ecount = ecount - 1
			line_arr = get_space_array(line)
			line_arr[-4] = line_arr[-4] + ' ' + line_arr[-3] + ' ' + line_arr[-2] + ' ' + line_arr[-1]
			del line_arr[-3:]
			lines.append(line_arr)
			if ecount == 0:
				break
	hmm_FILE.close()
	EVal_FILE.close()
	return lines

def get_quar_assent(fin):
	hmm_FILE  = open(fin, "r")
	q_str = ''
	a_str = ''
	d_str = ''
	q_tot = ''
	for line in hmm_FILE:
		query = re.match('Query:[\s\t]+(\S+)[\s\t]+\[(\w+)\=(\d+)\]',line)
		if query:
			q_str= query.group(1)
			q_tot= query.group(3)
			
		acces = re.match("Accession:[\s\t]+(\S+)[\s\t\n]+",line)
		if acces:
			a_str = acces.group(1)
		desc = re.match("Description:[\s\t]+(.*)",line)
		if desc:
			d_str = desc.group(1)
	
	
	return q_str, a_str, d_str, q_tot

def fout2_headers(fout2, opt):
	f2  = open(fout2, "a")
	to_print = ''
	new_print = []
	check = True
	hmm_FILE  = open(fin, "rb")
	EVal2  = open(fout2, "a")
	to_print = 'Sequence #  type  score  bias  c-Evalue  i-Evalue hmmfrom  hmm to    alifrom  alito type   envfrom  envto  type   acc'
	if 'g' in opt:
		to_print = 'Query	Accession	Description ' + to_print
	new_print[:] = to_print.split() 
	new_print = tab_separate_from_array(new_print) + '\n'
	f2.write(new_print)
def tab_fout2(lines):
	arr_rows = []
	arr_row=[]
	count = 0
	for line in lines:
		
		to_print = tab_separate_from_array(get_space_array(lines))
	arr = to_print.split()
	for i in arr:
		if len(arr_row) != 17:
			arr_row.append(i)
		elif len(arr_row) == 17:
			arr_rows.append(arr_row)
			if i:
				
				count = 0
				arr_row = []
				arr_row.append(i)
		else:
			break
		
	return arr_rows
def dfilter(arr_rows, thresh, q_perc,q_tot):
	arr_hold = []
	arr_hold2 = []
	perc = ''
	l_span = ''
	if thresh !=0:
		thresh = float(thresh)
		for i in arr_rows:
			if float(i[6]) <= thresh:
				arr_hold.append(i)
	if q_perc !=0:	
		q_perc = float(q_perc)
		for i in arr_hold:
			l_span = int(i[11]) - int(i[10])
			l_span = float(l_span)
			perc = l_span/float(q_tot)
			if perc >=q_perc:
				arr_hold2.append(i)
	if q_perc!=0:
		arr_hold = arr_hold2
	arr_rows = arr_hold
	return arr_rows

def desc2(arr_rows, d_str, a_str, q_str):
	for i in arr_rows:
		i.insert(0, d_str)
		i.insert(0, a_str)	
		i.insert(0, q_str)
	return arr_rows
def arr_row_tabs(arr_rows):
	i = ''
	w_tab = ''
	w_tabs = ''
	row = ''
	rows = ''
	for i in arr_rows:
		# for word in i:
			if i:
				w_tab = '\t'.join(i) + '\n'
				w_tabs = w_tabs + w_tab
	# print w_tabs
	return w_tabs

	
	
if __name__ == '__main__':
	if len(sys.argv) < 4 or len(sys.argv) > 9:
		print len(sys.argv[:])
		print "[1] = file_input [2]=evalue_output [3]=id_details_output"
		print "if [4]=y append header: 'E-value  score  bias....' to evalue_output to evalue_output" 
		print "g = add 3 columbs for accession, query, and description for file 1"
		print "h = prints headers for both filesS"
		print "d -allows for detailed analysis(options e e and  l"
		print "-e = threshold only returns e value over threshold"
		print "-l = threshhold for query lenght"
		sys.exit(1)

	fin = sys.argv[1]
	fout = sys.argv[2]
	fout2 = sys.argv[3]
	#option to print E-Val header line' E-value  score  bias....Description' in file 1
	if len(sys.argv) >= 5:
		opt = sys.argv[4]
			#do other tuff
	else:
		opt = 0
	opts = opt
	if 'd' in opt:
		if '-e' in sys.argv[5]:
			thresh = sys.argv[6]
		else:
			thresh = 0
		if 'l' in sys.argv[7]:
			q_perc = sys.argv[8]
		else:
			q_perc = 0
	hits = domain_HITS(fin)
	
	evalues = eval_get_array(hits, fin, fout, opt)
	q_str, a_str, d_str,q_tot = get_quar_assent(fin)
	if opt and 'g' in opt:
		for evalue in evalues:
			evalue.insert(0, d_str)
			evalue.insert(0, a_str)	
			evalue.insert(0, q_str)
	
	if opt and 'h' in opt:
		fout2_headers(fout2, opt)
	evals_string = tab_separated_evals(evalues)
	id_string = seq_get_all_ids(fin, evalues, opt)
	arr_rows = tab_fout2(id_string)
	if 'd' in opt:
		arr_rows = dfilter(arr_rows, thresh, q_perc,q_tot)
	if  opt and 'g' in opt:
		arr_rows = desc2(arr_rows,d_str,a_str,q_str)
	arr_rows = arr_row_tabs(arr_rows)
	f = open(fout, 'a')
	f2 = open(fout2, 'a')
	f.write(evals_string)
	# print evals_string
	f.write('\n')
	f2.write(arr_rows)
	# print id_string
	f.close()
	f2.close()




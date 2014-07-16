# parser for converting SSpace final evidence files to GFF3 format
# >> evidence_to_GFF3.py evidence.in file.out 
import sys
import re

def grab_info(fin, fout):
	arr = []
	start = 0
	for line in fin:
		if re.match('>(\S+)\|(\w+)(\d+)', line):
			scaf_info = re.match('>(\S+).size(\d+).tigs(\d+)', line)
			scaf_id = scaf_info.group(1)
			scaf_size = scaf_info.group(2)
			tigs_num = scaf_info.group(3)
		if line.startswith('>')== False:
			if re.match('(\S+)\|(\D+)(\d+)\|(\w+)\|gaps-*\d+', line):
				info  = re.match('(\S+)\|(\D+)(\d+)\|\D+\d+\|gaps-*(\d+)', line)
				contig = info.group(1)
				tig_size = int(info.group(3))
				gap = int(info.group(4))
				strand_dir = contig[0]
				if strand_dir == 'f':
					strand_dir = '+'
				elif strand_dir == 'r':
					strand_dir = '-'
				contig_name = re.sub('._', 'Con', contig)
				tig_end = start + tig_size 
				form = [scaf_id,'SSpace', contig, `start`, `tig_end`, '.', strand_dir, '.', 'ID=' +  contig_name + ';' + 'Name=' + contig_name]  
				form = '\t'.join(form)
				fout.write(form + '\n')
				start = tig_end + gap
			else:
				if re.match('(\S+)\|(\D+)(\d+)', line):
					end_info = re.match('(\S+)\|(\D+)(\d+)',line)
					f_size = int(end_info.group(3))
					scaf_end = start + f_size
					contig = end_info.group(1)
					cont_id = contig[0]
					if cont_id == 'f':
						strand_dir = '+'
					elif cont_id == 'r':
						strand_dir = '-'
					scaf_end = start + int(end_info.group(3))
					contig_name = re.sub('._', 'Con', contig)
					form = [scaf_id,'SSpace', contig, `start`, `scaf_end`, '.', strand_dir, '.', 'ID=' +  contig_name + ';' + 'Name=' + contig_name]
					form = '\t'.join(form)
					fout.write(form + '\n\n')
				start = 0
				
	return 0

def main(fin, fout):
	grab_info(fin, fout)
	return 0
if __name__ == '__main__':
	fin = open(sys.argv[1], 'rb')
	fout = open(sys.argv[2], 'wb')
	main(fin, fout)

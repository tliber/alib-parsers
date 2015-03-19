# Introduction #

This python program is designed to be used with hmm\_search\_files. It detects and displays the number of domain match hits for the sequence query. If matches are founds, it Extracts and appends tab-delimited(Excel formatted) domain sequence summary and domain annotations into 2 separate files. Optional arguments exist for custom modification of the output file.

# Details #

## Input Instructions ##

Arguments:
1 = program 2 = hmm\_file 3 = outfile\_summary 4\_outfile\_details

5 = optional input _ghd_

if d(escriptive)

6 = -e 7 = minimum desired threshold

if d and -e can input additional option:
8 = -l 9 = minimum threshold

all information written below is assumed for default(no 5) program
for further details see **options**

|g  |appends query, accession, and description into outfile\_summary(into columns 1 and 2)|
|:--|:------------------------------------------------------------------------------------|
|h | provides headers at the top of the file for each of the output files|
_Input Sample_

'>>python.exe pfam-hmm-parser-v01.py Zip.hmm.vs.CDS\_L\_sativa\_v4HC\_2014\_02\_01.e10 a.out b.out _gh_'


**Sequence Summary**
.Eval\_Output [file 1](output.md)
Scores for complete sequences (score includes all domains):

Full Sequence
|Column 1| statistical significance for hmm query sequence |_E-value_|
|:-------|:------------------------------------------------|:--------|
|Column 2|normalized expectation (-log(Exp)) |_score_|
|Column 3|E-value bias for query sequence|_bias_|
|_Best Domain Match_|
|Column 4| statistical significance for protein domain sequence match |_E-value_|
|Column 5| normalized expectation (-log(Exp)) |_score_|
|Column 6|E-value bias for best domain match|_bias_|
|_Domain specific hits_|
|Column 7| actual Number of domain matches |_exp_|
|Column 8|adjusted number of domain matches |_N_|
|_Identifiers_|
|Column 9| ID for the protein domain sequence |_Sequence_|
|Column 10 |Description of the sequence alignment |_Description_|

**Sequence’s Domain Annotations**

.domain\_annotation (output file 2)

Domain annotation for each sequence (and alignments):

|Column 1|Sequence ID|_sequence_|
|:-------|:----------|:---------|
|Column 2|Sub domain number for domain match |_`#`_|
|Column 3|Type of sequence |_type_|
|Column 4|normalized expectation (-log(Exp)) |_score_|
|Column 5|expectation bias |_bias_|
|Column 6|match value adjusted for haploid class and genome size, measured in pg (millions of base pairs) |_c-Evalue_|
|Column 7|amount of DNA embedded adjusted for alternative slicing, post translational modifications, multidomain proteins ,gene redundancy, expression and interaction |_i-Evalue_|
|Column 8|first position of the "Query" sequence in the alignment |_hmm from_|
|Column 9|last position of the "Query" sequence in the alignment |_hmmto_|
|Column 10| type of sequencing conducted on Query|_type_|
|P |partial alignment |
|C |complete alignment |
|R |partial upstream alignment |
|F |partial downstream alignment |
|Column 11| first position of the "Subject" sequence in the alignment |_alifrom_|
|Column 12|aligned to last position of the "Subject" sequence in the alignment  |_ali to_|
|Column 13|type of sequencing conducted on "Subject" |_PCRF_|
|Column 14|alignment for referenced sequence match|_envfrom_|
|Column 15|alignment until referenced sequence match end|_envto_|
|Column 16|type of sequencing conducted on Query|_PCRF_|
|Column 17| percent of identity matched |_acc_|

## Options ##

if option _g_ was selected _outfile1_ and _outfile2_ will contain the 3 additional rows,
the rest of the columns will be shifted to the right in order to adjust.

|Column 1| hmm Query ID |_Query_|
|:-------|:-------------|:------|
|Column 2| hmm Accession ID |_Accession_|
|Column 3| query protein's description |_Description_|

if options _d_ was selected

results can be filtered in if they match certain criteria.

example _hmmsearchparser_ _a.out_ _d_-e1e10-l.50

option -e filters out the sequences with i-value below the matching value

option -l filters out sequences whose bp length is below the percentage given (that fulfill) critea of _-e_ as well

For more information about hmm\_pfam\_domains visit http://hmmer.janelia.org/
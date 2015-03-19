## Introduction ##

This program by default extract the fasta sequences with domain hits to an output file. It appends all the sequence matches from either a file, or recursively through an entire directory.

`>>python.exe fasfa_hmm_parser a.out`

`>Viti\_vini.NP\_001268197 D1 89 108 PF10417.4 C-terminal domain of 1-Cys peroxiredoxin
TPGSKVTYPIAADPKrEIIK
>Sola\_tube.XP\_006356461 D1 90 103 PF10417.4 C-terminal domain of 1-Cys peroxiredoxin`

### options ###

to see the options for files and parameters:

`>>python.exe fasfa_hmm_parser file_or_directory a.out -h`

Options:
> `-h, --help            show this help message and exit
> > -a O\_ACC, --acc=O\_ACC
> > > sets a min accuracy for sequence match(enter
> > > percentage)

> > -l O\_LEN, --len=O\_LEN
> > > set min sequence length(enter length)

> > -i IVALUE, --ival=IVALUE
> > > sets max for i-values(enter i-value)

> > -c CVALUE, --cval=CVALUE
> > > sets max for c-values(enter e-value

> > -s O\_SUM, --out2=O\_SUM
> > > returns a summary file of the domain hits

> > -d DOM, --out3=DOM    prints domain details to out file`
example of all the arguments at once(can be input in any order).

`>>python fasfa_hmm_parcer folder a.out -s b.out -d c.out -l 1000 -c 1 -a .95 -i 1.2e-20`

The summary file is formatted to be used in fasta analysis.
The summary and detail files are both tab delimited for use in excel.

## Domain Summary(-s) ##

Full Sequence
|Column 1| hmm Query ID |_Query_|
|:-------|:-------------|:------|
|Column 2| hmm Accession ID |_Accession_|
|Column 3| query protein's description |_Description_|
|Column 4| statistical significance for hmm query sequence |_E-value_|
|Column 5|normalized expectation (-log(Exp)) |_score_|
|Column 6|E-value bias for query sequence|_bias_|
|_Best Domain Match_|
|Column 7| statistical significance for protein domain sequence match |_E-value_|
|Column 8| normalized expectation (-log(Exp)) |_score_|
|Column 9|E-value bias for best domain match|_bias_|
|_Domain specific hits_|
|Column 10| actual Number of domain matches |_exp_|
|Column 11|adjusted number of domain matches |_N_|
|_Identifiers_|
|Column 12| ID for the protein domain sequence |_Sequence_|
|Column 13 |Description of the sequence alignment |_Description_|

## Sequence’s Domain Annotations(-d) ##
Domain annotation for each sequence (and alignments):

|Column 1| hmm Query ID |_Query_|
|:-------|:-------------|:------|
|Column 2| hmm Accession ID |_Accession_|
|Column 3|Sequence ID|_sequence_|
|Column 4|Sub domain number for domain match |_`#`_|
|Column 5|Type of sequence |_type_|
|Column 6|normalized expectation (-log(Exp)) |_score_|
|Column 7|expectation bias |_bias_|
|Column 8|match value adjusted for haploid class and genome size, measured in pg (millions of base pairs) |_c-Evalue_|
|Column 9|amount of DNA embedded adjusted for alternative slicing, post-translation modifications, multidomain proteins ,gene redundancy, expression and interaction |_i-Evalue_|
|Column 10|first position of the "Query" sequence in the alignment |_hmm from_|
|Column 11|last position of the "Query" sequence in the alignment |_hmmto_|
|Column 12| type of sequencing conducted on Query|_type_|
|P |  partial alignment |
|C |  complete alignment |
|R |  partial upstream alignment |
|F |  partial downstream alignment |
|Column 13| first position of the "Subject" sequence in the alignment |_alifrom_|
|Column 14|aligned to last position of the "Subject" sequence in the alignment  |_ali to_|
|Column 15|type of sequencing conducted on "Subject" |_PCRF_|
|Column 16|alignment for referenced sequence match|_envfrom_|
|Column 17|alignment until referenced sequence match end|_envto_|
|Column 18|type of sequencing conducted on Query|_PCRF_|
|Column 19| percent of identity matched |_acc_|

For more information about hmm\_pfam\_domains visit http://hmmer.janelia.org/
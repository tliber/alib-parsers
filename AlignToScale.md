# Introduction #
The input should be a fasta formatted as such

>Viti\_vini.XP\_002285787 D1 4 238 PF00244.15 [14-3-3 protein] 14-3-3 Query: start 1 end 235
AEQAERYDEMVEAMKKVAKLDVELTVEERNLVSVGYKNVIGARRASWRILSSIEQKEETRGNEQNAKRIKDYRQRVEDELSKICNDILSVIDNHLIPSSS
>Popu\_tric.XP\_002311335 D1 7 241 PF00244.15 [14-3-3 protein] 14-3-3 Query: start 1 end 235
AEQAERYDEMVESMKNVAKLNCDLTVEERNLLSVGYKNVIGARRASWRIMSSIEQKEESKGNDSNVKLIKGYRQKVEEELSKICNDILSIIDDHLIPSSA
>Sola\_lyco.XP\_004239061 D1 7 241 PF00244.15 [14-3-3 protein] 14-3-3 Query: start 1 end 235
AEQAERYDEMVESMKKVAKLDVELTVEERNLLSVGYKNVIGARRASWRIMSSIEQKEESKGNEQNVKLIKGYRQKVEEELSKICSDILDIIDKHLIPSAG

## Launching in Command line ##
arg[1](1.md) = fasta.seq (like the one listed above)
arg[2](2.md) = outfile
arg[3](3.md) = desired\_sequence\_to\_match: must be found in file
arg[4](4.md) = specific domain for desired\_sequence
arg[5](5.md) = starting point for alignment, note that 1 indicates the first number in the domain provided
arg[6](6.md) = end point for alignment, not that this is also in reference to the first domain bp

`>>Python/python.exe AlignToScale.py seq.fasta aligned.out query_fullname domain_N(#) starting_bp last_bp`

`>> Python/python.exe AlignToScale.py b.out out.q Cucu_sati.XP_004162227 1 1 40`


# output\_sample #
>Rici\_comm.XP\_002513928 D1 5 239 PF00244.15 [14-3-3 protein] 14-3-3 Query: start 1 end 235
EQAERYDEMVEAMKKVAKLDVELTVEERNLVSVGYKNVI
>Citr\_clem.XP\_006446785 D1 7 240 PF00244.15 [14-3-3 protein] 14-3-3 Query: start 1 end 234
EQAERYDEMVDAMKNVAKLDVELTVEERNLLSVGYKNVI
>Citr\_sine.XP\_006469024 D1 7 240 PF00244.15 [14-3-3 protein] 14-3-3 Query: start 1 end 234
EQAERYDEMVDAMKNVAKLDVELTVEERNLLSVGYKNVI
>Glyc\_max.XP\_003544808 D1 8 244 PF00244.15 [14-3-3 protein] 14-3-3 Query: start 1 end 235
AERYEEMVEFMEKVSASaeSEELTVEERNLLSVAYKNVI
>Arab\_thal.NP\_567344 D1 10 246 PF00244.15 [14-3-3 protein] 14-3-3 Query: start 1 end 235
AERYEEMVEFMEKVAKAvdKDELTVEERNLLSVAYKNVI


# Details #

Alignment is simple. The script zips the sequences against each other and returns a truncated sequence with the highest sequence score (+2 for hit, -1 for miss). If entered sequence is greater that than the other fasta sequences, those with less  bp's than that of the entered value are flanked with -'s on each side and the program runs as follows.
# Introduction #

input:

`>> python.exe overlapCheck.py inputFILEtoREAD.tab outputFILE.tab

with optional flags/arguments:

>> python.exe overlapCheck.py inputFILEtoREAD.tab outputFILE.tab -d -l 1000
## Details ##

input format:

excel/tab delimited file, the columns should be arranged as follows

|Chromosome|Sequence Version|type|gene start|gene snd|any|any|gene Name|Old Sequence Version|
|:---------|:---------------|:---|:---------|:-------|:--|:--|:--------|:-------------------|

output:

returns a tab-delimited excel ready formatted list of overlapping sequences in the following order:

|Chromosome|Gene1|Gene2|Overlap Length|Overlap Start|Overlap End|
|:---------|:----|:----|:-------------|:------------|:----------|

Lsat\_1\_v6\_lg\_1  Lsa000223       Lsa000225       42352   1917404 1959756
Lsat\_1\_v6\_lg\_1  Lsa000239       Lsa000225       90041   1917404 2007445
Lsat\_1\_v6\_lg\_1  Lsa000239       Lsa000223       65366   1942079 2007445
Lsat\_1\_v6\_lg\_1  Lsa000237       Lsa000225       121470  1917404 2038874
Lsat\_1\_v6\_lg\_1  Lsa000237       Lsa000223       96795   1942079 2038874
Lsat\_1\_v6\_lg\_1  Lsa000237       Lsa000239       43627   1995247 2038874

## optional flags ##

| -d | inserts another column to deviate between perfectly aligning  sequences(i.e from different version), "OP" indicates a perfect alignment, "-" is the default filler|
|:---|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|

| -l | the "-l" option allows the user to filter out sequences with overlap lengths below a given threshold (i.e user input value following "-l" |
|:---|:------------------------------------------------------------------------------------------------------------------------------------------|


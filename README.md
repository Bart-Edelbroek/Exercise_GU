# Exercise_GU

To run the SequenceAnalyzer.py script, supply it with a 6-column text file with sequencing samples with header. Optionally a cutoff can be added which will define when to warn the user that too many sequences of a given species have failed. \
\
Example input: \
$ python SequenceAnalyzer.py -i samples.txt -c 0.12 \
\
Example output: \
Input file = samples.txt \
The total number of failed samples is  90  \
Warning: for the following species, more than  12.0  percent has failed: ['T', 'C', 'D', 'N'] 




Example of samples.txt with header: \
sample,pct_N_bases,pct_covered_bases,longest_no_N_run,num_aligned_reads,qc_pass \
DN-64554,3.91,96.07,7055,489499,TRUE \
DC-31756,4.14,95.93,7055,527966,TRUE \
DD-28879,4.32,95.68,9033,444775,TRUE \
DD-22466,3.63,96.37,7055,621979,TRUE \

Prerequisites: python3, pandas

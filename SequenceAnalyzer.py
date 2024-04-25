#!/usr/bin/env python
import pandas as pd
import argparse

def parse_input(file_in):
	#Function to parse the input file into a pandas dataframe. 
	#The first line will be used as a header, the other rows are looped over to fill the data and dataframe
	with open(file_in) as fin:
		print("Input file = "+str(file_in))
		data = []
		for i, line in enumerate(fin):
			if i == 0: #Take the first line and split it as the header
				header = line.strip('\n').split(",")
			if line[0] == "D": #Only consider valid lines (i.e. starting with species with D)
				row_data = {	# This could be changed to automatically read the given number of columns
					header[0] : line.strip('\n').split(",")[0],
					header[1] : line.strip('\n').split(",")[1],
					header[2] : line.strip('\n').split(",")[2],
					header[3] : line.strip('\n').split(",")[3],
					header[4] : line.strip('\n').split(",")[4],
					header[5] : line.strip('\n').split(",")[5]
				}
				data.append(row_data)
		df = pd.DataFrame(data)
	return df


def check_percentage(failed_samples,all_samples,cutoff):
	#Function to check the failed samples vs all samples and output which species failed more than the defined cutoff
	all_species = {} #Dict which holds all occured species and the number of each
	failed_species = {} #Dict which holds failed species and the number of each
	species_cutoff = [] #Ouput list with species over cutoff
	for species in all_samples.str[1].tolist():
		if species not in all_species:
			all_species[species] = 1
		else:
			all_species[species] += 1
	for species in failed_samples.str[1].tolist():
		if species not in failed_species:
			failed_species[species] = 1
		else:
			failed_species[species] += 1
	for species in failed_species:
		if (failed_species[species] / all_species[species]) > cutoff:
			species_cutoff.append(species)
	return species_cutoff


parser = argparse.ArgumentParser()
parser.add_argument("-i","--in_file", required=True, help="Input text file with samples and sequencing quality in 6 columns, the first line should be the header")
parser.add_argument("-c","--cutoff",  default=0.1, help="Cutoff for fraction of total per species that can fail before a warning is issued (default : 0.1)")
args = parser.parse_args()

file_in = args.in_file
cutoff = float(args.cutoff)

df = parse_input(file_in) #Input text file to pandas dataframe
df.pct_covered_bases = df.pct_covered_bases.astype(float) #Change string to float for covered bases

all_samples = df["sample"]

#Here the failed samples are defined. Please change these numbers according to the desired cutoffs
#New rules can be added for the remaining columns
failed_samples = df["sample"][(df["pct_covered_bases"] < 95.0) & (df["qc_pass"] == "FALSE")] 
print("The total number of failed samples is ",len(failed_samples))

species_cutoff = check_percentage(failed_samples,all_samples,cutoff)
if len(species_cutoff) > 0:
	print("Warning: for the following species, more than ",cutoff*100," percent has failed:",species_cutoff)

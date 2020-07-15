# -*- coding: utf-8 -*-
"""
Automatisation des tests pour le taux d apprentissage dans le but
d identifier la valeur maximale avant qu il y ait dérapage

@author: Jonathan Plourde

/home/jplou07/projects/def-fournier-ab/jplou07/Imagettes/TWI_D8/samples512_overlap70_min-annot10_1bands
"""
import sys
import getopt
import os
import numpy as np
import ruamel.yaml as yaml

def main(argv):

	dirpath = os.getcwd()
	inputfile = ''
	outputfile = ''
	dataImagettes = ''
	
	try:
            opts, args = getopt.getopt(argv,"hi:o:d:",["ifile=","ofile=,data="])
	except getopt.GetoptError:
            print ('test.py -i <inputfile> -o <outputfile> -data <typeindice>')
            sys.exit(2)
	for opt, arg in opts:
	    if opt == '-h':
                print ('test.py -i <inputfile> -o <outputfile> -data <typeindice>')
                sys.exit()
	    elif opt in ("-i", "--ifile"):
                inputfile = arg
	    elif opt in ("-o", "--ofile"):
	        outputfile = arg
	    elif opt in ("-d", "--data"):
	        dataImagettes = arg
	# Ouverture du fichier yaml
	with open(inputfile) as f:
	    params = yaml.load(f, Loader=yaml.Loader)
		
		# Changemement des parametres
	params['global']['data_path'] = dirpath+'/data/'+dataImagettes
	params['sample']['prep_csv_file'] = dirpath+'/data/'+dataImagettes+'/images_to_samples.csv'

	with open(outputfile, 'w') as fp:
	    yaml.dump(params, fp)

if __name__ == "__main__":
    main(sys.argv[1:])

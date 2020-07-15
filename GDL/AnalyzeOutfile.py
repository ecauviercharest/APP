# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 11:04:35 2020

@author: Jonathan Plourde
"""

import argparse
import sys
import os
import getopt

import ruamel_yaml as yaml
import pandas as pd
import matplotlib.pyplot as plt

def getYamlinfo(inputd):
	data = {}
	for root, dirs, files in os.walk(inputd):

		for file in files:
			if file.endswith(".yaml"):
				inputfile = os.path.join(root, file)			   
				with open(inputfile) as f:
					params = yaml.load(f, Loader=yaml.Loader)
					foldername = root.split("\1m")[-1][1:]
					try:
						testID = int(foldername.split('_')[1])
					except IndexError:
						testID = foldername[-7:]
					data[testID]={
						'Indice':params['global']['data_path'].split('/')[-1],
						'Number of Classes':params['global']['num_classes'],
						'Number of GPUs': params['global']['num_gpus'],
						'Number of Bands': params['global']['number_of_bands'],
						'Overlap': params['sample']['overlap'],
						'Batch Size' :params['training']['batch_size'],
						'Class Weights' :params['training']['class_weights'], 
						'Gamma' :params['training']['gamma'], 
						'Learning Rate' :params['training']['learning_rate'],
						'Number of Epochs' :params['training']['num_epochs'],
						'Step Size' :params['training']['step_size'],
						'Weight Decay':params['training']['weight_decay'],
						'Dropout':params['training']['dropout'],
						'Dropout Probability':params['training']['dropout_prob']
						}
	return (data)
def getloginfo(inputd,yamldic):
	for root, dirs, files in os.walk(inputd):
		for file in files:
			if file.endswith(".log"):
				inputfile = os.path.join(root, file)
				with open(inputfile) as f:
					foldername = root.split("\1m")[-1][1:]
					try:
						testID = int(foldername.split('_')[1])
					except IndexError:
						testID = foldername[-7:]
					
					log = f.readlines()
					name = file.replace('.log','')
					
					info = []
					noclass = []
					for line in log:
						cols = line.split('\t')
						try:
							stat = float(cols[-1].replace('\n', ''))
							vclass = str(cols[-2].replace('\n', ''))
						except ValueError:
							stat = None
						info.append(stat)
						noclass.append(vclass)
					if name == 'progress':
						try:
							yamldic[testID][name+'_Total'] = int(info[-1] - info[1])
						except:
							print (testID)
					elif name== 'metric_val_loss':
						try:
							yamldic[testID][name]=info[-1]
						except IndexError:
							yamldic[testID][name]=None
					elif name== 'metric_trn_loss':
						try:
							yamldic[testID][name]=info[-1]
						except IndexError:
							yamldic[testID][name]=None 
					elif name== 'metric_classwise_val_fscore':
						yamldic[testID]['val_fscore_Class_0']=0
						yamldic[testID]['val_fscore_Class_1']=0
						yamldic[testID]['val_fscore_Class_2']=0
						yamldic[testID]['val_fscore_Class_3']=0
						yamldic[testID]['val_fscore_Class_4']=0
						for num, val in zip(noclass, info):
							yamldic[testID]['val_fscore_Class_'+str(num)]+= val

						yamldic[testID]['val_fscore_Class_0']/=(yamldic[testID]['Number of Epochs'])
						yamldic[testID]['val_fscore_Class_1']/=(yamldic[testID]['Number of Epochs'])
						yamldic[testID]['val_fscore_Class_2']/=(yamldic[testID]['Number of Epochs'])
						yamldic[testID]['val_fscore_Class_3']/=(yamldic[testID]['Number of Epochs'])
						yamldic[testID]['val_fscore_Class_4']/=(yamldic[testID]['Number of Epochs'])
						try :
							if noclass[-1] == '2':
								yamldic[testID]['Last_val_fscore_Class_1'] = info[-2]
								yamldic[testID]['Last_val_fscore_Class_2']= info[-1]
							else:
								yamldic[testID]['Last_val_fscore_Class_1'] = info[-4]
								yamldic[testID]['Last_val_fscore_Class_2']= info[-3]
						except IndexError:
							yamldic[testID]['Last_val_precision_Class_2']=None
							yamldic[testID]['Last_val_precision_Class_1']=None
					elif name == 'metric_classwise_val_precision':
						try:
							if noclass[-1] == '2':
								yamldic[testID]['Last_val_precision_Class_1'] = info[-2]
								yamldic[testID]['Last_val_precision_Class_2']= info[-1]
							else:
								yamldic[testID]['Last_val_precision_Class_1'] = info[-4]
								yamldic[testID]['Last_val_precision_Class_2']= info[-3]
						except IndexError:
							yamldic[testID]['Last_val_precision_Class_2']=None
							yamldic[testID]['Last_val_precision_Class_1']=None
					elif name== 'metric_val_fscore_averaged':
						try:
							yamldic[testID][name]=info[-1]
						except IndexError:
							yamldic[testID][name]=None
					elif name== 'metric_val_precision_averaged':
						try:
							yamldic[testID][name]=info[-1]
						except IndexError:
							yamldic[testID][name]=None
						
def main(argv):
	
	#inputd = 'P:\Hiv2020\APPJO\Results\1m'
	inputd = "I:\Jonathan\Documents\APPJO\Results"
	#outputd = ''
	outputd = 'I:\Jonathan\Documents\APPJO\Excel\Results_Previous.xlsx'
	
#	try:
#		opts, args = getopt.getopt(argv,"hi:o:d:",["ifile=","ofile=,data="])
#	except getopt.GetoptError:
#		print ('test.py -i <inputdir> -o <outputdir> -d <typeindice>')
#		sys.exit(2)
#	for opt, arg in opts:
#		if opt == '-h':
#			print ('test.py -i <inputDir> -o <outputDir> -d <typeindice>')
#			sys.exit()
#		elif opt in ("-i", "--ifile"):
#			inputd = arg
#		elif opt in ("-o", "--ofile"):
#			outputd = arg
#		elif opt in ("-d", "--data"):
#			test = arg
	
	yamldic = getYamlinfo(inputd)
	getloginfo(inputd,yamldic)
	yamldata = pd.DataFrame.from_dict(yamldic, orient='index')
	writer = pd.ExcelWriter(outputd, engine='xlsxwriter')
	
	#yamldata.style.bar(subset=['Number of Classes', 'Number of Epochs', 'Step Size'], color='#d65f5f')
	yamldata.to_excel(writer, sheet_name='Results')
	workbook = writer.book
	worksheet = writer.sheets['Results']
	worksheet.conditional_format('P2:P135', {'type': '3_color_scale'})
	worksheet.conditional_format('Q2:Q135', {'type': '3_color_scale'})
	worksheet.conditional_format('T2:T135', {'type': '3_color_scale'})
	worksheet.conditional_format('S2:S135', {'type': '3_color_scale'})
	worksheet.conditional_format('R2:R135', {'type': '3_color_scale'})
	worksheet.conditional_format('V2:V135', {'type': '3_color_scale'})
	worksheet.conditional_format('X2:X135', {'type': '3_color_scale'})
	worksheet.conditional_format('U2:U135', {'type': '3_color_scale'})
	worksheet.conditional_format('Z2:Z135', {'type': '3_color_scale'})
	worksheet.conditional_format('W2:W135', {'type': '3_color_scale'})
	worksheet.conditional_format('AB2:AB135', {'type': '3_color_scale'})
	worksheet.conditional_format('AC2:AC135', {'type': '3_color_scale'})
	
	worksheet.conditional_format('Y2:Y135', {'type': '3_color_scale',
											'min_color':'#77fa6b',
											'mid_color':'#faf56b',
											'max_color':'#ff6242'})
	worksheet.conditional_format('AA2:AA135', {'type': '3_color_scale',
											'min_color':'#77fa6b',
											'mid_color':'#faf56b',
											'max_color':'#ff6242'})
	writer.save()
	
if __name__ == "__main__":
	main(sys.argv[1:])

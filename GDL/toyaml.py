import os
#import ruamel_yaml as yaml
import ruamel.yaml as yaml
import pandas as pd
import glob
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

#PATH TO CHANGE
#ShellDir = r"I:\Jonathan\Documents\\APPJO\Script\ComputeCanada\Shell"
#ConfDir = r"I:\Jonathan\Documents\APPJO\conf"
#ImageDir = r"I:\Jonathan\Documents\APPJO\Imagettes"
#ResultDir = r"I:\Jonathan\Documents\APPJO\Results"
#pathexcelFile=r"I:\OneDrive - USherbrooke\APP\GDL\EXCEL\Trainning.xlsx"

ShellDir = "/home/jplou07/projects/def-fournier-ab/jplou07/script/Shell"
ConfDir = "/home/jplou07/projects/def-fournier-ab/jplou07/conf"
ImageDir = "/scratch/jplou07/Imagettes"
ResultDir = "/home/jplou07/scratch/results"
pathexcelFile= "/home/jplou07/projects/def-fournier-ab/jplou07/Excel/Trainning.xlsx"

def exceltoyaml():
    
    data_xls = pd.read_excel(pathexcelFile, 'Yamlinfo', index_col=0, header=1, na_filter=False)
    listImageName = [os.path.basename(filepath).replace(".tar","") for filepath in glob.glob(os.path.join(ImageDir,'*.tar'))]
    confIDList = [os.path.basename(filepath).split('_')[0] for filepath in glob.glob(os.path.join(ConfDir,'*_config.yaml'))]

    for row in data_xls.iterrows():
        
        if row[1]['Status']== 'Completed':
            continue
        elif row[1]['Status'] == 'In progress':
            #check if id folder in results
            continue


        
        if row[1]["Indice"] not in listImageName:
            print (row[1]["Indice"], ' - unavailable Indice')
            continue

        if str(row[0]) in confIDList:
            continue
        outFilename = str(row[0])+'_'+row[1]["Indice"]+'_config.yaml'
        outputfile= os.path.join(ConfDir,outFilename)
        if "2_classes" in row[1]["Indice"]:
            NBClasses =2 
        elif "4_classes" in row[1]["Indice"]:
            NBClasses =4 
        elif "1_classes" in row[1]["Indice"]:
            NBClasses =1
        else:
            NBClasses =4 
        yamlDefault = os.path.join(ConfDir,'config_default_'+str(NBClasses)+'Classes.yaml')
        with open(yamlDefault) as f:
            params = yaml.load(f, Loader=yaml.Loader)

        params['global']['data_path']=row[1]["Indice"]
        params['global']['model_name']=row[1]["model_name"]
        params['global']['num_classes'] = NBClasses
        params['global']['num_gpus']=row[1]["num_gpus"]
        params['global']['number_of_bands']=row[1]["number_of_bands"]
        params['training']['batch_size']=row[1]["batch_size"]
        
        if row[1]['class_weights'] != '':
            params['training']['class_weights']=row[1]["class_weights"]
        	
        if row[1]['dropout'] == '':
            params['training']['dropout']=False
        else:
        	params['training']['dropout']=row[1]["dropout"]
    
        if row[1]['dropout_prob'] != '':
        	params['training']['dropout_prob']=row[1]["dropout_prob"]

        params['training']['gamma']=row[1]["gamma"]
        params['training']['learning_rate']=row[1]["learning_rate"]
        params['training']['loss_fn']=row[1]["loss_fn"]
        params['training']['num_epochs']=row[1]["num_epochs"]
        params['training']['optimizer']=row[1]["optimizer"]

        if row[1]['step_size'] != '':
        	params['training']['step_size']=row[1]["step_size"]
    
        if row[1]['weight_decay']!='':
        	params['training']['weight_decay']=row[1]["weight_decay"]

        with open(outputfile, 'w') as fp:
            yaml.dump(params, fp)
        
        if row[1]['Days'] != '':
            valueDays = row[1]["Days"]
        else:
            valueDays=1

        createBashFile(row[1]["Indice"], row[0], row[1]["num_gpus"], valueDays, row[1]["number_of_bands"])

def createBashFile(testData, testid, numGPUs, Days, nbBands):
    #path default
    pathDefault = os.path.join(ShellDir,"default_file.sh")
    defaultFile =  open(pathDefault, 'r')
    infoDefault = defaultFile.readlines()
    #change path in bash file
    infoDefault[10] = 'DATA='+testData+'\n'
    infoDefault[11] = 'CONF='+str(testid)+'_'+testData+"_config"+'\n'
    infoDefault[3] = "#SBATCH --gres=gpu:"+ str(numGPUs)+'\n'
    infoDefault[8] = "#SBATCH --time="+str(Days)+"-00:00\n"
    infoDefault[14] = 'BANDS=samples512_overlap70_min-annot10_'+str(nbBands)+'bands\n'
	infoDefault[31] = 'NoTEST='+str(testid)+'_$SLURM_JOB_ID\n'
    #creating bash file
    
    pathBashFile = os.path.join(ShellDir, testData+"_"+str(testid)+".sh")
    bashFile =  open(pathBashFile, 'w')
    bashFile.write(''.join(infoDefault))
    defaultFile.close()
    bashFile.close()

    #Sending bash file to scheduler
    time.sleep(30)
    cmd = 'sbatch '+pathBashFile
    print (cmd)
    os.system(cmd)

# class MyEventHandler(PatternMatchingEventHandler):
#     def on_modified(self, event):
#         super(MyEventHandler, self).on_modified(event)
#         exceltoyaml()
        

# watched_dir = os.path.split(pathexcelFile)[0]
# print ('watched_dir = {watched_dir}'.format(watched_dir=watched_dir))
# patterns = [pathexcelFile]
# event_handler = MyEventHandler(patterns=patterns)
# observer = Observer()
# observer.schedule(event_handler, watched_dir, recursive=True)
# observer.start()
# try:
#     while True:
#         time.sleep(10)
# except KeyboardInterrupt:
#     observer.stop()
# observer.join()


exceltoyaml()

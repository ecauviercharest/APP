import sys, glob, os, sys
import logging, getopt
import subprocess
import configparser
import whitebox
from shutil import copyfile, copy

'''
logger = logging.getLogger('gmq580')
logger.setLevel(logging.DEBUG)

logger.info("Process starts")
logger.error("Params is Null")

# fichier
fh = logging.FileHandler('C:\temp\gmq580.log')
# à l'écran
ch = logging.StreamHandler()
#

Conserver les paramètres de mon
application dans un fichier config (une
sorte de fichier .ini)
● Il peut être intéressant de disposer d’un
fichier .ini qui sera lu au départ de
l’application (config parser)

'''

outputdir = ""
inputdir = ""
typeIT = "D8"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:o:t:", ["help", "directory", "output", "type"])
except:
    print("for help use --help")
    propertiesfiles, outputdir = "", ""
for o, a in opts:
    if o in ("-h", "--help"):
        print("")
        print("Bienvenue dans l'aide. Pour produire un indice, svp rédiger la commande au format suivant:")
        print("nomduscript.py -d path/to/input/directory/ -o path/to/output/directory/ -t type d'indice voulu")
        print("Le type d'indice est soit : D8, FD8 ou Dinf. D8 est l'indice par défaut si aucun n'est spécifié.")
    elif o in ("-d", "--directory"):
        inputdir = a
    elif o in ("-o", "--output"):
        outputdir = a
    elif o in ("t", "--type"):
        typeIT = a

# définir le log et son format
logger = logging.getLogger('IT')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(outputdir + '\IT.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(message)s (call: %(module)s-%(funcName)s)')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

wbt = whitebox.WhiteboxTools()


def D8(dossier, img, directory):
    wbt.set_working_dir(directory)
    wbt.verbose = False

    imgpath = os.path.join(dossier, img)
    try:
        copyfile(imgpath, directory + img)
        logger.info("File copied : " + directory + img)
    except IOError as e:
        logger.error("Unable to copy file. %s" % e)
    except:
        logger.error("Unexpected error:", sys.exc_info())

    imgFile = os.path.splitext(img)[0]
    imgName = imgFile[4:]
    logger.debug("img =" + img)
    logger.debug("breach depression path = D8_" + imgName + "_breached.tif")
    try:
        wbt.breach_depressions(img, "D8_" + imgName + "_breached.tif")
        logger.info("DEM has been breached." + directory + img)
    except:
        logger.error("Unexpected error:", sys.exc_info())
    wbt.slope(img, "D8_" + imgName + "_slope.tif")
    wbt.d8_flow_accumulation("D8_" + imgName + "_breached.tif", "D8_" + imgName + "flow_acc.tif",
                             'specific contributing area')

    wbt.wetness_index("D8_" + imgName + "flow_acc.tif", "D8_" + imgName + "_slope.tif", "TWI_D8_" + imgName + ".tif")
    os.remove(directory + img)
    os.remove(directory + "D8_" + imgName + "_breached.tif")
    os.remove(directory + "D8_" + imgName + "_slope.tif")
    os.remove(directory + "D8_" + imgName + "flow_acc.tif")


def Dinf(dossier, img, directory):
    wbt.set_working_dir(directory)
    wbt.verbose = False
    imgpath = dossier + img
    copyfile(imgpath, directory + img)

    imgFile = os.path.splitext(img)[0]
    imgName = imgFile[4:]

    wbt.breach_depressions(img, "D8_" + imgName + "_breached.tif")
    wbt.slope(img, "D8_" + imgName + "_slope.tif")
    wbt.d_inf_flow_accumulation("D8_" + imgName + "_breached.tif", "Dinf_" + imgName + "flow_acc.tif",
                                'specific contributing area')
    wbt.wetness_index("Dinf_" + imgName + "flow_acc.tif", "D8_" + imgName + "_slope.tif",
                      "TWI_Dinf_" + imgName + ".tif")
    os.remove(directory + img)
    os.remove(directory + "D8_" + imgName + "_slope.tif")
    os.remove(directory + "D8_" + imgName + "_breached.tif")
    os.remove(directory + "Dinf_" + imgName + "flow_acc.tif")


def fD8(dossier, img, directory):
    wbt.set_working_dir(directory)
    wbt.verbose = False
    imgpath = dossier + img
    copyfile(imgpath, directory + img)
    imgFile = os.path.splitext(img)[0]
    imgName = imgFile[4:]
    wbt.breach_depressions(img, "D8_" + imgName + "_breached.tif")
    wbt.slope(img, "D8_" + imgName + "_slope.tif")
    wbt.d_inf_flow_accumulation("D8_" + imgName + "_breached.tif", "FD8_" + imgName + "flow_acc.tif",
                                'specific contributing area')
    wbt.wetness_index("FD8_" + imgName + "flow_acc.tif", "D8_" + imgName + "_slope.tif", "TWI_FD8_" + imgName + ".tif")
    os.remove(directory + img)
    os.remove(directory + "D8_" + imgName + "_slope.tif")
    os.remove(directory + "D8_" + imgName + "_breached.tif")
    os.remove(directory + "FD8_" + imgName + "flow_acc.tif")

def main():
    #dossier = r'F:/Jonathan/APP_Jonathan/MNT/Reproj/Chapeau/'
    # dossier = r'G:/Hiv2020/APPJO/MNT/TEST/'
    inputdirectory = os.path.abspath(inputdir)
    listeMNT = glob.glob(inputdir + '/' + '*.tif')

    for imgpath in listeMNT:
        filename = os.path.basename(imgpath)
        print(filename)

        if typeIT == 'D8':
            logger.info("Processing " + filename + " using " + typeIT + " method...")
            D8(inputdirectory, filename, outputdir)

        elif typeIT == 'Dinf':
            logger.info("Processing " + filename + "using " + typeIT + " method...")
            Dinf(inputdirectory, filename, r'F:/Elizabeth/Production_IT/1m_resolution/TWI/Chapeau/Dinf/')

        elif typeIT == 'FD8':
            logger.info("Processing " + filename + "using " + typeIT + " method...")
            fD8(inputdirectory, filename, r'F:/Elizabeth/Production_IT/1m_resolution/TWI/Chapeau/FD8/')

        print('Méthode D8 en cours...')



main()

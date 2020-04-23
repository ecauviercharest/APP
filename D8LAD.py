# Script Name: DinfFlowDirection
#
# Created By:  David Tarboton
# Date:        9/23/11

# Import ArcPy site-package and os modules
import os
import subprocess
import glob
import time
import math
import numpy as np
from osgeo import gdal, osr
'''
# DinfFLowDirection('F:\Hiv2020\APP - Jonathan\MNT', 'F:\Hiv2020\APP - Jonathan\MNT\PROJ2M')
def DinfFLowDirection(o_local_dir, i_dir_elevation):
    dir_fel = glob.glob(os.path.join(i_dir_elevation, '*\*.tif'))

    for fel in dir_fel:
        print(os.path.basename(fel))

        # Input Number of Processes
        inputProc = str(8)

        # Outputs
        outfileName = fel.split("\Reproj")[-1][1:]

        ang = os.path.join(o_local_dir, 'Dir', outfileName)

        slp = os.path.join(o_local_dir, 'slope', outfileName)
        print(slp)
        # Construct command
        cmd = 'mpiexec -n ' + inputProc + ' DinfFlowDir -fel ' + '"' + fel + '"' + ' -ang ' + '"' + ang + '"' + \
              ' -slp ' + '"' + slp + '"'

        # Submit command to operating system
        os.system(cmd)

        # Capture the contents of shell command and print it to the arcgis dialog box
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        print("Happens while running")

        message = "\n"
        for line in process.stdout.readlines():
            if isinstance(line, bytes):  # true in Python 3
                line = line.decode()
            message = message + line
            print(message)
        time.sleep(60)


# DinfFlowArea('F:\Hiv2020\APP - Jonathan\MNT', 'F:\Hiv2020\APP - Jonathan\MNT\PROJ2M')
def DinfFlowArea(o_local_dir, i_dir_elevation):
    dir_ang = glob.glob(os.path.join(i_dir_elevation, '*\*.tif'))

    for ang in dir_ang:
        print(os.path.basename(ang))
        # Input Number of Processes
        inputProc = str(8)

        # Output
        outfileName = ang.split("\Reproj")[-1][1:]
        sca = os.path.join(o_local_dir, outfileName)

        # Construct command
        cmd = 'mpiexec -n ' + inputProc + ' AreaDinf -ang ' + '"' + ang + '"' + ' -sca ' + '"' + sca + '"'

        # Submit command to operating system
        os.system(cmd)

        # Capture the contents of shell command and print it to the arcgis dialog box
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        message = "\n"
        for line in process.stdout.readlines():
            if isinstance(line, bytes):  # true in Python 3
                line = line.decode()
            message = message + line


DinfFLowDirection(r"G:\TWI\D8LAD", 'D:\Jonathan\APP_Jonathan\MNT\Reproj')
DinfFlowArea(r'G:\TWI\D8LAD', 'D:\Jonathan\APP_Jonathan\MNT\Reproj')
'''
def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array

def array2raster(newRasterfn, rasterfn, array):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = array.shape[1]
    rows = array.shape[0]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Byte)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

def TWI(slopefile, flowaccfile):
    slope = raster2array(slopefile)
    flowacc = raster2array(flowaccfile)
    calcul1 = flowacc + 1 // (slope/100) + 1
    calcul2 = np.log(calcul1)
    #print(calcul2[20:30])
    return calcul2


path = r'D:/Jonathan/APP_Jonathan/MNT/Reproj/Chapeau/'
MNTlist = glob.glob(path + '*.tif', recursive=True)
outputdir = 'G:/TWI/Chapeau/D8LAD/'

for MNTpath in MNTlist:
    filename = os.path.basename(MNTpath)
    print(filename)
    outfileName = 'TWI_D8LAD_' + filename[4:]
    outputpath = os.path.join(outputdir, outfileName)

    slope = 'G:/TWI/D8LAD/slope/Chapeau/' + filename
    flowacc = 'G:/TWI/D8LAD/Dir/Chapeau/' + filename

    ITarray = TWI(slope, flowacc)

    array2raster(outputpath, MNTpath, ITarray)


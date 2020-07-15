import numpy as np
from osgeo import gdal

'''
tan alphad = d / Ld 
où d = elevation (m) 
Ld = horizontal distance to the point with an elevation d meters below the elevation of the starting cell 
following the steepest-direction flow path
'''


def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array


def find_nearest(array, value):
    a = np.asarray(array)
    at = a.transpose()
    # idx = np.unravel_index(np.argmin(a, axis=None), a.shape)
    idx1 = np.unravel_index(np.argmin(np.abs(a - value), axis=None), a.shape)
    idx2 = np.unravel_index(np.argmin(np.abs(at - value), axis=None), at.shape)
    dist1 = np.sqrt(idx1[0] ** 2 + idx1[1] ** 2)
    dist2 = np.sqrt(idx2[0] ** 2 + idx2[1] ** 2)
    if dist1 < dist2:
        idx = idx1
    else:
        idx = idx2[1], idx2[0]
    return idx


def Hjerdt(d, Ld):
    calcul = d / Ld
    return calcul


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


def createIT(array, d):
    IT = []
    for i in range(len(array)):
        row = []
        for j in range(len(array[0])):
            value = array[i][j] - d
            index = find_nearest(array, value)
            x, y = index[0], index[1]
            dist = np.sqrt((i - x) ** 2 + (j - y) ** 2)
            row.append(Hjerdt(5, dist))
        print('done: ', (count / len(array)))
        IT.append(row)
        print(IT)
    return IT


def main(MNTpath, outputPathfn, d):
    MNTarray = raster2array(MNTpath)  # creates array from MNT
    Hjerdtarray = createIT(MNTarray, d)
    # Hjerdtarray = createPath(MNTpath, MNTarray, startCoord, stopCoord) # creates path array
    array2raster(outputPathfn, MNTpath, Hjerdtarray)  # converts IT array to raster


if __name__ == "__main__":
    # MNTpath = 'D:/Jonathan/APP_Jonathan/MNT/Reproj/Chapeau/MNT_CH_18_13w109.tif'
    MNTpath = r'C:/Users/caue3201/Desktop/test.tif'
    outputPathfn = r'C:/Users/caue3201/Desktop/test_result.tif'
    d = 5
    main(MNTpath, outputPathfn, d)

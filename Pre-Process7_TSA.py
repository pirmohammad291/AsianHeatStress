# Basically, this takes a folder of 2D-raster, stacks them, and then returns new rasters
# containig pixel-by-pixel trend analyses along the 3rd axis (r-value, slope, etc.)
import os, gdal
import numpy as np
from gdalconst import *
from scipy import stats
import scipy

# Function that reads an entire folder of rasters as arrays and stores them in a list, 
# default raster input format is GeoTiff
# printOut is only used to debug the code
def tiffToarray(inFol, printOut = False, inFormat = "tif"):
    # Use the first raster as a blueprint for the raster size of all rasters
    for allRasters in os.listdir(inFol):
        if allRasters[-3:] == "tif":
            firstRasStr = inFol + allRasters
            break
    firstRasGDAL = gdal.Open(firstRasStr, GA_ReadOnly)   
    cols = firstRasGDAL.RasterXSize
    rows = firstRasGDAL.RasterYSize        
    finList = [] # initialise list that will store all arrays to be returned in the end
    for files in os.listdir(inFol):
        if files[-3:] == inFormat:
            if printOut:
                print(files)            
            fileIn = inFol + files 
            dataset = gdal.Open(fileIn, GA_ReadOnly)
            array = dataset.ReadAsArray(0, 0, cols, rows)            
            finList.append(array)            
    return finList

# Function that calculates linear regression and Mann-Kendall-pValue coefficients for each raster pixel against continous time steps
# Input must be a list of arrays
# Benchmark: a time series of 15 rasters, with each having 321x161 pix (51681), the entire process takes
# about 19.1 seconds in total, with 5.8s for linReg and 13.2s for MK
def linReg(inList):    
    #equally spaced time steps by length of inList    
    timeList = np.asarray(list(range(len(inList))))
    stepLen = len(inList)
    #stack input arrays to make a 3D array
    dstack = np.dstack((inList))    
    dstack1D = dstack.reshape(-1)
    # Break down dstack1D into a list, each element in list contains the single steps
    # of one pixel -> List length is equal to number of pixels
    # List can be used to use Pythons map() function
    dstackList = [dstack1D[i:i+stepLen] for i in range(0, len(dstack1D), stepLen)]
    #initialise empty arrays to be filled by output values, arrays are 1D
    slopeAr,intcptAr,rvalAr,pvalAr,stderrAr,mkPAr,mkZAr,mkTrendAr, PercAr = [np.zeros(inList[0].reshape(-1).shape) for _ in range(9)]    
    # Use map() to iterate over each pixels timestep values for linear reg and Mann.Kendall
    # Method is about 10% faster than using 2 for-loops (one for x- and y-axis)
    outListReg = list(map( (lambda x: scipy.stats.linregress(timeList, x)) , dstackList))    
    outListMK = list(map( (lambda x: mk_test(x)) , dstackList)) 
    outListPR = list(map( (lambda x: np.percentile(x, 90)) , dstackList))            
    for k in range(len(outListReg)):
        slopeAr[k] = outListReg[k][0]
        intcptAr[k] = outListReg[k][1]
        rvalAr[k] = outListReg[k][2]
        pvalAr[k] = outListReg[k][3]
        stderrAr[k] = outListReg[k][4]        
        mkPAr[k] = outListMK[k][0]   # 0 for p; 1 for h; 2 for z; 3 for Sen's trend
        mkZAr[k] = outListMK[k][2]
        mkTrendAr[k] = outListMK[k][3]
        PercAr [k] = outListPR[k]
    
    outShape = inList[0].shape
    outTuple = (slopeAr.reshape(outShape), 
                intcptAr.reshape(outShape), 
                rvalAr.reshape(outShape), 
                pvalAr.reshape(outShape), 
                stderrAr.reshape(outShape),
                mkPAr.reshape(outShape),
                mkZAr.reshape(outShape),
                mkTrendAr.reshape(outShape),
                PercAr.reshape(outShape))                
    return outTuple

# Mann-Kendall-Test
# Originally from: http://www.ambhas.com/codes/statlib.py
# I've changed the script though, now its about 35x faster than the original (depending on time series length
# Input x must be a 1D list/array of numbers
def mk_test(x, alpha = 0.05):    
    n = len(x)     
    # calculate S    
    listMa = np.matrix(x)               # convert input List to 1D matrix
    subMa = np.sign(listMa.T - listMa)  # calculate all possible differences in matrix
                                        # with itself and save only sign of difference (-1,0,1)
    s = np.sum( subMa[np.tril_indices(n,-1)] ) # sum lower left triangle of matrix
    # calculate the unique data
    # return_counts=True returns a second array that is equivalent to tp in old version    
    unique_x = np.unique(x, return_counts=True)
    g = len(unique_x[0])

    # calculate the var(s)
    if n == g: # there is no tie
        var_s = (n*(n-1)*(2*n+5))/18
    else: # there are some ties in data       
        tp = unique_x[1]        
        var_s = (n*(n-1)*(2*n+5) + np.sum(tp*(tp-1)*(2*tp+5)))/18
    
#    # Detrend
#    t = stats.theilslopes(x)
#    xx = range(1, n+1)
#    v_detrend = x - np.multiply(xx, t[0])
#    
#    # Account for Autocorrelation
#    I = np.argsort(v_detrend)
#    d = n*np.ones(2*n-1)
#    acf = (np.correlate(I, I, 'full')/d)[n-1:]
#    acf = acf/acf[0]
#    interval = stats.norm.ppf(1-alpha/2)/np.sqrt(n)
#    u_bound = 0+interval
#    l_bound = 0-interval
#    
#    sni=0
#    for i in range(1, n-1):
#        if (acf[i] > u_bound or acf[i] < l_bound):
#            sni += (n-i)*(n-i-1)*(n-i-2)*acf[i]
#    n_ns = 1+(2/(n*(n-1)*(n-2)))*sni
#    var_s = var_s*n_ns   
        
    if s>0:
        z = (s - 1)/np.sqrt(var_s)
    elif s == 0:
            z = 0
    elif s<0:
        z = (s + 1)/np.sqrt(var_s)    
    # calculate the p_value
    p = 2*(1-scipy.stats.norm.cdf(abs(z))) # two tail test
    h = abs(z) > scipy.stats.norm.ppf(1-alpha/2)
    
    # Sen's Slope
    q = []
    for row in range(0, len(x)+1):
        for col in range(row+1, len(x)):
            q.append((x[col] - x[row])/(col-row))

    sort = np.sort(q)
    trend = 0
    
    temp1 = int(len(sort)/2)
    temp2 = int((len(sort)+2)/2)
    
    if ((len(sort)%2)==0):
        trend = (sort[temp1]+sort[temp2])/2
    else:
        trend =  sort[temp1]
    
    return p,h,z,trend

# Function that converts a numpy array to a GeoTIFF and saves it to disk, needs an existing GeoTIFF file as a blueprint
# Changed after the original
# http://gis.stackexchange.com/questions/58517/python-gdal-save-array-as-raster-with-projection-from-other-file
# inTiff  is an exisiting GeoTiff file, the attributes from this file are used to create the output
# array    is the array that will be saved as a tiff   
# outFile  is the path and name of the desired output GeoTiff
def array_to_raster(inTiff,array,outFile):    
    inDataset = gdal.Open(inTiff, GA_ReadOnly)
    # You need to get those values like you did.
    x_pixels = inDataset.RasterXSize  # number of pixels in x
    y_pixels = inDataset.RasterYSize  # number of pixels in y
    PIXEL_SIZE = inDataset.GetGeoTransform()[1]   # size of the pixel...        
    x_min = inDataset.GetGeoTransform()[0] 
    y_max = inDataset.GetGeoTransform()[3]   # x_min & y_max are like the "top left" corner.
    wkt_projection = inDataset.GetProjectionRef()
    driver = gdal.GetDriverByName('GTiff')
    outDataset = driver.Create(
        outFile,
        x_pixels,
        y_pixels,
        1,
        gdal.GDT_Float32, )
    outDataset.SetGeoTransform((
        x_min,    # 0
        PIXEL_SIZE,  # 1
        0,                      # 2
        y_max,    # 3
        0,                      # 4
        -PIXEL_SIZE))
    outDataset.SetProjection(wkt_projection)
    outDataset.GetRasterBand(1).WriteArray(array)
    outDataset.FlushCache()  # Write to disk.
    return outDataset, outDataset.GetRasterBand(1)  #If you need to return, remember to return also the dataset because the band don`t live without dataset

################## USAGE EXAMPLE ####################
# Take rasters with annual values and return statistical time series trend indices
inFol = r"E:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\historical_1990-2015\Mktest\\"       # Input folder containing GeoTiffs 

outFol = r"E:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\historical_1990-2015\Mktest\Trend\\"    # Output folder, will contain statistical GeoTiffs after script is run
if not os.path.exists(outFol):
    os.makedirs(outFol)
    
inArrays = tiffToarray(inFol) #convert GeoTiffs to numpy arrays
outTuple = linReg(inArrays)   #run linear regression and return arrays of slope, r etc. as a tuple

# get first raster in list and use it as a blueprint for size etc. 
for allRasters in os.listdir(inFol):
        if allRasters[-3:] == "tif":
            firstRasStr = inFol + allRasters
            break
# define the names of the statistical output rasters
outNames = ("An_slope.tif", "An_intcp.tif", "An_rval.tif", "An_pval.tif", "An_stderr.tif","An_mkP.tif","An_mkZ.tif","An_mktrend.tif", "An_Percn90.tif")
# convert the arrays back to rasters and save them to disk
for fname, i in zip(outNames, range(len(outNames))):
    array_to_raster(firstRasStr,outTuple[i],outFol+fname)

import arcpy, sys, os
from arcpy import env
import numpy as np
from xlwt import Workbook, Formula
import xlrd
from arcpy.sa import *
import tkFileDialog                     
import Tkinter

global data_path
data_path = r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp126_2026-2100\tasmax\\"
data_path1=data_path+"ACCESS-CM2\Raster\\"
data_path2=data_path+"ACCESS-ESM1-5\Raster\\"
data_path3=data_path+"AWI-CM-1-1-MR\Raster\\"
data_path4=data_path+"BCC-CSM2-MR\Raster\\"
data_path5=data_path+"CanESM5\Raster\\"
data_path6=data_path+"CMCC-ESM2\Raster\\"
data_path7=data_path+"EC-Earth3\Raster\\"
##data_path8=data_path+"EC-Earth3-AerChem\Raster\\"
##data_path9=data_path+"EC-Earth3-CC\Raster\\"
data_path10=data_path+"EC-Earth3-Veg\Raster\\"
data_path11=data_path+"EC-Earth3-Veg-LR\Raster\\"
data_path12=data_path+"FGOALS-g3\Raster\\"
##data_path13=data_path+"GFDL-CM4\Raster\\"
data_path14=data_path+"GFDL-ESM4\Raster\\"
data_path15=data_path+"INM-CM4-8\Raster\\"
data_path16=data_path+"INM-CM5-0\Raster\\"
data_path17=data_path+"IPSL-CM6A-LR\Raster\\"
data_path18=data_path+"KACE-1-0-G\Raster\\"
data_path19=data_path+"MIROC6\Raster\\"
##data_path20=data_path+"MPI-ESM1–2-HR\Raster\\"
data_path21=data_path+"MPI-ESM1-2-LR\Raster\\"
data_path22=data_path+"MRI-ESM2-0\Raster\\"
data_path23=data_path+"NESM3\Raster\\"
data_path24=data_path+"NorESM2-LM\Raster\\"
data_path25=data_path+"NorESM2-MM\Raster\\"
data_path26=data_path+"TaiESM1\Raster\\"
save_path=data_path+"0_Ensemble_Mean\\"
if not os.path.exists(save_path):
    os.makedirs(save_path)
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace = data_path1
RasterList=arcpy.ListRasters()
for ras in RasterList:
    if not os.path.exists(save_path+ras):
        raster1=arcpy.Raster(data_path1+ras)
        raster2=arcpy.Raster(data_path2+ras)
        raster3=arcpy.Raster(data_path3+ras)
        raster4=arcpy.Raster(data_path4+ras)
        raster5=arcpy.Raster(data_path5+ras)
        raster6=arcpy.Raster(data_path6+ras)
        raster7=arcpy.Raster(data_path7+ras)
##        raster8=arcpy.Raster(data_path8+ras)
##        raster9=arcpy.Raster(data_path9+ras)
        raster10=arcpy.Raster(data_path10+ras)
        raster11=arcpy.Raster(data_path11+ras)
        raster12=arcpy.Raster(data_path12+ras)
##        raster13=arcpy.Raster(data_path13+ras)
        raster14=arcpy.Raster(data_path14+ras)
        raster15=arcpy.Raster(data_path15+ras)
        raster16=arcpy.Raster(data_path16+ras)
        raster17=arcpy.Raster(data_path17+ras)
        raster18=arcpy.Raster(data_path18+ras)
        raster19=arcpy.Raster(data_path19+ras)
##        raster20=arcpy.Raster(data_path20+ras)
        raster21=arcpy.Raster(data_path21+ras)
        raster22=arcpy.Raster(data_path22+ras)
        raster23=arcpy.Raster(data_path23+ras)
        raster24=arcpy.Raster(data_path24+ras)
        raster25=arcpy.Raster(data_path25+ras)
        raster26=arcpy.Raster(data_path26+ras)
        outimg=(((raster1+raster2+raster3+raster4+raster5+raster6+raster7+raster10+raster11+raster12+raster14+raster15+raster16+
                  raster17+raster18+raster19+raster21+raster22+raster23+raster24+raster25+raster26)/22))
        outimg.save(save_path+ras)
        print ras

import arcpy, sys, os
from arcpy import env
import numpy as np
from xlwt import Workbook, Formula
import xlrd
from arcpy.sa import *
import tkFileDialog                     
import Tkinter

arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True


data_path = r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp585_2026-2100\Tsday\YearlyMean\Trend\\"
save_path = data_path+"corr_Trend\\"
arcpy.env.workspace = data_path
if not os.path.exists(save_path):
    os.makedirs(save_path)
RasterList = arcpy.ListRasters()
for ras in RasterList:
    if not os.path.exists(save_path+ras):
        ti_img = arcpy.Raster(data_path+ras)
        outputimg = Con((ti_img>0),ti_img)
        outputimg.save(save_path+ras)
        print ras

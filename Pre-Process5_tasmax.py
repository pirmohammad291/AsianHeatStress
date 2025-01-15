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

class subset_LST:
    def Scaling_factor(self):
        data_path1=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CRU4.06\tmn_clip_Asia\Mean\\"
        data_path2=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\historical_1990-2015\tasmin\0_Ensemble_Mean\clip_Asia\Mean\\"
        save_path=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\historical_1990-2015\tasmin\0_Ensemble_Mean\Scaling_factor\\"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.workspace = data_path1
        RasterList=arcpy.ListRasters()
        for ras in RasterList:
            if not os.path.exists(save_path+ras):
                raster1 = arcpy.Raster(data_path1+ras)
                raster2 = arcpy.Raster(data_path2+ras)
                outimg = (raster1) - (raster2)
                outimg.save(save_path+ras)
                print ras

    def daily_correction(self):
        data_path_dailyCMIP=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp370_2026-2100\tasmax\0_Ensemble_Mean\\"
        data_path_monthlyBias=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\historical_1990-2015\tasmax\0_Ensemble_Mean\Scaling_factor\\"
        save_path=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp370_2026-2100\tasmax\0_Ensemble_Mean\BiasCorr\\"
        Apr = data_path_monthlyBias+"04.tif"
        May = data_path_monthlyBias+"05.tif"
        Jun = data_path_monthlyBias+"06.tif"
        Jul = data_path_monthlyBias+"07.tif"
        Aug = data_path_monthlyBias+"08.tif"
        Sep = data_path_monthlyBias+"09.tif"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.workspace = data_path_dailyCMIP
        RasterList=arcpy.ListRasters()
        for ras in RasterList:
            if not os.path.exists(save_path+ras):
                raster1 = arcpy.Raster(data_path_dailyCMIP+ras)     
                date=''.join(ras.split('.')[:1])
                a=str(date)
                m=a[4:6]
                if int(m)==04:
                    outimg = (raster1-273.15) + (Apr)
                    outimg.save(save_path+ras)
                    print ras
                if int(m)==05:
                    outimg = (raster1-273.15) + (May)
                    outimg.save(save_path+ras)
                    print ras
                if int(m)==06:
                    outimg = (raster1-273.15) + (Jun)
                    outimg.save(save_path+ras)
                    print ras
                if int(m)==07:
                    outimg = (raster1-273.15) + (Jul)
                    outimg.save(save_path+ras)
                    print ras
                if int(m)==8:
                    outimg = (raster1-273.15) + (Aug)
                    outimg.save(save_path+ras)
                    print ras
                if int(m)==9:
                    outimg = (raster1-273.15) + (Sep)
                    outimg.save(save_path+ras)
                    print ras

def main():
    output = subset_LST()
##    output.Scaling_factor()
    output.daily_correction()

if __name__=="__main__":
    main()

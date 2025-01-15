import arcpy, sys, os
from arcpy import env
import numpy as np
from xlwt import Workbook, Formula
import xlrd
from arcpy.sa import *
import tkFileDialog                     
import Tkinter
import math as m

arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True

class subset_LST:
    def Tw(self):
        data_path1=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp585_2026-2100\tasmax\0_Ensemble_Mean\BiasCorr\\"
        data_path2=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp585_2026-2100\hursmin\0_Ensemble_Mean\\"
        save_path=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp585_2026-2100\Twday\\"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.workspace = data_path1
        RasterList=arcpy.ListRasters()
        for ras in RasterList:
            if not os.path.exists(save_path+ras):
                T = arcpy.Raster(data_path1+ras)
                RH = arcpy.Raster(data_path2+ras)
                outATan = T*ATan(0.151977*Power((RH+8.313659),0.5)) + ATan(T+RH) - ATan(RH-1.676331) + 0.00391838*Power(RH,1.5)*ATan(0.023101*RH) - 4.686035
                outATan.save(save_path+ras)
                print ras

    def Ts(self):
        data_path1=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp585_2026-2100\Twday\\"
        data_path2=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp585_2026-2100\hursmin\0_Ensemble_Mean\\"
        save_path=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp585_2026-2100\Tsday\\"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.workspace = data_path1
        RasterList=arcpy.ListRasters()
        for ras in RasterList:
            if not os.path.exists(save_path+ras):
                Tw = arcpy.Raster(data_path1+ras)
                RH = arcpy.Raster(data_path2+ras)
                outheatstress = Tw + 4.5*(1-Power((RH/100),2))
                outheatstress.save(save_path+ras)
                print ras
            


def main():
    output = subset_LST()
    output.Tw()
    output.Ts()

if __name__=="__main__":
    main()

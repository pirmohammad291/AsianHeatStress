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
    def hotSpell(self):
        data_path=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp245_2026-2100\Tsday\\"
        data_path_Percn=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp245_2026-2100\Tsday\YearlyMean\Trend\corr_Trend\An_Percn95.tif"
        save_path=data_path+"hotSpell_T27_P95\\"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.workspace = data_path
        RasterList=arcpy.ListRasters()
        for ras in RasterList:
            if not os.path.exists(save_path+ras):
                Ts = arcpy.Raster(data_path+ras)
                outputimg1 = Con((Ts>=27),2, Ts)   # 19 for Lethal AND 27 for Danger
                outputimg2 = Con((Ts>=data_path_Percn),1, Ts)
                outputimg = (outputimg1) - (outputimg2)
                outimg = Con((outputimg==1),outputimg,0)
                outimg.save(save_path+ras)
                print ras

def main():
    output = subset_LST()
    output.hotSpell()

if __name__=="__main__":
    main()

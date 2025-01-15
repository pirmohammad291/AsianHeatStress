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
    global data_path
    data_path = r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\\"
    def LST(self):
        print "Please wait LST file is generating..."
        save_path = data_path+"corr_hursmax\\"
        arcpy.env.workspace = data_path
        if not os.path.exists(save_path):
             os.makedirs(save_path)
        RasterList = arcpy.ListRasters()
        for ras in RasterList:
            if not os.path.exists(save_path+ras):
                ti_img = arcpy.Raster(data_path+ras)
                ti_img_max = arcpy.GetRasterProperties_management(ti_img, "MAXIMUM").getOutput(0)
                ti_img_min = arcpy.GetRasterProperties_management(ti_img, "MINIMUM").getOutput(0)
                print type(ti_img_max)
                if ti_img_max>=90 :
                    corr=int(float(ti_img_max))-90
                    to_img = (ti_img-corr)
                    to_img.save(save_path+ras)
                    print ras

    def Extract(self):
        print "Please wait Extract is generating..."
        data_path1=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\historical_1990-2015\tasmax\0_Ensemble_Mean\Raw\\"
        arcpy.env.workspace=data_path1
        save_path=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\historical_1990-2015\tasmax\0_Ensemble_Mean\clip_Asia\\"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        India_shp=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\Study Area\Lower_Asia\Asia_only.shp"
        RasterList=arcpy.ListRasters()
        for ras in RasterList:
            if not os.path.exists(save_path+ras):
                ti_img = arcpy.Raster(data_path1+ras)
                arcpy.gp.ExtractByMask_sa(ti_img, India_shp, save_path+ras)
                print ras

                
    def fill(self):
        print "Please wait null filling LST file..."
        data_path1 = r"E:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp585_2026-2100\hursmax\0_Ensemble_Mean\\"
        save_path = r"E:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp585_2026-2100\hursmax\0_Ensemble_Mean\Fill\\"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        arcpy.CheckOutExtension("spatial")
        arcpy.env.workspace = data_path1
        rasterList = arcpy.ListRasters()
        rasCount1 = len(rasterList)
        for ras in rasterList:
            if not os.path.exists(save_path+ras):
                Inputimg = arcpy.Raster(data_path1+ras)
                Inputimg_max = arcpy.GetRasterProperties_management(Inputimg, "MAXIMUM").getOutput(0)
                Inputimg_min = arcpy.GetRasterProperties_management(Inputimg, "MINIMUM").getOutput(0)
                corr=int(float(Inputimg_max))-100
                outputimg = Con((Inputimg>=100),100, Inputimg)
                outputimg.save(save_path+ras)
                print ras


    def RasterStats(self):
        print "Please wait Statistics file generating..."
        data_path1=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\historical_1990-2015\hursmin\0_Ensemble_Mean\BiasCorr_clip_Asia\\"
        arcpy.env.workspace=data_path1
        save_path=data_path1+"Fill_statistics\\"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        arcpy.CheckOutExtension("Spatial")
        RasterList = arcpy.ListRasters()
        book = Workbook()
        sheet1 = book.add_sheet("Raw")
        sheet1.write(0,0, "File Name")
        sheet1.write(0,1, 'Min') 
        sheet1.write(0,2, 'Max')
        sheet1.write(0,3, 'Mean')
        sheet1.write(0,4, 'STD')
        ex_row = 1
        for ras in RasterList:
            if not os.path.exists(save_path+ras):
                sheet1.write(ex_row, 0, ras)
                sheet1.write(ex_row, 1, arcpy.GetRasterProperties_management(ras, "MINIMUM", "").getOutput(0))
                sheet1.write(ex_row, 2, arcpy.GetRasterProperties_management(ras, "MAXIMUM", "").getOutput(0))
                sheet1.write(ex_row, 3, arcpy.GetRasterProperties_management(ras, "MEAN", "").getOutput(0))
                sheet1.write(ex_row, 4, arcpy.GetRasterProperties_management(ras, "STD", "").getOutput(0))
                ex_row = ex_row + 1
                print ras
        book.save(save_path+"Stats.xls")
      
            
def main():
    output = subset_LST()
##    output.LST()
##    output.Extract()
    output.fill()()
##    output.Resample()
##    output.RasterStats()

if __name__=="__main__":
    main()


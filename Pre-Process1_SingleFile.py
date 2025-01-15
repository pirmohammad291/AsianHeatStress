import arcpy, sys
import os
import re
from arcpy.sa import*
import numpy as np
import math as m
import pandas as pd

class netCDF:
    def Multiple_netCDF(self):
        path = r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\CMIP6\ssp126_2026-2100\hursmax\EC-Earth3-Veg\\"
        list_dir = os.listdir(path)
        arcpy.env.overwriteOutput =True
        arcpy.CheckOutExtension("Spatial")
        outLoc = path+"Raster\\"
        Asia_shp=r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\Study Area\Lower_Asia\Asia_only.shp"
        if not os.path.isdir(outLoc):
            os.mkdir(outLoc)           
        variable = "hursmax"
        x_dimension = "lon"
        y_dimension = "lat"
        band_dimension = ""
        dimension = "time"
        valueSelectionMethod = "BY_VALUE"
        for inNetCDF in range(len(list_dir)):
            nc_FP = arcpy.NetCDFFileProperties(path + list_dir [inNetCDF] )
            nc_Dim = nc_FP.getDimensions()
            for dimension in nc_Dim:
                top = nc_FP.getDimensionSize(dimension)
                for i in range(0, top):
                    if dimension == "time":
                        dimension_values = nc_FP.getDimensionValue(dimension, i)
                        nowFile = str(dimension_values)
                        x=nowFile
                        ou1=''.join(x.split(' ')[:-2])        # for YYYYMM [-1:0:-1] AND for YYYYMMDD [::-1]
                        ou=''.join(ou1.split('-')[::1])
##                        print ou
##                        print (type(ou))
##                        year=''.join(ou1.split('-')[::4])
##                        print year
##                        pu=int(ou)
                        myInput= ou
##                        print (type(ou))
##                        matched=re.search("[^\d]",myInput) #https://www.pythonforbeginners.com/exceptions/valueerror-invalid-literal-for-int-with-base-10
                        if myInput.isdigit():
                            myInt=int(myInput)
                            print myInt
                            if myInt >= 20260101 :
                                dv1 = ["time", dimension_values]
                                dimension_values = [dv1]
                                if not os.path.exists(outLoc + ou + ".tif"):
                                    arcpy.MakeNetCDFRasterLayer_md(path + list_dir [inNetCDF], variable, x_dimension, y_dimension, nowFile, band_dimension, dimension_values, valueSelectionMethod)
##                                arcpy.CopyRaster_management(nowFile, outLoc + ou + ".tif", "", "", "", "NONE", "NONE", "")
                                    outExtractByMask = ExtractByMask(nowFile, Asia_shp)
##                              arcpy.gp.ExtractByMask_sa(nowFile, Asia_shp, outLoc + ou + ".tif")
                                    arcpy.Resample_management(outExtractByMask, outLoc + ou + ".tif", "0.5", "BILINEAR")
                                    print ou
                            else:
                                print "Raster process not done"
                        else:
                            print "Input Cannot be converted into Integer"
                                
                            
def main():
    output=netCDF()
    output.Multiple_netCDF()

if __name__ == "__main__":
    main()

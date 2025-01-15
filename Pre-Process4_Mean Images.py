import arcpy, sys
import os
from arcpy.sa import *
from xlwt import Workbook, Formula
import xlrd
import numpy as np
from matplotlib import pyplot as plt

arcpy.CheckOutExtension("spatial")
path = r"D:\00_PolyU_LSGI\01_Research\02_Heat Stress\ERA5_monthly\1600Hrs\r\\" #Fill_clip_Asia
list_dir = os.listdir(path)
arcpy.env.overwriteOutput =True

dtime = ['19900401',	'19910401',	'19920401',	'19930401',	'19940401',	'19950401',	'19960401',	'19970401',	'19980401',	'19990401',	'20000401',	'20010401',	'20020401',	'20030401',	'20040401',	'20050401',	'20060401',	'20070401',	'20080401',	'20090401',	'20100401',	'20110401',	'20120401',	'20130401',	'20140401',	'19900501',	'19910501',	'19920501',	'19930501',	'19940501',	'19950501',	'19960501',	'19970501',	'19980501',	'19990501',	'20000501',	'20010501',	'20020501',	'20030501',	'20040501',	'20050501',	'20060501',	'20070501',	'20080501',	'20090501',	'20100501',	'20110501',	'20120501',	'20130501',	'20140501',	'19900601',	'19910601',	'19920601',	'19930601',	'19940601',	'19950601',	'19960601',	'19970601',	'19980601',	'19990601',	'20000601',	'20010601',	'20020601',	'20030601',	'20040601',	'20050601',	'20060601',	'20070601',	'20080601',	'20090601',	'20100601',	'20110601',	'20120601',	'20130601',	'20140601',	'19900701',	'19910701',	'19920701',	'19930701',	'19940701',	'19950701',	'19960701',	'19970701',	'19980701',	'19990701',	'20000701',	'20010701',	'20020701',	'20030701',	'20040701',	'20050701',	'20060701',	'20070701',	'20080701',	'20090701',	'20100701',	'20110701',	'20120701',	'20130701',	'20140701',	'19900801',	'19910801',	'19920801',	'19930801',	'19940801',	'19950801',	'19960801',	'19970801',	'19980801',	'19990801',	'20000801',	'20010801',	'20020801',	'20030801',	'20040801',	'20050801',	'20060801',	'20070801',	'20080801',	'20090801',	'20100801',	'20110801',	'20120801',	'20130801',	'20140801',	'19900901',	'19910901',	'19920901',	'19930901',	'19940901',	'19950901',	'19960901',	'19970901',	'19980901',	'19990901',	'20000901',	'20010901',	'20020901',	'20030901',	'20040901',	'20050901',	'20060901',	'20070901',	'20080901',	'20090901',	'20100901',	'20110901',	'20120901',	'20130901',	'20140901']
sv = ['04', '05','06','07','08','09']

##for i in range(len(list_dir)):
##    print(list_dir[i])
save_path = path+"Mean\\"
if not os.path.exists(save_path):
    os.makedirs(save_path)
j = 0
for per in range(len(sv)):
    rasters = []
    for i in range(25):
        if not os.path.exists(save_path+sv[per]+".tif"):
            rasters.append(path+dtime[j]+".tif")
            print "File", dtime[j]
            j = j + 1
    arcpy.gp.CellStatistics_sa(""+";".join(rasters), save_path+sv[per]+'.tif', "MEAN", "DATA")
    print "Year", sv[per]

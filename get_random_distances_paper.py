# -*- coding: utf-8 -*-
"""
Spyder Editor

This file creates random points in a given geography then takes statistics of distances of the nearest points
Author:
    Alex Din
"""

##
import arcpy
import csv
import numpy  as np
import os
from   random import randint
import time
##
start_time = time.time()
## this needs to be 1000 in order to get 999 iterations because of the range loop starts at 1, not 0
iterations = 1000
## the number of random points to be created each iteration
pointsNum  = 23081
## the prjArea is the project area area geography which is the Baltimore CBSA in this example
prjArea    = r"C:\Path\to\the\feature\class\for\the\project\geography"
## the csvName is the name of your output file, it MUST have '.csv' appended to the string
csvName    = "Baltimore_CBSA.csv"
## workspace is the geodatabase where functions will be performed
workspace  = r"C:\Path\to\the\working\geodatabase.gdb"
## dirspace is where your csv will be written, the directory must already exist prior to running the script
dirspace   = r"C:\Path\to\the\working\directory"
## csvPath is the combination of the csvName and dirspace for outputing the final CSV
csvpath    = os.path.join(dirspace,csvName)
## the name of the random points
ptsName    = "samplepoints"
## the random number is used to export a random set of points for visualization purposes
randomNumb = randint(1, iterations)
## the work environments are set
arcpy.env.overwriteOutput = True
arcpy.env.workspace       = workspace
os.chdir(dirspace)
## the print statement informs the user which
print "Iteration %s will be exported as a random copy for map purposes" %(randomNumb)
##
for number in range(1,iterations):
    print "Processing number %s" %(number)
    small_time = time.time()
    # create a set of random points within the project area
    try:
        arcpy.CreateRandomPoints_management(workspace, ptsName, prjArea, "", pointsNum, "", "POINT", "")
    except Exception as e:
        print e
    # compute nearest neighbor distance
    try:
        nearValueList = []
        arcpy.Near_analysis(ptsName, ptsName, "", "NO_LOCATION", "")
        with arcpy.da.SearchCursor(ptsName,["NEAR_DIST"]) as cursor:
            for row in cursor:
                nearValueList.append(row[0])
        nearValueList.sort()
        # print the values in the IPython console to inspect while processing
        p25  = round(np.percentile(nearValueList, 25), 2)
        print "25th Percentile: %s" %(p25)
        p50  = round(np.percentile(nearValueList, 50), 2)
        print "50th Percentile: %s" %(p50)
        p75  = round(np.percentile(nearValueList, 75), 2)
        print "75th Percentile: %s" %(p75)
        mean = round(np.mean(nearValueList), 2)
        print "Mean: %s" %(mean)
        std  = round(np.std(nearValueList),  2)
        print "STD: %s" %(std)
        var  = round(np.var(nearValueList,ddof=1),  2)
        print "Variance: %s" %(var)
        maxx  = round(np.max(nearValueList),  2)
        print "Maximum: %s" %(maxx)
        minn  = round(np.min(nearValueList),  2)
        print "Minimum: %s" %(minn)
        del cursor, row
    except Exception as e:
        print e
    # get the time it took to run just this one iteration
    small_time_end = time.time()
    small_elapse   = round((small_time_end - small_time),2)
    print "This iteration took %s seconds" %(small_elapse)
    # log the information to a CSV file
    # if the CSV does not yet exist, the CSV will be created with headers and append the first iteration of data
    # else, if the CSV does exist, the information will be appended to a new row
    try:
        headRows = ["Number", "Seconds","25P", "Median", "75P", "Mean","STD", "Variance", "Maximum","Minimum"]
        dataRows = [number,small_elapse,p25,p50,p75,mean,std,var,maxx,minn]
        if not os.path.exists(csvpath):
            with open(csvName, 'wb') as f:
                wtr = csv.writer(f, delimiter= ',')
                wtr.writerow(headRows)
                wtr.writerow(dataRows)
        else:
            with open(csvName, 'ab') as f:
                wtr = csv.writer(f, delimiter= ',')
                wtr.writerow(dataRows)
    except Exception as e:
        print e
    del f, wtr
    # if the iteration matches the random number, export the sample dataset for visualization purposes
    try:
        if number == randomNumb:
            out_name = "%s_random_%s" %(ptsName,number)
            arcpy.FeatureClassToFeatureClass_conversion(ptsName,workspace,out_name)
    except Exception as e:
        print e
    print("--------------------------------------------------------------------")
##
end_time = time.time()
print("Total time elapsed was %g seconds" % round((end_time - start_time),2))
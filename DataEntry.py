
# coding: utf-8

# In[1]:

import sqlite3
import fiona
import json
from json import *
import gdal
from osgeo import ogr
import os
import collections


# In[2]:

#Retrieve variables
projectname = raw_input("Enter project name: ")
pathrow1 = raw_input("Enter Path Row PPPRRR: ")
username = raw_input("Enter the user who processed the scene: ")
completed = raw_input("Have you finished running the model on this scene? y/n ")
if completed == 'n':
    ccdcversion = ''
    model = 'None'
    processing = raw_input("Have you started processing the images yet? y/n ")
    if processing == 'n':
        status = 'Not Yet Started'
        locationname = ''
    else:
        status = 'In Processing'
        locationname = raw_input("Enter the location of the image directory: ")    
else:
    status = 'Completed'
    modeltype = raw_input("YATSM or CCDC? ")
    model = modeltype.upper()
    if model == "YATSM":
        locationname = raw_input("Enter location on server of parameter file: ")
    elif model == "CCDC":
        minRMSE = raw_input("Enter the minimum RMSE (If unknown just press [ENTER]): ")
        changeprob = raw_input("Enter the probability of change value (If unknown just press [ENTER]): ")
        noiseprob = raw_input("Enter the noise probability value (If unknown just press [ENTER]): ")
        consecChange = raw_input("Enter the number of consecutive observations for a confirmed change (If unknown just press [ENTER]: ")
        coefs = raw_input("Enter the number of coefficients used (If unknown just press [ENTER]): ")
        locationname = raw_input("Enter the location of the image stack on the server: ")            
        ccdcversion = raw_input("Enter the version of CCDC used (If unknown just press [ENTER]): ")
    else:
        print "Please try the script again"
        exit()
    
if model == "YATSM":
    print '\n\nYour scene characteristics are:\nModel Run: %s\nPathRow: %s\nParameter Location: %s\nProcesing User: %s' % (modeltype, pathrow1, locationname, username)
    answer = raw_input("Is this correct? y/n ")
elif model == "CCDC":
    print '\n\nYour scene characteristics are:\nModel Run: %s\nPathRow: %s\nMinimum RMSE: %s\nChange Probability: %s\nNoise Probability: %s\nConsecutive Observations: %s\nCoefficients: %s\nStack Location: %s\nUsername: %s\nVersion: %s\n' %(modeltype, pathrow1, minRMSE, changeprob, noiseprob, consecChange, coefs, locationname, username, ccdcversion)
    answer = raw_input("Is this correct? y/n ")
else:
    print '\n\nYour scene characteristics are:\nProcessing: %s\nPathRow: %s\nUsername: %s\n' %(status, pathrow1, username)
    answer = raw_input("Is this correct? y/n ")

    
if answer == 'n':
    exit()


# In[3]:

#Start process of updating database
print 'Updating database...'
conn = sqlite3.connect('SceneDatabase.db')
c = conn.cursor()


# In[4]:

#Define the functions for entering data
def yatsmDataEntry():
    c.execute("INSERT INTO yatsm(Project, PathRow, User, Location) VALUES(?,?,?,?)",
              (projectname, pathrow1, username, locationname))
    conn.commit()
    
def ccdcDataEntry():
    c.execute("INSERT INTO ccdc(Project, PathRow, User, MinRMSE, ChangeProb, NoiseProb, ConsecChange, Coef, LocationCCDC) VALUES(?,?,?,?,?,?,?,?,?)",
              (projectname, pathrow1, username, minRMSE, changeprob, noiseprob, consecChange, coefs, locationname))
    conn.commit()
    
def bothDataEntry():
    c.execute("INSERT INTO both(Project, PathRow, User, Location, Status) VALUES(?,?,?,?,?)",
              (projectname, pathrow1, username, locationname, status))
    conn.commit()


# In[5]:

#Update tables
if model == "YATSM":
    yatsmDataEntry()
if model == "CCDC":
    ccdcDataEntry()
    
bothDataEntry()


# In[6]:

#Exporting 'both' table to .csv using Pandas
print "Updating .CSV files..."
import pandas.io.sql as panda
con = sqlite3.connect('SceneDatabase.db')
table = panda.read_sql('select * from both', con)
table.to_csv('SceneList.csv')
table2 = panda.read_sql('select * from yatsm', con)
table2.to_csv('YATSM_Scenes.csv')
table3 = panda.read_sql('select * from ccdc', con)
table3.to_csv('CCDC_Scenes.csv')


# In[7]:

#Make the template for all but the last input of GeoJSON
template =     ''' { "type" : "Feature",
        "properties" : { "fillColor" : "%s", "strokeColor" : "%s", "fillOpacity" : "%s", "WRS2" : "%s", "Project" : "%s", "Author" : "%s", "Location" : "%s"}, "geometry" : %s},
    '''


# In[8]:

#Make the template for the last input of GeoJSON
template2 =     ''' { "type" : "Feature",
        "properties" : { "fillColor" : "%s", "strokeColor" : "%s", "fillOpacity" : "%s", "WRS2" : "%s", "Project" : "%s", "Author" : "%s", "Location" : "%s"}, "geometry" : %s}
    '''


# In[9]:

#Setup the beginning of the GeoJSON file
output =     ''' {"type": "FeatureCollection",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features": [
    ''' \


# In[10]:


# In[12]:

#Loop over each row in the CSV and plug into templates
#Note: There has to be a better way to do this...
import csv
iter = 0
print "Updating GeoJSON file..."
f = open('SceneList.csv')
rawData = csv.reader(f.readlines())
t = len(open('SceneList.csv').readlines())
#print t
for row in rawData:
    if row[6] == 'In Processing':
        fillop = '0.3'
    elif row[6] == 'Not Yet Started':
        fillop = '0.0'
    else:
        fillop = '0.9'
    iter += 1
    if row[2].upper() == 'CMS_MEXICO' or row[2].upper() =='CMS MEXICO':
        fillcolor = '#33a02c'
    elif row[2].upper() == 'ACRE':
        fillcolor = '#1f78b4'
    elif row[2].upper() == 'AMAZON':
        fillcolor = '#a6cee3'
    elif row[2].upper() == 'GUANGZHOU':
        fillcolor = '#b2df8a'
    elif row[2].upper() == 'BOSTON':
        fillcolor = '#80b1d3'
    elif row[2].upper() == 'CMS':
        fillcolor = '#fb9a99'
    elif row[2].upper() == 'IDS':
        fillcolor = '#e31a1c'
    elif row[2].upper() == 'LCMS':
        fillcolor = '#ff7f00'
    elif row[2].upper() == 'VIETNAM':
        fillcolor = '#ffff99'
    elif row[2].upper() == 'CAMBODIA DEFORESTATION':
        fillcolor = '#6a3d9a'
    elif row[2].upper() == 'FUSION':
        fillcolor = '#b15928'
    else:
        fillcolor = '#737373'
    if iter >= 2 and iter != t:
        source = fiona.open('/usr3/graduate/bullocke/bin/Database/HelperFiles/wrs2_descending.shp')
        for rec in source:
            if rec['properties']['WRSPR'] == int(row[3]):
                break
        PR = rec['geometry']
        PR2 = str(PR).replace('(','[').replace(')',']').replace('\'','\"')
        output += template % (fillcolor, fillcolor, fillop, row[3], row[2], row[4], row[5], PR2)
    if iter == t:
        source = fiona.open('/usr3/graduate/bullocke/bin/testing/database2/Database/HelperFiles/wrs2_descending.shp')
        for rec in source:
            if rec['properties']['WRSPR'] == int(row[3]):
                break
        PR = rec['geometry']
        PR2 = str(PR).replace('(','[').replace(')',']').replace('\'','\"')
        output += template2 % (fillcolor, fillcolor, fillop, row[3], row[2], row[4], row[5], PR2)


# In[13]:

#Add the tail to the output file
output +=     '''     ]
}
    '''


# In[147]:

#Open the GeoJSON and update

outFileHandle = open("PRmap.geojson", "w")
outFileHandle.write(output)
outFileHandle.close()


print "Done! Thank you!"
# In[ ]:




# In[ ]:




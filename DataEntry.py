
# coding: utf-8

# In[1]:

import sqlite3
from collections import OrderedDict
import fiona
import json
from json import *
import gdal
from osgeo import ogr
import os


# In[35]:

#Retrieve variables
modeltype = raw_input("YATSM or CCDC? ")
projectname = raw_input("Enter project name: ")
pathrow1 = raw_input("Enter Path Row PPPRRR: ")
username = raw_input("Enter the user who processed the scene: ")
if modeltype == "YATSM" or modeltype == "yatsm":
    locationname = raw_input("Enter location on server of parameter file: ")
elif modeltype == "CCDC" or modeltype == "ccdc":
    minRMSE = raw_input("Enter the minimum RMSE (If unknown just press [ENTER]): ")
    changeprob = raw_input("Enter the probability of change value (If unknown just press [ENTER]): ")
    noiseprob = raw_input("Enter the noise probability value (If unknown just press [ENTER]): ")
    consecChange = raw_input("Enter the number of consecutive observations for a model fit (If unknown just press [ENTER]): ")
    coefs = raw_input("Enter the number of coefficients used (If unknown just press [ENTER]): ")
    locationname = raw_input("Enter the location of the image stack on the server: ")            
else:
    print "Please try the script again"
    exit()
    
if modeltype == "YATSM" or modeltype == "yatsm":
    print 'Your scene characteristics are:\nModel Run: %s\nPathRow: %s\nParameter Location: %s\nProcesing User: %s' % (modeltype, pathrow1, locationname, username)
else:
    print '\n\nYour scene characteristics are:\nModel Run: %s\nPathRow: %s\nMinimum RMSE: %s\nChange Probability: %s\nNoise Probability: %s\nCoefficients: %s\nStack Location: %s\n' %(modeltype, pathrow1, minRMSE, changeprob, noiseprob, coefs, locationname)

answer = raw_input("Is this correct? y/n ")
    
if answer == 'n':
    exit()


# In[37]:

#Determine the styling
strokecolor = '#000000'
opaquenumb = 1
if modeltype == 'yatsm' or modeltype == 'YATSM':
    fillcolor = '#C00000'
else:
    fillcolor = '#0000CC'
    


# In[38]:

#Prepare the variables for the YATSM shapefile
pathrow2 = pathrow1.lstrip("0")
_model = modeltype
_pr = int(pathrow2)
_project = projectname
_author = username
_location = locationname
_fill = fillcolor
_stroke = strokecolor
_opaque = opaquenumb

_properties = OrderedDict([
    ['fill', 'str'],
    ['stroke', 'str'],
    ['fill-opacity', 'int'],
    ['Model', 'str'],
    ['WRS2', 'int'],
    ['Project', 'str'],
    ['Author', 'str'],
    ['Location', 'str']
])


# In[47]:

#Prepare the schema
_schema = {'geometry': 'Polygon',
           'properties': _properties,
           }


# In[40]:

#Match PathRow with WRS2 shapefile
source = fiona.open('/usr3/graduate/bullocke/bin/Database/HelperFiles/wrs2_descending.shp')
for rec in source:
    if rec['properties']['WRSPR'] == _pr:
        break


# In[53]:

#Update the database shapefile for YATSM
with fiona.open('/usr3/graduate/bullocke/bin/Database/HelperFiles/PRmap.shp') as f:
    elem = next(f)
    elem['geometry'] = rec['geometry']
    elem['properties'] = {
        'fill': _fill,
        'stroke': _stroke,
        'Model': _model,
        'WRS2': _pr,
        'Project': _project,
        'Author': _author,
        'Location': _location,
}
with fiona.open('/usr3/graduate/bullocke/bin/Database/HelperFiles/PRmap.shp', 'a') as f:
    f.write(elem)


# In[54]:

#Convert shapefile to .GeoJSON to be used on GitHub using Leaflet.js
print "Updating GeoJSON file"
os.remove("PRmap.geojson")
os.system("ogr2ogr -f GeoJSON -t_srs crs:84 PRmap.geojson /usr3/graduate/bullocke/bin/Database/HelperFiles/PRmap.shp")
os.system("chmod g+rwx PRmap.geojson")

# In[13]:

#Start process of updating database
print 'Updating database'
conn = sqlite3.connect('SceneDatabase.db')
c = conn.cursor()


# In[14]:

#Define data entry functions
def yatsmDataEntry():
    c.execute("INSERT INTO yatsm(Project, PathRow, User, Location) VALUES(?,?,?,?)",
              (projectname, pathrow1, username, locationname))
    conn.commit()
    
def ccdcDataEntry():
    c.execute("INSERT INTO ccdc(Project, PathRow, User, MinRMSE, ChangeProb, NoiseProb, ConsecChange, Coef, LocationCCDC) VALUES(?,?,?,?,?,?,?,?,?)",
              (projectname, pathrow1, username, minRMSE, changeprob, noiseprob, consecChange, coefs, locationname))
    conn.commit()


# In[22]:

if modeltype == "YATSM" or modeltype == "yatsm":
    yatsmDataEntry()
if modeltype == "CCDC" or modeltype == "ccdc":
    ccdcDataEntry()


# In[47]:

##Show table in python if desired
#c.execute("Select * from yatsm")
#table=c.fetchall()
#for x in table:
#    print x


# In[24]:

#Update CSV File for yatsm
import csv
print 'Updating CSV'
if modeltype == "YATSM" or modeltype == "yatsm":
    c.execute('select * from yatsm')
    with open('YATSM_Scenes.csv', 'wb') as fout:
        writer = csv.writer(fout)
        writer.writerow(['ID','Project','Path Row', 'User', 'Parameter File Location']) # heading row
        writer.writerows(c.fetchall())
if modeltype == "CCDC" or modeltype == "ccdc":
    c.execute('select * from ccdc')
    with open('CCDC_Scenes.csv', 'wb') as fout:
        writer = csv.writer(fout)
        writer.writerow(['ID','Project','Path Row', 'User', 'MinRMSE', 'Change Probability', 'Noise Probability','Consecutive Observations for Change', '# Coefficients', 'Stack Location']) # heading row
        writer.writerows(c.fetchall())


# In[ ]:




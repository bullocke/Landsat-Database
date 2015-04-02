
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

#Exporting 'both' table to .csv using Pandas
print "Updating .CSV files..."
import pandas.io.sql as panda
con = sqlite3.connect('/usr3/graduate/bullocke/bin/Database/SceneDatabase.db')
table = panda.read_sql('select * from both', con)
table.to_csv('/usr3/graduate/bullocke/bin/Database/SceneList.csv')
table2 = panda.read_sql('select * from yatsm', con)
table2.to_csv('/usr3/graduate/bullocke/bin/Database/YATSM_Scenes.csv')
table3 = panda.read_sql('select * from ccdc', con)
table3.to_csv('/usr3/graduate/bullocke/bin/Database/CCDC_Scenes.csv')

# In[7]:

#Make the template for all but the last input of GeoJSON
template =     ''' { "type" : "Feature",
        "properties" : { "fill" : "%s", "stroke" : "%s", "fill-opacity" : "%s", "WRS2" : "%s", "Project" : "%s", "Author" : "%s", "Location" : "%s"}, "geometry" : %s},
    '''


# In[8]:

#Make the template for the last input of GeoJSON put %s in for fill,stroke, and fill-op
template2 =     ''' { "type" : "Feature",
        "properties" : { "fill" : "%s", "stroke" : "%s", "fill-opacity" : "%s", "WRS2" : "%s", "Project" : "%s", "Author" : "%s", "Location" : "%s"}, "geometry" : %s}
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
f = open('/usr3/graduate/bullocke/bin/Database/SceneList.csv')
rawData = csv.reader(f.readlines())
t = len(open('/usr3/graduate/bullocke/bin/Database/SceneList.csv').readlines())
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

#    fillcolor='#33a02c'
#    fillop='0.9'
    if iter >= 2 and iter != t:
        source = fiona.open('/usr3/graduate/bullocke/bin/Database/HelperFiles/wrs2_descending.shp')
        for rec in source:
            if rec['properties']['WRSPR'] == int(row[3]):
                break
        PR = rec['geometry']
        PR2 = str(PR).replace('(','[').replace(')',']').replace('\'','\"')
        output += template % (fillcolor, fillcolor, fillop, row[3], row[2], row[4], row[5], PR2)
    if iter == t:
        source = fiona.open('/usr3/graduate/bullocke/bin/Database/HelperFiles/wrs2_descending.shp')
        for rec in source:
            if rec['properties']['WRSPR'] == int(row[3]):
                break
        PR = rec['geometry']
        PR2 = str(PR).replace('(','[').replace(')',']').replace('\'','\"')
        output += template2 % (fillcolor, fillcolor, fillop, row[3], row[2], row[4], row[5], PR2)

output +=     '''     ]
}
    '''

# In[147]:

#Open the GeoJSON and update

outFileHandle = open("/usr3/graduate/bullocke/bin/Database/PRmap.geojson", "w")
outFileHandle.write(output)
outFileHandle.close()


print "Done! Thank you!"


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
    else:
        print "Please try the script again"
        exit()
    
if model == "YATSM":
    print '\n\nYour scene characteristics are:\nModel Run: %s\nPathRow: %s\nParameter Location: %s\nProcesing User: %s' % (modeltype, pathrow1, locationname, username)
    answer = raw_input("Is this correct? y/n ")
elif model == "CCDC":
    print '\n\nYour scene characteristics are:\nModel Run: %s\nPathRow: %s\nMinimum RMSE: %s\nChange Probability: %s\nNoise Probability: %s\nConsecutive Observations: %s\nCoefficients: %s\nStack Location: %s\nUsername: %s\n' %(modeltype, pathrow1, minRMSE, changeprob, noiseprob, consecChange, coefs, locationname, username)
    answer = raw_input("Is this correct? y/n ")
else:
    print '\n\nYour scene characteristics are:\nProcessing: %s\nPathRow: %s\nUsername: %s\n' %(status, pathrow1, username)
    answer = raw_input("Is this correct? y/n ")

    
if answer == 'n':
    exit()


# In[3]:

#Start process of updating database
print 'Updating database...'
conn = sqlite3.connect('/usr3/graduate/bullocke/bin/Database/SceneDatabase.db')
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

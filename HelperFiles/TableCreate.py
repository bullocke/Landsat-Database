
# coding: utf-8

# In[1]:

import sqlite3


# In[5]:

conn = sqlite3.connect('SceneDatabase2.db')
c = conn.cursor()


# In[6]:

#Create table for YATSM
def YATSMtableCreate():
    c.execute("CREATE TABLE yatsm(id integer primary key autoincrement, Project TEXT, PathRow INT, User TEXT, Location TEXT)")


# In[8]:

def CCDCtableCreate():
    c.execute("CREATE TABLE ccdc(id integer primary key autoincrement, Project TEXT, PathRow INT, User TEXT, MinRMSE INT, ChangeProb REAL, NoiseProb REAL, ConsecChange INT, Coef INT, LocationCCDC TEXT)")

def BothtableCreate():
    c.execute("CREATE TABLE both(id integer primary key autoincrement, Project TEXT, PathRow INT, User TEXT, Model, Location)")

# In[9]:

YATSMtableCreate()


# In[10]:

CCDCtableCreate()


# In[11]:

BothtableCreate()




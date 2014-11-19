## About

This is a database manager to help organize Curtis Woodcock's remote sensing group at Boston University. The group has recently been analyzing time series models developed using entire Landsat image stacks to look at landcover change. The model used for analysis is termed CCDC (Continuous Change Detection and Classification) and was developed by Zhe Zhu and Curtis Woodcock (Zhu and Woodcock 2014). Recently, it has been used as a strong influence in the development of another model, YATSM (Yet Another Time Series Model), by Chris Holden. The original CCDC is written in MATLAB, while YATSM is being developed in Python.

This page is meant to help organize the research at BU that utilizes the two time series models. Information on the scenes run can be found in the two data tables, CCDC_Scenes.csv and YATSM_Scenes.csv, as well as basic information on all scenes in All_Scenes.csv. In addition, the information is visualized on a map, PRmap.geojson. The map is color coded based on whether it was run by CCDC, YATSM, or both.


##How to Use

If you run a model at BU, it would be nice if you could contribute to the database. To do this first go to the data directory at:
   
    /usr3/graduate/bullocke/bin/Database


Next, make sure you have all the modules and libraries loaded by typing:

    module load batch_landsat/v4

Finally, execute the interactive database console by typing:

    python DataEntry.py

The console will ask you some questions about the scene you run. Please fill out everything that you can. It is helpful to know the parameters used if we want to use the scene for something else in the future.

That is all! The script will update the .CSV data table and .GeoJSON map file. The data is updating automatically, but will only appear on this repository once I push the update.  

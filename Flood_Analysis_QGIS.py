from qgis import processing
from qgis.utils import iface

from PyQt5.QtCore import QVariant

#Please insert your folder path to start
inputpath = "/Users/mac/Desktop/test_data/"

#Merging rasters
Merged = processing.run("gdal:merge",
    {
        'INPUT': [inputpath + 'dsm_1m_utm17_e_20_90.tif',
                inputpath + 'dsm_1m_utm17_e_20_91.tif',
                inputpath + 'dsm_1m_utm17_e_21_90.tif',
                inputpath + 'dsm_1m_utm17_e_21_91.tif'],
        'PCT':False,
        'SEPARATE':False,
        'NODATA_INPUT':None,
        'NODATA_OUTPUT':None,
        'OPTIONS':'',
        'EXTRA':'',
        'DATA_TYPE':5,
        'OUTPUT':inputpath + 'Merged.tif'})


#Removing sinks
sinkfill = processing.run("saga:fillsinkswangliu", 
    {
        'ELEV':inputpath + 'Merged.tif',
        'MINSLOPE':0.01,
        'FILLED':inputpath + 'FilledDEM.sdat',
        'FDIR':inputpath + 'FlowDirections.sdat',
        'WSHED':inputpath + 'Watershed.sdat'
    }
)


#Using raster calculator to identify flooded area when water level is above two meters


lyr1 = QgsRasterLayer(inputpath + 'FilledDEM.sdat')
output = inputpath + 'waterline_2.tif'
entries = []

ras = QgsRasterCalculatorEntry()
ras.ref = "FilledDEM@1"
ras.raster = lyr1
ras.bandNumber = 1
entries.append(ras)

calc = QgsRasterCalculator(' (  ( "FilledDEM@1" <= 190 )  = 1 )  AND  (  ( "FilledDEM@1" >= 190 )  = 0 ) ',output, 'GTiff', \
lyr1.extent(), lyr1.width(), lyr1.height(), entries)

calc.processCalculation()
iface.addRasterLayer(output)


#Adding vector layers

vectorlayer_hydrography = QgsVectorLayer(inputpath + 'Hydrography_Area.shp', "Hydrography_Area", "ogr")
vectorlayer_road = QgsVectorLayer(inputpath + 'Road.shp', "Road", "ogr")
vectorlayer_building = QgsVectorLayer(inputpath + 'Building.shp', "Building", "ogr")
vectorlayer_pedestrian = QgsVectorLayer(inputpath + 'Pedestrian_Network_Area.shp', "Pedestrian_Network_Area", "ogr")


#Loading vector layers

QgsProject.instance().addMapLayer(vectorlayer_hydrography)
QgsProject.instance().addMapLayer(vectorlayer_road)
QgsProject.instance().addMapLayer(vectorlayer_building)
QgsProject.instance().addMapLayer(vectorlayer_pedestrian)
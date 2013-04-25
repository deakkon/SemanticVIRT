#py imports
import sys
import pygal
import gc
from pygal.style import *

#import user defined functions
from sys import path
path.append("/home/jseva/SemanticVIRT/python/utils/")
from databaseODP import * 
from utils import *

def returnAnalysisReuslts(grouping,model,limit,range):
    sqlAnalysisReport = "select * from analysis_precision where groupingType = '%s' and model='%s' and limitValue = '%s' and typeValue = '%s'" %(grouping,model,limit,range)
    analysisReport = dbQuery(sqlAnalysisReport)
    return analysisReport

def prepareData(sqlResults):
    data = []
    labels = getUniqueItems(sqlResults,6)
    categories = getUniqueItems(sqlResults,1)
    for cat in categories:
        catData = []
        catData.append(cat)
        tempdata = [float(x[5]) for x in sqlResults if x[1] == cat]
        catData.extend(tempdata)
        data.append(catData)
    return (data,labels)

def RadarGraph(grouping, model, limit, range):
    """
    title: string
    labels: list
    data: list of lists
    """

    data, labels  = prepareData(returnAnalysisReuslts(grouping,model,limit,range))
    radar_chart = pygal.Radar(x_scale=.1, y_scale=.1, style=LightSolarizedStyle,legend_at_bottom=True)
    title = "%s %s %s %s" %(grouping, model, limit, range)
    radar_chart.title = title
    radar_chart.x_labels = labels
    
    for row in data:
        #print row[0], row[1:]
        radar_chart.add(row[0],row[1:])
    
    fn = "graphs/radar/%s_%s_%s_%s.svg" %(grouping, model, limit, range)
    radar_chart.render_to_file(fn)
    print grouping, model, limit, range, fn

def drawRadarGraph():
    GROUPTYPE = ["CATID","FATHERID","GENERAL"]
    models = [0.1, 0.25, 0.5, 0.75, 1.0]
    limits = [10,100,1000]
    ranges = [1,2]
    
    for range in ranges:
        for groupingType in GROUPTYPE:
            for model in models:
                for limit in limits:
                    RadarGraph(groupingType, model, limit, range)

drawRadarGraph()
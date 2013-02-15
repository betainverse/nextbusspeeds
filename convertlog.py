#!/usr/bin/python

import time,urllib2
import xml.etree.ElementTree as ET
from datetime import datetime
from sys import argv

def getTimeStamp():
    #2013-02-13 13:58:38.431522
    timestamp = '%s'%datetime.today()
    return timestamp.split('.')[0]

def getDistance(lat1,lon1,lat2,lon2):
    deltalat = abs(lat1-lat2)
    deltalon = abs(lon1-lon2)
    deltalatmi = deltalat*69
    deltalonmi = deltalon*49
    return sqrt(deltalatmi**2+deltalonmi**2)

def getStopInfo(xml):
    root = ET.fromstring(xml) #root is body
    route = root.find('route')
    stops = route.findall('stop')
    stopDict = {}
    for stop in stops:
        stopDict[stop.get('tag')]=(stop.get('title'),stop.get('lat'),stop.get('lon'))
    return stopDict

def getDirectionInfo(xml):
    root = ET.fromstring(xml) #root is body
    route = root.find('route')
    directions = route.findall('direction')
    for d in directions:
        stops = d.findall('stop')
        stopTags = [stop.get('tag') for stop in stops]
        dirDict[d.get('tag')]=(d.get('title'),d.get('name'),stopTags)
    return dirDict
    
def getDirectionName(xml,dirTag):
    return getDirectionInfo(xml)[dirTag][1]

def getDirectionTitle(xml,dirTag):
    return getDirectionTitle(xml)[dirTag][0]
    
def getDirectionStopData(xml,dirTag):
    stopDict = getStopInfo(xml)
    stopTags = getDirectionInfo(xml)[dirTag][2]
    CoordList = [(stopDict[stoptag][1],stopDict[stoptag][2]) for stoptag in stopTags]
    return CoordList

#somehow calculate distance from one stop to the next, store in a dictionary indexed
#by coordinates.

#have tag-indexed dictionary that gives distance from start
#have coord indexed dictionary (for a direction?) that gives tag

def makeOneWayStopPath(xml):
    stopDict = getStopInfo(xml)
    root = ET.fromstring(xml) #root is body
    route = root.find('route')
    direction = route.find('direction') #only take first one
    stops = direction.findall('stop')
    path = []
    for stop in stops:
        stopdata = stopDict[stop.get('tag')]
        path.append((stopdata[1],stopdata[2]))
    for stop in path:
        print stop[1],stop[0]
    return path

def makeReturnStopPath(xml):
    stopDict = getStopInfo(xml)
    root = ET.fromstring(xml) #root is body
    route = root.find('route')
    direction = route.findall('direction')[1] #only take second one
    stops = direction.findall('stop')
    path = []
    for stop in stops:
        stopdata = stopDict[stop.get('tag')]
        path.append((stopdata[1],stopdata[2]))
    for stop in path:
        print stop[1],stop[0]
    return path

def getBusProgress(direction,lat,lon):
    xml = getRouteXML(routenum)
    

def makePath():
    return pointslist

def getRouteXML(routenum):
    url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=mbta&r=%d'%routenum
    try:
        response = urllib2.urlopen(url)
        xml = response.read()
        return xml
    except Exception,e:
        print e

# def getRoute(routenum):
#     url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=mbta&r=%d'%routenum
#     try:
#         response = urllib2.urlopen(url)
#         xml = response.read()
#     except Exception,e:
#         print e
#     root = ET.fromstring(xml) #root is body
#     route = root.find('route')
#     paths = route.findall('path')
#     coordlist = []
#     for path in paths:
#         points=path.findall('point')
#         for point in points:
#             lat = point.get('lat')
#             lon = point.get('lon')
#             coordlist.append((lon,lat))
#             print lon,lat
#         print ""
#     return route #ordered list of pairs

def getTimeDiff(t1,t2):
    #convert from msec
    t1i=int(t1) #should not need to cast as int
    t2i=int(t2)
    msec = t2i-t1i
    sec = msec/1000.0
    minutes = sec/60.0
    return minutes

def getDestination(dirTag):
    if dirTag == None:
        return 'None'
    if dirTag == '1_0_var0':
        return 'Harvard'
    elif dirTag == '1_1_var0':
        return 'Dudley'
    elif dirTag == '701_0_var0':
        return 'Central'
    elif dirTag == '701_1_var0':
        return 'BMC'
    else:
        return 'Other'

def getRoutename(routenum):
    if routenum=='1':
        return '1'
    elif routenum=='701':
        return 'CT1'
    else:
        return 'other'

def readLog(filename):
    busDict = {}
    logfile = open(filename,'r')
    for line in logfile.readlines():
        busID,destination,lat,lon,date,time = line.split()
        if busID not in busDict.keys():
            busDict[busID]={}
        busDict[busID]['\t'.join([date,time])]='\t'.join([destination,lat,lon])
    logfile.close()
    return busDict

def writeTable(filename,busDict):
    buscolumns = busDict.keys()
    buscolumns.sort()
    timestamps = []
    for bus in buscolumns:
        times = busDict[bus].keys()
        for t in times:
            if t not in timestamps:
                timestamps.append(t)
    #times = sorted(timestamps, key=lambda a:map(int,a.split(':')))
    timestamps.sort()
    tablefile = open(filename,'w')
    tablefile.write("Date\tTime\t")
    for bus in buscolumns:
        tablefile.write("%s\t%s\t%s\t"%(bus,bus,bus))
    tablefile.write("\nDate\tTime\t")
    for bus in buscolumns:
        tablefile.write("Destination\tLatitude\tLongitude\t")
    tablefile.write("\n")
    for stamp in timestamps:
        tablefile.write(stamp)
        tablefile.write('\t')
        for bus in buscolumns:
            if stamp in busDict[bus].keys():
                tablefile.write("%s\t"%(busDict[bus][stamp]))
            else:
                tablefile.write("\t\t\t")
        tablefile.write("\n")
    tablefile.close()

def writeLatitudesLongitudes(latfilename,longfilename,busDict):
    buscolumns = busDict.keys()
    buscolumns.sort()
    timestamps = []
    for bus in buscolumns:
        times = busDict[bus].keys()
        for t in times:
            if t not in timestamps:
                timestamps.append(t)
    #times = sorted(timestamps, key=lambda a:map(int,a.split(':')))
    timestamps.sort()
    latfile = open(latfilename,'w')
    longfile = open(longfilename,'w')
    latfile.write("Date\tTime\t")
    longfile.write("Date\tTime\t")
    for bus in buscolumns:
        latfile.write("%s\t"%bus)
        longfile.write("%s\t"%bus)
    latfile.write("\n")
    longfile.write("\n")
    for stamp in timestamps:
        latfile.write(stamp)
        latfile.write('\t')
        longfile.write(stamp)
        longfile.write('\t')
        for bus in buscolumns:
            if stamp in busDict[bus].keys():
                latfile.write("%s\t"%busDict[bus][stamp].split('\t')[1])
                longfile.write("%s\t"%busDict[bus][stamp].split('\t')[2])
            else:
                latfile.write("\t")
                longfile.write("\t")
        latfile.write("\n")
        longfile.write("\n")
    latfile.close()
    longfile.close()
    

def main():
    print getTimeStamp()
    #busDict = readLog('test.log')
    #writeTable('test.txt',busDict)
    ##writeLatitudesLongitudes('lat.log','long.log',busDict)
    xml = getRouteXML(1)
    makeOneWayStopPath(xml)
    print ''
    makeReturnStopPath(xml)
main()

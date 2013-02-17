#!/usr/bin/python

import time,urllib2
import xml.etree.ElementTree as ET
from datetime import datetime
from sys import argv
from math import sin,cos,atan2,sqrt,pi

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

def deg2rad(deg):
    rad = deg * pi/180
    return rad

def getStopDist(stop1,stop2): #check need for math
    #based on js http://andrew.hedges.name/experiments/haversine/
    lat2 = deg2rad(float(stop2.get('lat')))
    lat1 = deg2rad(float(stop1.get('lat')))
    lon1 = deg2rad(float(stop1.get('lon')))
    lon2 = deg2rad(float(stop2.get('lon')))
    dlat = lat2-lat1
    dlon = lon2-lon1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2( sqrt(a), sqrt(1-a) )
    R = 3961
    d = R * c #(where R is the radius of the Earth) (3961 miles & 6373 km)
    #return getDistance(lat1,lon1,lat2,lon2)
    return d

def getStopInfo(xml):
    root = ET.fromstring(xml) #root is body
    route = root.find('route')
    stops = route.findall('stop')
    stopDict = {}
    for stop in stops:
        stopDict[stop.get('tag')]=(stop.get('title'),stop.get('lat'),stop.get('lon'))
    return stopDict

def getStops(xml):
    root = ET.fromstring(xml) #root is body
    route = root.find('route')
    stops = route.findall('stop')
    return stops

def getStop(xml,stoptag):
    allstops = getStops(xml)
    for stop in allstops:
        if stop.get('tag')==stoptag:
            return stop

def getDirectionInfo(xml):
    root = ET.fromstring(xml) #root is body
    route = root.find('route')
    directions = route.findall('direction')
    dirDict = {}
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

def getDirectionStopList(xml,dirTag):
    stopDict = getStopInfo(xml)
    stopTags = getDirectionInfo(xml)[dirTag][2]
    allstops = getStops(xml)
    dirStops = [getStop(xml,stopTag) for stopTag in stopTags]
    return dirStops

def getDistFromOrigin(stop):
    return float(stop.get('totalDist'))

def addDistDataToStops(stoplist):
    stoplist[0].set('totalDist','0')
    stoplist[0].set('distToPred','0')
    for i in range(1,len(stoplist)):
        pred = getStopDist(stoplist[i],stoplist[i-1])
        total = getDistFromOrigin(stoplist[i-1])+pred
        print i,pred,total
        stoplist[i].set('totalDist',str(total))
        stoplist[i].set('distToPred',str(pred))
    #return stoplist

def getDistFromPred(stop):
    return float(stop.get('distToPred'))

def insertPointToStops(routepoints,newpoint):
    
    return 0

#somehow calculate distance from one stop to the next, store in a dictionary indexed
#by coordinates. No, store in XML objects.

#have tag-indexed dictionary that gives distance from start
#have coord indexed dictionary (for a direction?) that gives tag

# route lat lon -> percent completion

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

def getBusProgress(bus):
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
    #stops=getStops(xml)
    dirTag = '1_0_var0'
    stops = getDirectionStopList(xml,dirTag)
    addDistDataToStops(stops)
    print getStopDist(stops[0],stops[len(stops)-1])
    print stops[0].get('totalDist'),stops[len(stops)-1].get('totalDist')
    print stops[0].get('distToPred'),stops[len(stops)-1].get('distToPred')
    for stop in stops:
        print getDistFromOrigin(stop)
    #makeOneWayStopPath(xml)
    print ''
    #makeReturnStopPath(xml)
main()

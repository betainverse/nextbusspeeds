#!/usr/bin/python

import urllib2,time
import xml.etree.ElementTree as ET
from datetime import datetime

def getTimeStamp():
    #2013-02-13 13:58:38.431522
    timestamp = '%s'%datetime.today()
    return timestamp.split('.')[0]

def getXML(route,time):
    r=str(route)
    t=str(time)
    url='http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=mbta&r='+r+'&t='+t
    response = urllib2.urlopen(url)
    xml = response.read()
    return xml

def getTime(xml):
    #The time in msec since the epoch. If you specify a time of 0, then
    #data for the last 15 minutes is provided.
    root = ET.fromstring(xml) #root is body
    lastTime = root.find('lastTime')
    time=lastTime.get('time')
    return int(time)
    #print body

def getDistance(lat1,lon1,lat2,lon2):
    deltalat = abs(lat1-lat2)
    deltalon = abs(lon1-lon2)
    deltalatmi = deltalat*69
    deltalonmi = deltalon*49
    return sqrt(deltalatmi**2+deltalonmi**2)

def getTimeDiff(t1,t2):
    #convert from msec
    t1i=int(t1) #should not need to cast as int
    t2i=int(t2)
    msec = t2i-t1i
    sec = msec/1000.0
    minutes = sec/60.0
    return minutes

def printResults(xml):
    root = ET.fromstring(xml) #root is body
    buses = root.findall('vehicle')
    #print xml
    for bus in buses:
        busID=bus.get('id')
        predictable=bus.get('predictable')
        destination = getDestination(bus.get('dirTag'))
        lat = bus.get('lat')
        route = getRoutename(bus.get('routeTag'))
        if destination == 'Harvard':
            print route,busID,destination,lat,predictable
        #print bus.tag, bus.attrib

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

def getBuses(xml,desiredDest):
    root = ET.fromstring(xml) #root is body
    buses = root.findall('vehicle')
    #print xml
    busDict = {}
    for bus in buses:
        busID=bus.get('id')
        predictable=bus.get('predictable')
        destination = getDestination(bus.get('dirTag'))
        lat = float(bus.get('lat'))
        route = getRoutename(bus.get('routeTag'))
        if destination == desiredDest:
            busDict[busID]=lat
    return busDict

def collectData(routenum,destination,prevTime=0):
    HarvardLatMax=42.37513
    runningBuses = {} #BusID, (startTime (int,msec),prevLat,starttimestamp?,prevLong)
    pastBuses = {} #BusId, totalTime (float,min)
    while True:
        try:
            xml=getXML(routenum,0)
            busDict = getBuses(xml,destination)
            #print busDict.keys()
            #print runningBuses.keys()
            for bus in runningBuses.keys():
                startTime = runningBuses[bus][0]
                maxLat = runningBuses[bus][2]
                startTimeStamp = runningBuses[bus][1]
                if bus in busDict.keys():
                    print bus,startTimeStamp,getTimeStamp().split()[1],maxLat
                elif maxLat > 42.368:
                    newID = bus + '-%d'%startTime
                    pastBuses[newID] = getTimeDiff(startTime,prevTime)
                    print bus, "finished in %0.1f"%pastBuses[newID],startTimeStamp,getTimeStamp().split()[1]#,startTime
                    del runningBuses[bus]
                else:
                    print 'bus ',bus,'disappeared %s'%getTimeStamp().split()[1],maxLat
                    #If the bus hasn't gotten far enough north, then it just briefly disappeared from the nextbus list.
                #remove bus from running buses, add to past buses
                #worry if a bus drops off the list mid-route, deal later
            for bus in busDict.keys():
                latitude = busDict[bus]
                if bus in runningBuses.keys():
                    startTime = runningBuses[bus][0]
                    prevMaxLat = runningBuses[bus][2]
                    startTimeStamp = runningBuses[bus][1]
                    if latitude > prevMaxLat:
                        runningBuses[bus]=(startTime,startTimeStamp,latitude) #updatemaxlats for running buses
                    else:
                        runningBuses[bus]=(startTime,startTimeStamp,prevMaxLat)
                else:
                    startTimeStamp = getTimeStamp()
                    runningBuses[bus]=(prevTime,startTimeStamp,latitude)
            prevTime = getTime(xml) 
        except Exception, e:
            print e
        time.sleep(15)

def main():
    #http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=mbta&r=1 gives 
    #<route tag="1" title="1" color="330000" oppositeColor="ffffff" latMin="42.3297899" latMax="42.37513" lonMin="-71.11851" lonMax="-71.07354">
    #<direction tag="1_0_var0" title="Harvard Station via Mass. Ave." name="Outbound" useForUI="true">
    #CT1 = 701
    #0 is northbound for CT1
    #xml = getXML(701,0)
    print getTimeStamp()
    xml = getXML(1,0)
    printResults(xml)
    starttime=getTime(xml)
    print starttime
    collectData(1,'Harvard',starttime)

main()

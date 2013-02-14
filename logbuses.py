#!/usr/bin/python

import urllib2,time
import xml.etree.ElementTree as ET
from datetime import datetime
from sys import argv

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
        return str(routenum)

def getBuses(xml):
    root = ET.fromstring(xml) #root is body
    buses = root.findall('vehicle')
    return buses

def parseBus(vehicle):
    busID=vehicle.get('id')
    predictable=vehicle.get('predictable')
    destination = getDestination(vehicle.get('dirTag'))
    lat = float(vehicle.get('lat'))
    lon = float(vehicle.get('lon'))    
    return "%s %s %0.7f %0.7f %s"%(busID,destination,lat,lon,getTimeStamp())

def collectData(routenums):
    while True:
        for routenum in routenums:
            try:
                xml=getXML(routenum,0)
                buses = getBuses(xml)
                if len(buses)>0:
                    logfilename = 'Route%s-%s.log'%(getRoutename(routenum),getTimeStamp().split()[0])
                    logfile = open(logfilename, 'a')
                    for bus in buses:
                        logfile.write(parseBus(bus)+'\n')
                    logfile.close()
            except Exception, e:
                print e
        time.sleep(60)

def main():
    #http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=mbta&r=1 gives 
    #<route tag="1" title="1" color="330000" oppositeColor="ffffff" latMin="42.3297899" latMax="42.37513" lonMin="-71.11851" lonMax="-71.07354">
    #<direction tag="1_0_var0" title="Harvard Station via Mass. Ave." name="Outbound" useForUI="true">
    #CT1 = 701
    #0 is northbound for CT1
    #xml = getXML(701,0)
    print getTimeStamp()
    collectData(argv[1:])

main()

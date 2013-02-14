nextbusspeeds
=============

A degree of latitude is approximately 69 miles, and a minute of latitude is approximately 1.15 miles. A second of latitude is approximately 0.02 miles, or just over 100 feet.

A degree of longitude varies in size. At the equator, it is approximately 69 miles, the same size as a degree of latitude. The size gradually decreases to zero as the meridians converge at the poles. At a latitude of 45 degrees, a degree of longitude is approximately 49 miles. Because a degree of longitude varies in size, minutes and seconds of longitude also vary, decreasing in size towards the poles.

>> str(datetime.timedelta(seconds=666))

>>> import time, datetime
>>> a = time.strptime("00:11:06", "%H:%M:%S")
>>> datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).seconds
666

2013-02-13 18:27:06
<?xml version="1.0" encoding="utf-8" ?> 
<body copyright="All data copyright MBTA 2013.">
<vehicle id="2122" routeTag="1" dirTag="1_1_var0" lat="42.3730369" lon="-71.1173871" secsSinceReport="43" predictable="true" heading="272"/>
<vehicle id="2282" routeTag="1" dirTag="1_1_var0" lat="42.3490668" lon="-71.0886474" secsSinceReport="28" predictable="true" heading="161"/>
<vehicle id="2246" routeTag="1" dirTag="1_1_var0" lat="42.3369127" lon="-71.0775184" secsSinceReport="13" predictable="true" heading="138"/>
<vehicle id="2135" routeTag="1" dirTag="1_0_var0" lat="42.3430238" lon="-71.0853264" secsSinceReport="28" predictable="true" heading="332"/>
<vehicle id="2209" routeTag="1" dirTag="1_0_var0" lat="42.3352381" lon="-71.0753224" secsSinceReport="73" predictable="true" heading="317"/>
<vehicle id="2218" routeTag="1" dirTag="1_0_var0" lat="42.3718487" lon="-71.1150643" secsSinceReport="13" predictable="true" heading="319"/>
<vehicle id="2243" routeTag="1" dirTag="1_1_var0" lat="42.3358047" lon="-71.0760425" secsSinceReport="28" predictable="true" heading="141"/>
<vehicle id="0829" routeTag="1" dirTag="1_1_var0" lat="42.3425504" lon="-71.0846167" secsSinceReport="58" predictable="true" heading="133"/>
<vehicle id="2242" routeTag="1" dirTag="1_1_var0" lat="42.37299" lon="-71.1173275" secsSinceReport="43" predictable="true" heading="272"/>
<vehicle id="2249" routeTag="1" dirTag="1_0_var0" lat="42.3630561" lon="-71.0995561" secsSinceReport="28" predictable="true" heading="299"/>
<vehicle id="2134" routeTag="1" dirTag="1_1_var0" lat="42.3357922" lon="-71.076246" secsSinceReport="28" predictable="true" heading="141"/>
<vehicle id="2192" routeTag="1" dirTag="1_1_var0" lat="42.3435274" lon="-71.0859545" secsSinceReport="13" predictable="true" heading="161"/>
<lastTime time="1360798004944"/>
</body>


     dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))^2 + cos(lat1) * cos(lat2) * (sin(dlon/2))^2
    c = 2 * atan2( sqrt(a), sqrt(1-a) )
    d = R * c (where R is the radius of the Earth) 

Note: this formula does not take into account the non-spheroidal (ellipsoidal) shape of the Earth. It will tend to overestimate trans-polar distances and underestimate trans-equatorial distances. The values used for the radius of the Earth (3961 miles & 6373 km) are optimized for locations around 39 degrees from the equator (roughly the Latitude of Washington, DC, USA). 

Decimal Degrees = Degrees + minutes/60 + seconds/3600
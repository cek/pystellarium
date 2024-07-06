from Stellarium import Stellarium
from datetime import datetime
from geopy import geocoders
from dateutil import parser
import time


s = Stellarium()

s.planet = "Earth"
s.region = "North America"
s.timerate = 0

# Oakland, CA
(latitude, longitude) = (37.80437088012695,-122.27079772949219)
s.setLatlong(latitude, longitude)

timeString = "01/20/2024 01:00:00 PST"
dt = parser.parse(timeString)
print(dt.strftime("%m %d %Y %H:%M:%S %Z"))
jday = s.datetimeToJday(dt)

s.fov = 5.5
# TZ hack
minsPerDay = 24*60
dt = 1.0/minsPerDay
jday += 8./24.
for i in range(10):
    s.jday = jday
    time.sleep(1)
    jday += dt

s.mainView_customScreenshotWidth = 2*1920
s.mainView_customScreenshotHeight = 2*1080
s.mainView_flagUseCustomScreenshotSize = True

#s.actions.saveScreenshotGlobal()

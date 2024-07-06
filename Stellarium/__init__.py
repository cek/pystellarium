import requests
import subprocess
from . import _StellariumActions
from . import _StellariumProperties
import jdcal
import math
import datetime

class Stellarium(_StellariumProperties.StellariumProperties):
    def __init__(self, baseUrl='http://localhost:8090/api/'):
        self.baseUrl = baseUrl
        self.actions = _StellariumActions.StellariumActions(self)
        self._propId = '-2'
        self._propertyValues = {}
        # Ensure base url ends in '/'
        if self.baseUrl[-1] != '/':
            self.baseUrl += '/'

    def _get(self, url, params=''):
        if params:
            response = requests.get(self.baseUrl + url, params=params)
        else:
            response = requests.get(self.baseUrl + url)
        if response.status_code != 200:
            raise ValueError(f"Stellarium get request failed with status {response.status_code}.")
        return response.json()

    def _post(self, cmd, name, payload):
        param = {name : str(payload) }
        res = requests.post(self.baseUrl + cmd, data = param)
        if res.status_code != 200:
            raise ValueError(f"Stellarium post request failed with status {res.status_code}.")
    def _postParams(self, cmd, params):
        res = requests.post(self.baseUrl + cmd, data = params)
        if res.status_code != 200:
            raise ValueError(f"Stellarium post request failed with status {res.status_code}.")
    def getActions(self):
        return self._get('stelaction/list')

    def getProperties(self):
        return self._get('stelproperty/list')

    def getStatus(self, propId = None, actionId = None):
        if not propId and not actionId:
            return self._get('main/status')
        if not propId:
            params = {'actionId': actionId}
        elif not actionId:
            params = {'propId': propId}
        else:
            params = {'actionId': actionId, 'propId': propId}
        return self._get('main/status', params=params)
    def getPlugins(self):
        return self._get('main/plugins')
    def getView(self):
        return self._get('main/view')
    def time(self, time, timerate):
        params = {'time': str(time), 'timerate': str(timerate)}
        return self._postParams('main/time', params)
    def move(self, x, y):
        params = {'x': str(x), 'y': str(y)}
        return self._postParams('main/move', params)

    def removeOverlays(self):
        pass

    @property
    def fov(self):
        status = self.getStatus()
        return status['view']['fov']
    @fov.setter
    def fov(self, fov):
        return self._post('main/fov', 'fov', fov)

    @property
    def window(self):
        return self.windowDimensions
    @window.setter
    def window(self, l):
        self.windowDimensions = l
        params = {'w': l[0], 'h': l[1]}
        return self._postParams('main/window', params)

    def utcTime(self):
        return self.getStatus()['time']['utc']

    def localTime(self):
        return self.getStatus()['time']['local']

    def isTimeNow(self):
        return self.getStatus()['time']['isTimeNow']

    def timeZone(self):
        return self.getStatus()['time']['timeZone']

    def deltaT(self):
        return self.getStatus()['time']['deltaT']

    @property
    def jday(self):
        status = self.getStatus()
        return status['time']['jday']
    @jday.setter
    def jday(self, jday):
        return self._post('main/time', 'time', jday)

    @property
    def timerate(self):
        status = self.getStatus()
        return status['time']['timerate']
    @timerate.setter
    def timerate(self, timerate):
        return self._post('main/time', 'timerate', timerate)

    @property
    def latitude(self):
        status = self.getStatus()
        return status['location']['latitude']
    @latitude.setter
    def latitude(self, lat):
        params = {'latitude' : str(lat) }
        return self._postParams('location/setlocationfields', params)

    def getLocations(self):
        return self._get('location/list')
    def getCountries(self):
        return self._get('location/countrylist')
    def getPlanets(self):
        return self._get('location/planetlist')

    # Location
    @property
    def longitude(self):
        status = self.getStatus()
        return status['location']['longitude']
    @longitude.setter

    def longitude(self, long):
        params = {'longitude' : str(long) }
        return self._postParams('location/setlocationfields', params)

    def setLatlong(self, lat, long):
        params = {'latitude': str(lat), 'longitude': str(long)}
        return self._postParams('location/setlocationfields', params)

    # Non-functional?
    def setLocation(self, loc):
        params = {'id': loc}
        return self._postParams('location/setlocationfields', params)

    # Non-functional?
    def locationSearch(self, loc):
        params = {'term': loc}
        return self._get('locationsearch/search', params)

    def locationNearby(self, lat, long, radius):
        params = {'planet': 'Earth', 'latitude': lat, 'longitude': long, 'radius': radius}
        return self._get('locationsearch/nearby', params)

    @property
    def altitude(self):
        status = self.getStatus()
        return status['location']['altitude']
    @altitude.setter
    def altitude(self, alt):
        params = {'altitude' : str(alt) }
        return self._postParams('location/setlocationfields', params)

    @property
    def region(self):
        status = self.getStatus()
        return status['location']['region']
    @region.setter
    def region(self, c):
        params = {'region' : str(c) }
        return self._postParams('location/setlocationfields', params)

    @property
    def planet(self):
        status = self.getStatus()
        return status['location']['planet']
    @planet.setter
    def planet(self, p):
        params = {'planet' : str(p) }
        return self._postParams('location/setlocationfields', params)

    def jdayToDatetime(self, t, localconvert = True):
        gdate = jdcal.jd2gcal(t, 0)
        gtime = gdate[3]
        if localconvert:
            gtime += self.getStatus()['time']['gmtShift']
        gtime *= 24
        hours = math.floor(gtime)
        gtime = 60 * (gtime - hours)
        mins = math.floor(gtime)
        gtime = 60 * (gtime - mins)
        secs = math.floor(gtime)
        usecs = math.floor(1000000. * (gtime - secs))
        return datetime.datetime(gdate[0], gdate[1], gdate[2], hours, mins, secs, usecs)

    def datetimeToJday(self, dt):
        # Note that we return a string, which provides more precision than a single float
        jdate = jdcal.gcal2jd(dt.year, dt.month, dt.day)
        frac = dt.hour / 24.0 + dt.minute / (24.*60) + dt.second / (24.*60.*60.)
        return jdate[0] + jdate[1] + frac


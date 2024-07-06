from Stellarium import Stellarium
import datetime

def test_time():
    s = Stellarium()
    s.actions.returnToCurrentTime()
    dt = datetime.datetime.now()
    s.time = s.datetimeToJday(dt)
    newdt = s.jdayToDatetime(s.time, localconvert=False)
    # There is some loss of precision in storing jday in a single double.
    # As such, allow some fuzz
    assert (newdt - dt).total_seconds() < 1

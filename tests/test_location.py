from Stellarium import Stellarium

def test_location():
    s = Stellarium()
    (latitude, longitude) = (37.80437088012695,-122.27079772949219)
    s.setLatlong(latitude, longitude)
    assert s.latitude == latitude
    assert s.longitude == longitude
    s.region = "South America"
    assert s.region == "South America"
    s.planet = "Mars"
    assert s.planet == "Mars"
    s.region = "North America"
    s.planet = "Earth"

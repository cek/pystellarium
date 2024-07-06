from Stellarium import Stellarium

def test_properties():
    s = Stellarium()
    a = s.getProperties()
    assert len(a) > 0
    for prop in a.items():
        propId = prop[0]
        value = prop[1]['value']
        variantType = prop[1]['variantType']
        typeString = prop[1]['typeString']
        typeEnum = prop[1]['typeEnum']
        assert len(propId) > 0
        assert len(typeString) > 0
        assert variantType 

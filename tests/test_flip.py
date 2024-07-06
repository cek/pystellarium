from Stellarium import Stellarium

def test_flip():
    s = Stellarium()
    s.actions.verticalFlip = True
    assert s.actions.verticalFlip
    s.actions.verticalFlip = False
    assert not s.actions.verticalFlip
    s.verticalFlip = True
    assert s.verticalFlip
    s.verticalFlip = False
    assert not s.verticalFlip

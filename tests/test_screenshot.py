from Stellarium import Stellarium

def test_screenshot():
    stel = Stellarium()
    stel.actions.saveScreenshotGlobal()

from Stellarium import Stellarium

def test_actions():
    s = Stellarium()
    a = s.getActions()
    assert len(a) > 0
    for item in a.items():
        for action in item[1]:
            actionName = action['id']
            isBoolean = action['isCheckable']
            assert len(actionName) > 0
            text = action['text']
            assert len(text) > 0

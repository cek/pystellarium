# Generate methods for supported stellarium actions
import sys
from StellariumBase import Stellarium

def methodName(actionName):
    # Transform action method name to legal camel case
    #   Remove leading 'action' and 'Script/'
    #   Remove '_' from e.g. This_Action_Name
    #   Strip script name suffix ('.scc')
    #   Replace '.' and '-' with '_'
    #   Convert first character to lower case to give us camel case names
    if actionName.startswith('action'):
        actionName = actionName[6:]
    if actionName.startswith('Script/'):
        actionName = actionName[7:]
    if actionName.endswith('.ssc'):
        actionName = actionName[:-4]
    actionName = actionName.replace('_', '')
    actionName = actionName.replace('.', '_')
    actionName = actionName.replace('-', '_')
    actionName = actionName[0].lower() + actionName[1:]
    return actionName

stel = Stellarium()

# Get list of supported actions
actions = stel.getActions()

# Write to implementation file
sys.stdout = open('_StellariumActions.py', 'wt')

# Gather 'checkable' action names, which will we implement as properties
actionPropNames = []
for item in actions.items():
    for action in item[1]:
        if action['isCheckable']:
            actionPropNames.append(action['id'])

print("""
# Automatically generated by generate.py -- do not edit.
class StellariumActions:
    def __init__(self, parent):
        self._parent = parent
        self._actionId = '-2'
        self._actionValues = {}
    def _update(self):
        s = self._parent.getStatus(actionId=self._actionId)
        ac = s['actionChanges']
        self._actionId = ac['id']
        ch = ac['changes']
        for change in ch.items():
            self._actionValues[change[0]] = change[1]
    def _action(self, action):
        return self._parent._post('stelaction/do', 'id', action)
    def _getValue(self, id):
        self._update()
        return self._actionValues[id]
    def _setValue(self, id):
        self._action(id)
""")

for item in actions.items():
    for action in item[1]:
        actionId = action['id']
        actionName = methodName(actionId)
        docString = action['text']
        docString = docString.replace('"', "'")
        isCheckable = action['isCheckable']
        if isCheckable:
            # Make checkable actions properties
            print(f"    @property")
            print(f"    def {actionName}(self):")
            print(f'        """{docString}"""')
            print(f"        return self._getValue('{actionId}')")
            print(f"    @{actionName}.setter")
            print(f"    def {actionName}(self, value):")
            print(f"        self._setValue('{actionId}')")
        else:
            print(f"    def {actionName}(self):")
            print(f'        """{docString}"""')
            print(f"        return self._action('{action['id']}')")

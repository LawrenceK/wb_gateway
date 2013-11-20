from turbogears.database import PackageHub
from sqlobject import *

hub = PackageHub("WebBrickConfig")
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass


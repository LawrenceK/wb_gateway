from turbogears.database import PackageHub
from sqlobject import *

hub = PackageHub("WebBrickGateway")
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass


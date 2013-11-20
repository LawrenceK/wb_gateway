# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

from turbogears.database import PackageHub
from sqlobject import *

hub = PackageHub("WebBrickConfig")
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass


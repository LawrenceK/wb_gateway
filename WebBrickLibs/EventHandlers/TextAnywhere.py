# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 



import logging

from EventLib.Event import Event
from EventLib.Status          import StatusVal
from EventLib.SyncDeferred    import makeDeferred

from EventHandlers.BaseHandler import BaseHandler
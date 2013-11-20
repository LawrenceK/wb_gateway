# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: Certificate.py 2612 2008-08-11 20:08:49Z graham.klyne $

"""
Module to handle WebBrickSystems certificates.

Load attributes into the object?

"""
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

siteKey = "site"
wbsKey = "WebBrickSystems"

class Certificate:
    def __init__(self):
        pass

    def load(self,path):
        pass

class Request:
    def __init__(self):
        pass

    def package(self):
        #package user data and user certificate.
        pass

# End. $Id: Certificate.py 2612 2008-08-11 20:08:49Z graham.klyne $

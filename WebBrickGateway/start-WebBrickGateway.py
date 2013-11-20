# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#
# $Id: start-WebBrickGateway.py 2611 2008-08-11 20:05:08Z graham.klyne $
#
import sys

from WebBrickGateway.main import start

if __name__ == "__main__":

    # First look on the command line for a desired config file,
    if len(sys.argv) > 1:
        start(sys.argv[1])
    else:
        start()

# End. $Id: start-WebBrickGateway.py 2611 2008-08-11 20:05:08Z graham.klyne $

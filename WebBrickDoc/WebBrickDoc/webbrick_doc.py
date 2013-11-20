# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

#
#
#!/usr/bin/python
#
# $Id: webbrick_doc.py 2612 2008-08-11 20:08:49Z graham.klyne $
#

import webbrowser
import os.path
import pkg_resources

def main():
    #iname = os.path.join( os.path.split(__file__)[0], "index.html")
    iname = pkg_resources.resource_filename("WebBrickDoc", "../index.html")
    webbrowser.open_new( iname )

if __name__ == "__main__":
    main()
    
# End. $Id: webbrick_doc.py 2612 2008-08-11 20:08:49Z graham.klyne $

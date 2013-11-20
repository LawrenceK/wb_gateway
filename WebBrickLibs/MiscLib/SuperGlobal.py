# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: SuperGlobal.py 2612 2008-08-11 20:08:49Z graham.klyne $

import __main__

class SuperGlobal:
    """
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/457667

    Here so can use in testing.

    Creates globals.

    i.e.
    superglobal = SuperGlobal()
    superglobal.data = ....

    However many times you create SuperGlobal it access the same data.
    """

    def __getattr__(self, name):
        return __main__.__dict__.get(name, None)
        
    def __setattr__(self, name, value):
        __main__.__dict__[name] = value
        
    def __delattr__(self, name):
        if __main__.__dict__.has_key(name):
            del  __main__.__dict__[name]

# $Id: log.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# coherenece log replacement to to hook direct to python logging.

import logging

#_log = logging.getLogger( "coherence" )

class Loggable(object):

    # I want to be able to do something at init.
    def __new__(cls, *args, **kwargs):
        obj = super(Loggable, cls).__new__(cls, *args, **kwargs)
        obj._log = logging.getLogger( cls.__module__ )
#	print cls.__module__
        return obj

    def critical(self, msg, *args):
        self._log.critical(msg, *args)

    def msg(self, message, *args):
        self._log.info(message, *args)

    def error(self, *args):
        self._log.error(*args)

    def exception(self, *args):
        self._log.exception(*args)

    def warning(self, *args):
        self._log.warning(*args)

    def info(self, *args):
        self._log.info(*args)

    def debug(self, *args):
        self._log.debug(*args)

    def log(self, *args):
        self._log.info(*args)

def error(cat, format, *args):
	logging.getLogger( cat ).error( format, *args )

def warning(cat, format, *args):
	logging.getLogger( cat ).warning( format, *args )

def info(cat, format, *args):
	logging.getLogger( cat ).info( format, *args )

def debug(cat, format, *args):
	logging.getLogger( cat ).debug( format, *args )

def exception(cat, format, *args):
	logging.getLogger( cat ).exception( format, *args )

def log(cat, format, *args):
	logging.getLogger( cat ).info( format, *args )

def human2level(levelname):
    levelname = levelname.lower()
    if levelname.startswith('none'):
        return logging.NOTSET
    if levelname.startswith('error'):
        return logging.ERROR
    if levelname.startswith('warn'):
        return logging.WARNING
    if levelname.startswith('info'):
        return logging.INFO
    if levelname.startswith('debug'):
        return logging.DEBUG
    return logging.DEBUG

def init(logfile=None,loglevel='*:2'):
    pass
 
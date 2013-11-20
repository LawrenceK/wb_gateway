#! /usr/bin/env python
#
# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>

import os, sys, logging

from twisted.internet import reactor
from twisted.python import usage

from coherence.base import Coherence

from configobj import ConfigObj

class Options(usage.Options):
    optParameters = [['configfile', 'c', '', 'path to configfile'],
                    ]

def main(options):

    # get settings or options
    def setConfigFile(filename):
        if filename is '':
            filename = './coherence.conf'
        return filename

    config = ConfigObj( setConfigFile( options['configfile']))
    c = Coherence(config)
    #c = Coherence(plugins={'FSStore': {'content_directory':'tests/content'},
    #                       'Player': {})
    #c.add_plugin('FSStore', content_directory='tests/content', version=1)
    
if __name__ == '__main__':

#    logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG,filename="coherence.log")

    options = Options()
    try:
        options.parseOptions()
    except usage.UsageError, errortext:
        print '%s: %s' % (sys.argv[0], errortext)
        print '%s: Try --help for usage details.' % (sys.argv[0])
        sys.exit(1)

    reactor.callWhenRunning(main, options)
    reactor.run()

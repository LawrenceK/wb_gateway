# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

from coherence import log

class BaseClient(log.Loggable):
    #  Base for any client to a UPNP service

    def __init__(self, service):
        self.service = service
        self.namespace = service.get_type()
        self.url = service.get_control_url()
        self.service.subscribe()
        self.service.client = self

    def remove(self):
        self.service.remove()
        self.service = None
        self.namespace = None
        self.url = None
        del self

    def subscribe_for_variable(self, var_name, callback, signal=True):
        self.service.subscribe_for_variable(var_name, instance=0, callback=callback,signal=signal)


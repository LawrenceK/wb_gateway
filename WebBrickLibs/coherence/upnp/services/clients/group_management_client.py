# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

from coherence import log

from coherence.upnp.services.clients.base_client import BaseClient

class GroupManagementClient(BaseClient):
    #  Base for any client to a UPNP service

    def __init__(self, service):
        super(GroupManagementClient,self).__init__(service)
        self.GroupCoordinatorIsLocal = None
        self.LocalGroupUUID = None

        self.subscribe_for_variable("GroupCoordinatorIsLocal", self.group_management_update)
        self.subscribe_for_variable("LocalGroupUUID", self.group_management_update)
# or instead of subscribe
#	    return self.device_properties.service.get_state_variable("ZoneName").value

    def group_management_update(self, variable):
        if variable.name == "GroupCoordinatorIsLocal":
            self.GroupCoordinatorIsLocal = variable.value
            self.debug("GroupCoordinatorIsLocal %s", self.GroupCoordinatorIsLocal )
            
        elif variable.name == "LocalGroupUUID":
            self.LocalGroupUUID = variable.value
            self.debug("LocalGroupUUID %s", self.LocalGroupUUID )


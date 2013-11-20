# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php or see LICENSE file.
# Copyright 2007-2008 Brisa Team <brisa-develop@garage.maemo.org>

from brisa.core.reactors import install_default_reactor
reactor = install_default_reactor()

# from brisa.core.reactors import GLib2Reactor
# reactor = GLib2Reactor()

# from brisa.core.reactors import Gtk2Reactor
# reactor = Gtk2Reactor()

import sys

from brisa.upnp.control_point.control_point_webbrick import ControlPointWB
from brisa.core.threaded_call import run_async_function


class CommandLineControlPointAV(ControlPointWB):

    def __init__(self):
        ControlPointWB.__init__(self)
        self.running = True
        self._initial_subscribes()
        self.devices_found = []
        self.commands = {'start': self._search,
                         'stop': self._stop,
                         'list': self._cmd_list_devices,
                         'exit': self._exit,
                         'help': self._help}

    def _initial_subscribes(self):
        self.subscribe('new_device_event', self.on_new_device)
        self.subscribe('remove_device_event', self.on_remove_device)

    def on_new_device(self, dev):
        self.devices_found.append(dev)
        if dev.devices:
            for child_dev in dev.devices.values():
                self.devices_found.append(child_dev)

    def on_remove_device(self, udn):
        for dev in self.devices:
            if dev.udn == udn:
                self.devices_found.remove(dev)
                break

    def _cmd_list_devices(self):
        n = 0
        for dev in self.devices_found:
            print 'device %d:' % n
            print '\tudn:', dev.udn
            print '\tmodel_name:', dev.model_name
            print '\tfriendly_name:', dev.friendly_name
            print '\tservices:', dev.services
            print '\ttype:', dev.device_type
            #if dev.devices:
            #    print '\tchild devices:'
            #    for child_dev in dev.devices.values():
            #        print '\t\tudn:', child_dev.udn
            #        print '\t\tfriendly_name:', child_dev.friendly_name
            #        print '\t\tservices:', dev.services
            #        print '\t\ttype:', child_dev.device_type
            print
            n += 1

    def _cmd_set_server(self, id):
        self._current_server = self.devices_found[id]

    def _cmd_set_render(self, id):
        self._current_renderer = self.devices_found[id]

    def _cmd_browse(self, id):
        result = self.browse(id, 'BrowseDirectChildren', '*', 0, 10)
        result = result['Result']
        for d in result:
            print "%s %s %s" % (d.id, d.title, d.upnp_class)
    
    def av_actions(self):
        """ Pauses the rendering.
        """
        avt = self.get_avt_service()
        print 
        print '\tactions:', avt.get_actions()
    
    def av_vars(self):
        """ Pauses the rendering.
        """
        avt = self.get_avt_service()
        print 
        print '\tvariables:', avt.get_variables()
    
    def sub_service(self):
        avt = self.get_avt_service()
        avt.event_subscribe(self.event_host, self._event_subscribe_callback, None, True, self._event_renew_callback)
    
    def _event_subscribe_callback(self, cargo, subscription_id, timeout):
        print "Event subscribe done!"
        print 'Subscription ID: ' + str(subscription_id)
        print 'Timeout: ' + str(timeout)
    
    def _event_renew_callback(self, cargo, subscription_id, timeout):
        print "Event renew done!"
        print 'Subscription ID: ' + str(subscription_id)
        print 'Timeout: ' + str(timeout)
    
    def _event_callback(self, name, value):
        print "Event message!"
        print 'State variable:', name
        print 'Variable value:', value

        
    def sub_vars(self):
        avt = self.get_avt_service()
        print '\tsubscribe to: 1'
        var = avt.subscribe_for_variable("CurrentTrack", self._event_callback)
        print '\tsubscribe to: 2'
        var = avt.subscribe_for_variable("CurrentTrackDuration", self._event_callback)
        print '\tsubscribe to: 3'
        var = avt.subscribe_for_variable("TransportState", self._event_callback)
        print '\tsubscribe DONE'
        
    def get_vars(self):
        avt = self.get_avt_service()
        var = avt.get_state_variable("CurrentTrack").get_value()
        print var
        var = avt.get_state_variable("CurrentTrackDuration").get_value()
        print var
        var = avt.get_state_variable("TransportState").get_value()
        print var

    
        
    def _search(self):
        self.start_search(600, 'upnp:rootdevice')
        print 'search started'

    def _stop(self):
        self.stop_search()
        print 'search stopped'

    def _help(self):
        print 'commands: start, stop, list, ' \
              'browse, set_server, set_render, play, exit, help, av_actions, av_vars, av_play, av_pause'

    def _exit(self):
        self.running = False

    def run(self):
        self.start()
        run_async_function(self._handle_cmds)
        reactor.add_after_stop_func(self.stop)
        reactor.main()

    def _handle_cmds(self):
        try:
            while self.running:
                command = str(raw_input('>>> '))
                try:
                    self.commands[command]()
                except KeyError:
                    if command.startswith('browse'):
                        self._cmd_browse(command.split(' ')[1])
                    elif command.startswith('set_server'):
                        self._cmd_set_server(int(command.split(' ')[1]))
                    elif command.startswith('set_render'):
                        self._cmd_set_render(int(command.split(' ')[1]))
                    elif command.startswith('av_play'):
                        self.av_play()
                    elif command.startswith('av_stop'):
                        self.av_stop()
                    elif command.startswith('av_pause'):
                        self.av_pause()
                    elif command.startswith('av_next'):
                        self.av_next() 
                    elif command.startswith('av_previous'):
                        self.av_previous()
                    elif command.startswith('av_actions'):
                        self.av_actions()    
                    elif command.startswith('av_vars'):
                        self.av_vars()
                    elif command.startswith('av_sub_service'):
                        self.sub_service()
                    elif command.startswith('av_sub_vars'):
                        self.sub_vars()
                    elif command.startswith('av_get_vars'):
                        self.get_vars()
                    
                    else:
                        print 'Invalid command, try help'
                command = ''
        except KeyboardInterrupt, k:
            print 'quiting'

        reactor.main_quit()


def main():
    print "WebBrick Command Line ControlPoint \n"
    cmdline = CommandLineControlPointAV()
    cmdline.run()

if __name__ == "__main__":
    main()

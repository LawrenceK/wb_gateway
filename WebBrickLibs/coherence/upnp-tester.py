#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2008, Frank Scholz <coherence@beebits.net>

# upnp-tester.py
#
# very basic atm
#
# provides these functions:
#
# list           - display all devices
# extract <uuid> - extract device and service xml files and put them in a
#                  /tmp/<uuid> directory
# send <uuid>    - pack the before extracted xml files in a tar.gz and
#                  send them via email to the Coherence googlemail account
#

#LPK
#   instead of /tmp use gettempdir for platform temporary location.
#   use worker thread for windows command handling.
#
from tempfile import gettempdir
tmpdir = gettempdir()

# address to send tgz files
mail_domain = 'googlemail.com'
email_address = 'upnp.fingerprint@googlemail.com'
from_address = ''   # no return address

#mail_domain = 'lklyne.co.uk'
#email_address = 'upnp.fingerprint@lklyne.co.uk'
#from_address = 'upnp.tester@lklyne.co.uk'

import os, os.path, threading, sys

from sets import Set

from twisted.internet import stdio
from twisted.protocols import basic
from twisted.internet import protocol

from twisted.mail import smtp

from twisted.internet import reactor, defer
from twisted.web import client

from twisted.names import client as namesclient
from twisted.names import dns

from coherence.base import Coherence

import StringIO

class SMTPClient(smtp.ESMTPClient):

    """ build an email message and send it to our googlemail account
    """

    def __init__(self, mail_from, mail_to, mail_subject, mail_file, *args, **kwargs):
        smtp.ESMTPClient.__init__(self, *args, **kwargs)
        self.mailFrom = mail_from
        self.mailTo = mail_to
        self.mailSubject = mail_subject
        self.mail_file =  mail_file
        self.mail_from =  mail_from

    def getMailFrom(self):
        result = self.mailFrom
        self.mailFrom = None
        return result

    def getMailTo(self):
        return [self.mailTo]

    def getMailData(self):
        from email.mime.application import MIMEApplication
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg['Subject'] = self.mailSubject
        msg['From'] = self.mail_from
        msg['To'] = self.mailTo
        fp = open(self.mail_file, 'rb')
        tar = MIMEApplication(fp.read(),'x-tar')
        fp.close()
        tar.add_header('Content-Disposition', 'attachment', filename=os.path.basename(self.mail_file))
        msg.attach(tar)
        return StringIO.StringIO(msg.as_string())

    def sentMail(self, code, resp, numOk, addresses, log):
        print 'Sent', numOk, 'messages (', code, ' ', resp, ' ', numOk, ' ', addresses, ' ', log, ')'

class SMTPClientFactory(protocol.ClientFactory):
    protocol = SMTPClient

    def __init__(self, mail_from, mail_to, mail_subject, mail_file, *args, **kwargs):
        self.mail_from = mail_from
        self.mail_to = mail_to
        self.mail_subject = mail_subject
        self.mail_file = mail_file

    def buildProtocol(self, addr):
        return self.protocol(self.mail_from, self.mail_to,
                             self.mail_subject, self.mail_file,
                             secret=None, identity='localhost')


class UI(basic.LineReceiver):
    from os import linesep as delimiter

    def connectionMade(self):
        self.print_prompt()

    def lineReceived(self, line):
        args = line.strip().split()
        if args:
            cmd = args[0].lower()
            if hasattr(self, 'cmd_%s' % cmd):
                getattr(self, 'cmd_%s' % (cmd))(args[1:])
            elif cmd == "?":
                self.cmd_help(args[1:])
            else:
                self.transport.write("""Unknown command '%s'\n"""%(cmd))
        self.print_prompt()

    def cmd_help(self,args):
        "help -- show help"
        methods = Set([ getattr(self, x) for x in dir(self) if x[:4] == "cmd_" ])
        self.transport.write("Commands:\n")
        for method in methods:
            if hasattr(method, '__doc__'):
                self.transport.write("%s\n"%(method.__doc__))

    def cmd_list(self, args):
        "list -- list devices"
        self.transport.write("Devices:\n")
        for d in self.coherence.get_devices():
            self.transport.write(str("%s %s [%s/%s/%s]\n" % (d.friendly_name, ':'.join(d.device_type.split(':')[3:5]), d.st, d.usn.split(':')[1], d.host)))

    def cmd_extract(self, args):
        "extract <uuid> -- download xml files from device"
        
        def extract_device(device):
            # extract single device
            self.transport.write(str("extracting from %s @ %s\n" % (device.friendly_name, device.host)))
            try:
                l = []

                def got_device_ok(page, device):
                    self.transport.write( "\n Ok device %s" %(str(device.get_uuid()) ) )
                    
                def got_device_err(failure, device):
                    self.transport.write( str("\n %s device %s" %(str(failure), str(device.get_uuid()) ) ) )
                    return failure
                    
                def got_service_ok(page, service):
                    self.transport.write( str("\n Ok service %s" %(str(service) ) ) )
                    
                def got_service_err(failure, service):
                    self.transport.write( str("\n %s service %s" %(str(failure), str(service) ) ) )
                    return failure
                    
                def device_extract(workdevice, path):
                    tmp_dir = os.path.join(path,workdevice.get_uuid())
                    # check and clean dircetory.
                    if not os.path.exists(tmp_dir):
                        os.mkdir(tmp_dir)
                    self.transport.write( str("\n device %s" %(workdevice.get_location() ) ) )
                    fname = os.path.join(tmp_dir,'device-description.xml')
                    d = client.downloadPage(workdevice.get_location(),fname)
                    d.addCallback( got_device_ok, workdevice)
                    d.addErrback( got_device_ok, workdevice)
                    l.append(d)

                    for service in workdevice.services:
                        fname = os.path.join(tmp_dir,'%s-description.xml'%service.service_type.split(':',3)[3])
                        self.transport.write( str("\n service %s %s" %(fname, service.get_scpd_url() ) ) )
                        d = client.downloadPage(service.get_scpd_url(),fname)
                        d.addCallback( got_service_ok, service)
                        d.addErrback( got_service_ok, service)
                        l.append(d)


                    for ed in workdevice.devices:
                        device_extract(ed, tmp_dir)

                def finished(result):
                    self.transport.write(str("\nextraction of device %s finished\nfiles have been saved to /%s/%s\n" %(device.friendly_name,tmpdir,device.get_uuid())))
                    for r in result:
                        self.transport.write(str("\nresult %s" % str(r) ))
                        
                    self.print_prompt()

                device_extract(device,tmpdir)

                dl = defer.DeferredList(l)
                dl.addCallback(finished)
            except Exception, msg:
                self.transport.write(str("problem creating download directory %s\n" % msg))

        if len(args) > 0:
            device = self.coherence.get_device_with_id(args[0])
            if device == None:
                self.transport.write("device %s not found - aborting\n" % args[0])
            else:
                extract_device(device)
        else:
            # extract all
            for device in self.coherence.get_devices():
                extract_device(device)

    def cmd_send(self, args):
        "send <uuid> -- send before extracted xml files to the Coherence home base"
        
        def send_device(uuid):
            if os.path.isdir(os.path.join(tmpdir,uuid)) == 1:
                tgz_file_name = os.path.join(tmpdir,uuid+'.tgz')
                cwd = os.getcwd()
                os.chdir(tmpdir)
                import tarfile
                tar = tarfile.open(tgz_file_name, "w:gz")
                for file in os.listdir(os.path.join(tmpdir,uuid)):
                    tar.add(os.path.join(uuid,file))
                tar.close()
                os.chdir(cwd)

                def got_mx(result):
                    mx_list = result[0]
                    mx_list.sort(lambda x, y: cmp(x.payload.preference, y.payload.preference))
                    if len(mx_list) > 0:
                        import socket
                        import getpass
#                        from_address = '@'.join((getpass.getuser(),socket.gethostname()))
                        reactor.connectTCP(str(mx_list[0].payload.name), 25,
                            SMTPClientFactory(from_address,  email_address, 
                                    'xml-files', tgz_file_name))

                mx = namesclient.lookupMailExchange(mail_domain)
                mx.addCallback(got_mx)

        if len(args) > 0:
            send_device(args[0])
        else:
            # send all
            for device in self.coherence.get_devices():
                send_device(device.get_uuid())

    def cmd_quit(self, args):
        "quit -- quits this program"
        reactor.stop()

    cmd_exit = cmd_quit

    def print_prompt(self):
        self.transport.write('>>> ')

class win_command(threading.Thread):
    def __init__(self, ui ):
        threading.Thread.__init__(self)
        self.ui = ui

    def run(self):
        self.ui.print_prompt()
        while True:
            try :
                cmd = sys.stdin.readline()
                self.ui.lineReceived(cmd)
            except Exception, ex:
                import traceback
                traceback.print_exc()

def start_win_command_thread( ui ):
    ui.transport = sys.stdout
    _thread = win_command(ui)
    _thread.setDaemon(True)
    _thread.start()

def main():
    c = Coherence({'logmode':'none', 'webserver':{}, 'controlpoint':'yes', 'start':'yes'})
#    c = Coherence({'logmode':'none'})

    ui = UI()
    ui.coherence = c

    import os
    if os.name == 'nt': #sys.platform == 'win32':
	start_win_command_thread( ui )
    else:
	stdio.StandardIO(ui)

    reactor.run()
    
if __name__ == '__main__':
    main()

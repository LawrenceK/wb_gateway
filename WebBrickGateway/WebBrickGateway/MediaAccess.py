# $Id: MediaAccess.py 2610 2008-08-11 20:04:17Z graham.klyne $

import turbogears
import logging
from urllib import quote
from os import listdir
from os.path import isfile
from socket import gethostbyaddr, gethostname

import cherrypy

from mediaserver.MediaSet import MediaSet
from MiscLib.DomHelpers import parseXmlString, getNamedNodeText, getElemXml, getNamedElem

import ClientProfiles

mediaTemplate="""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML, 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1-strict-dtd">
<html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml" >

<head>
  <title>%s</title>
  <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
  <link href="/static/css/panel.css" rel="stylesheet" />
  <script src="/static/javascript/MochiKit.js"></script>
  <script src="/static/javascript/WebBrick.js"></script>
  <script src="/static/javascript/WbPanel.js"></script>
    <script src="/static/javascript/VlcPlugin.js"></script>
</head>

<body>

    <table class="navTable">
      <tr>
        <td class="navBar" onClick="window.location='/'">Home</td>
        <td class="buttonAbsent" id="backButton">Back</td>
        <td class="buttonAbsent" id="moreButton">More</td>
        <td class="infoBar" id="menuTitle">Lighting and Scenes</td>
      </tr>
    </table>
    
<embed type="application/x-vlc-plugin"
         name="video1"
         id="video1"
         autoplay="no" loop="yes" width="720" height="480"
         target="%s%s" />

<table class="infoTable">
    <tr>
        <td class="navBar" onclick='VLCplay()'>
            Play
        </td>
        <td class="navBar" onclick='VLCpause()'>
            Pause
        </td>
        <td class="navBar" onclick='VLCplay()'>
            Forward
        </td>
        <td class="navBar" onclick='VLCpause()'>
            Rewind
        </td>
        <td class="navBar" onclick='VLCstop()'>
            Stop
        </td>
    </tr>
</table>

</body>

</html>
"""

# --------------------------------------------------
# Media server command and status access class
# --------------------------------------------------
class MediaAccess( MediaSet ):
    """
    Local class to handle queries that are forwarded to a Media server.
    """
    def __init__(self):
        # a dictionary of media server names to media server implementations
        MediaSet.__init__( self )
        self.__log = logging.getLogger( "WebBrickGateway.MediaAccess" )
        self.videoTracks = {
                '0': {'title':'Enterprise Broken Bow Part 1', 'location':'/static/video/BrokenBowPart1.avi' },
                '1': {'title':'Enterprise Broken Bow Part 2', 'location':'/static/video/BrokenBowPart2.avi' },
                }
        #
        # I think this needs dealing with in the browser.
        #
        port = cherrypy.config.get( 'server.socket_port', '8080' )
        ipadr = cherrypy.config.get( 'server.socket_host' )

        addresses = gethostbyaddr(gethostname())  # (hostname, aliaslist, ipaddrlist)
        ipaddrlist = addresses[2]
        self.__log.debug( 'server addresses %s' % (ipaddrlist) )
        if not ipadr:
            ipadr = ipaddrlist[0]

        self.serverBaseUrl = 'http://%s:%s' % ( ipadr, port )
        self.__log.debug( 'serverBaseUrl %s' % (self.serverBaseUrl) )

    @turbogears.expose(template="WebBrickGateway.templates.mediastatus", format="xml", content_type="text/xml")
    def status( self, medianame='name-required', status='item-required' ):
        """
        Return status of a media server
        """
        result = ClientProfiles.makeStandardResponse( cherrypy.request )

        self.__log.debug( 'MediaAccess.status %s, %s ' % (medianame, status) )
        result['stserr'] = None
        result['mediaName'] = medianame

        try :
            if ( status == 'vol' ):
                xmlStr = MediaSet.volume( self, medianame )
            elif ( status == 'playlist' ):
                 xmlStr = MediaSet.playlist( self, medianame )
            elif ( status == 'playlists' ):
                xmlStr = MediaSet.playlists( self, medianame )
            elif ( status == 'position' ):
                xmlStr = MediaSet.status( self, medianame )
            else:
                xmlStr = MediaSet.status( self, medianame )
            self.__log.debug( '%s:%s - xmlString %s' % (medianame, status, xmlStr) )
            xml = parseXmlString( xmlStr )

            if ( status == 'position' ):
                result['position'] = getNamedNodeText( xml, 'position' )
                result['duration'] = getNamedNodeText( xml, 'duration' )

            elif ( status == 'vol' ):
                result['vol'] = getNamedNodeText( xml, status )

            elif ( status == 'playlist' ):
                result['playlist'] = getElemXml( getNamedElem( xml, status ) )

            elif ( status == 'playlists' ):
                result['playlists'] = getElemXml( getNamedElem( xml, status ) )

            elif ( status == 'track' ):
                result['track'] = getNamedNodeText( xml, status )

            else:
                result[str(status)] = getNamedNodeText( xml, status )
        except Exception, ex :
            self.__log.exception( 'Error %s, %s ' % (medianame, status) )
            result['stserr'] = "unknown"
            
        return result

    # command does not return entity
    @turbogears.expose()
    def command(self, medianame='name-required', mediacmd="command-to-issue"):
        """
        Issue command to media server
        """
        self.__log.debug( 'status %s, %s ' % (medianame, mediacmd) )
        result = MediaSet.command( self, medianame, mediacmd )
        raise cherrypy.HTTPRedirect("/mediapanel?mediatitle=iTunes&amp;medianame=%s" % (medianame) )
        if not result:
            result = ""
        return result

    # command does not return entity
    @turbogears.expose()
    def setVolume(self, medianame='name-required', newVolume="level"):
        """
        Issue command to media server
        """
        self.__log.debug( 'setVolume %s, %s ' % (medianame, newVolume) )
        result = MediaSet.setVolume( self, medianame, newVolume )
        raise cherrypy.HTTPRedirect("/mediapanel?mediatitle=iTunes&amp;medianame=%s" % (medianame) )
        if not result:
            result = ""
        return result

    # command does not return entity
    @turbogears.expose()
    def setPosition(self, medianame='name-required', newPosition="newPosition"):
        """
        Issue command to media server
        """
        self.__log.debug( 'setPosition %s, %s ' % (medianame, newPosition) )
        result = MediaSet.setPosition( self, medianame, newPosition )
        raise cherrypy.HTTPRedirect("/mediapanel?mediatitle=iTunes&amp;medianame=%s" % (medianame) )
        if not result:
            result = ""
        return result

    @turbogears.expose()
    def embed2( self, trackId='0' ):
        """
        Return status of a media server
        """
        # '/static/video/BrokenBowPart1.avi'
        title = self.videoTracks[trackId]['title']
        relUrl = self.videoTracks[trackId]['location']
        result = mediaTemplate % ( title, self.getServer(), relUrl )
        self.__log.debug( 'embed %s' % (result,) )
        return result

    @turbogears.expose(template="WebBrickGateway.templates.StreamVideo", format="html", content_type="text/html")
    def embed( self, trackId='0' ):
        """
        Return status of a media server
        """
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "StreamVideo" )

        # '/static/video/BrokenBowPart1.avi'
        title = self.videoTracks[trackId]['title']
        relUrl = self.videoTracks[trackId]['location']

        result['mediaUrl'] = relUrl
        result['mediatitle'] = title,
        result['height'] = 400,
        result['width'] = 720,
        result['server'] = self.serverBaseUrl

        self.__log.debug( 'embed %s' % (result,) )
        return result

    @turbogears.expose(template="WebBrickGateway.templates.StreamVideoList", format="html", content_type="text/html")
    def showlist( self ):
        """
        Return status of a media server
        """
        result = ClientProfiles.makeStandardResponse( cherrypy.request, "StreamVideoList" )

#        loc = config.get('/video')['static_filter.dir']
        loc = cherrypy.config.get('static_filter.dir', '/var/www/video', False, '/video')

        if loc:
            mediaFiles = listdir( loc )
            mediaDict = {}
            if mediaFiles:
                idx = 0
                for fil in mediaFiles:
                    if isfile( "%s/%s" % (loc,fil) ):
                        mediaDict[str(idx)] = {'title':fil, 'location':'/video/%s' % quote(fil) }
                        idx = idx + 1

            self.videoTracks = mediaDict

        result['videoTracks'] = self.videoTracks
        result['height'] = 400
        result['width'] = 800
        result['server'] = self.serverBaseUrl

        self.__log.debug( 'list %s' % (result,) )
        return result

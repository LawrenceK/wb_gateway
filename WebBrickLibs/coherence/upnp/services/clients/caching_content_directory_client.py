import threading, logging, sys

from twisted.python import threadable

from content_directory_client import ContentDirectoryClient

# this extends the base client to cache browse results.
# needs to pick up container change events
# The cache reads what is required as required.

#
# WebBrick UPNP event interface
#
# give each server a unique id
SERVER_SEQ = 0
# maximum number of seconds to wait for data to be returned when browsing track contents
MAX_BROWSE_WAIT = 180

def validateTwistedCall():
    if not threadable.isInIOThread():
        raise Exception("We are not in the event loop")

class UPNP_Item_interface( object ):
    # Document methods.
    def title(self):
        return None

    def album(self):
        return None

    def artist(self):
        return None

    def local_id(self):
        # private local id that is small
        return None

    def set_local_id(self):
        # private local id that is small
        return None

    def id(self):
        return None

    def parent_id(self):
        return None

    def upnp_class(self):
        return None

    def resources(self):
        return None

class UPNP_Container_interface(UPNP_Item_interface):
    # Document methods.
    def enumItems(self):
        yield None

    def enumContainers(self):
        yield None

    def size(self):
        return 0

_log = logging.getLogger( UPNP_Item_interface.__module__ )

def device_name(client):
    # get device by root_id
    root_dev = client.device.get_root_device()
    _log.debug( "root_dev %s (%s)", root_dev, client )
    if root_dev:
        root_client = root_dev.client
        if hasattr(root_client,"get_zone_name"):
            return root_client.get_zone_name()
    return client.device.get_friendly_name()

def makeId(sid,cid,tid=None):
    if tid is None:
        return "%s:%s" % (sid,cid) 
    return "%s:%s:%s" % (sid,cid,tid) 

def splitId(id):
    # return tuple split at colon.
    return [int(id) for id in id.split(':')]

class UPNP_Item(UPNP_Item_interface):
    def __init__(self, client, item):
        self._client = client
        # copy to object later
        self._item = item

    def data(self,k):
        if k in self._item:
            return self._item[k]
        return ''

    def title(self):
        return self.data('title')

    def album(self):
        return self.data('album')

    def artist(self):
        result =  self.data('artist')
        if not result:
            result =  self.creator()
        return result

    def creator(self):
        return self.data('creator')

    def id(self):
        return self.data('id')

    def parent_id(self):
        return self.data('parent_id')

    def upnp_class(self):
        return self.data('upnp_class')

    def resources(self):
        return self.data('resources')

    def log_item(self ):
        _log.debug( "UPNP_Item %s", self )

#'album': 'Now 1984 (Disc 1)', 
#'title': 'Young At Heart', 
#'album_art_uri': '/getaa?u=x-file-cifs%3a%2f%2fSILENT%2fMusic%2fCompilations%2fNow%25201984%2520(Disc%25201)%2f1-09%2520Young%2520At%2520Heart.mp3&v=1', 
#'parent_id': 'S://SILENT/Music/Compilations/Now%201984%20(Disc%201)', 
#'upnp_class': 'object.item.audioItem.musicTrack', 
#'id': 'S://SILENT/Music/Compilations/Now%201984%20(Disc%201)/1-09%20Young%20At%20Heart.mp3', 
#'resources': {'x-file-cifs://SILENT/Music/Compilations/Now%201984%20(Disc%201)/1-09%20Young%20At%20Heart.mp3': 'x-file-cifs:*:audio/mpeg:*'}}

#'parent_id': 'S://SILENT/Music/Compilations', 
#'child_count': 'None', 
#'id': 'S://SILENT/Music/Compilations/The%20American%20Diner%20(Disc%202)', 
#'upnp_class': 'object.container', 
#'title': 'The American Diner (Disc 2)'

#'artist': 'Bonnie Tyler', 
#'title': 'Bonnie Tyler', 
#'parent_id': '1$12', 
#'child_count': '36', 
#'upnp_class': 'object.container.person.musicArtist', 
#'id': '1$12$1013212288'

#'album': 'Best Of The Best Gold', 
#'artist': 'Bonnie Tyler', 
#'title': 'Getting So Excited', 
#'parent_id': '1$12$1013212288', 
#'upnp_class': 'object.item.audioItem.musicTrack', 
#'id': '1$12$1013212288$2758044077', 
#'resources': {'http://192.168.0.1:9000/disk/music/DLNA-PNMP3-OP11-FLAGS01700000/O1$12$1013212288$2758044077.mp3': 'http-get:*:audio/mpeg:DLNA.ORG_PN=MP3;DLNA.ORG_OP=11;DLNA.ORG_FLAGS=01700000000000000000000000000000'}

    def __str__(self):
        return str(self._item)

class UPNP_Container(UPNP_Item,UPNP_Container_interface):
    """
    This is used to hold a local copy of some or all of a UPNP path.

    We need to be able to enumerate
    """
    def __init__(self, client, item ):
        super(UPNP_Container, self).__init__(client, item)
        #UPNP_Item.__init__(self, client, item)
        self._more_loaded = threading.Event()
        self._loaded_at_update_id = None
        self._last_seen_update_id = None
        self.reset_container()
        self._last_seen_update_id = 0   # allow load once, otherwise reload to often

    def reset_container(self):
        _log.debug("reset container %s", self.id() )
        self._load_complete = False
        # a list of items at this level
        self._items = []
        # a list of containers at this level
        self._containers = []
        self._loaded_at_update_id = self._last_seen_update_id

    def new_update_id(self, id):
        # we have had something tell us this is invalid so clear and reload when required
        self._last_seen_update_id = id
        _log.debug("new_update_id for %s of %s (%s)", self.id(), self._last_seen_update_id, self._loaded_at_update_id )

    def more_loaded(self, is_complete):
        # called by browse to indicate we have some more.
        _log.debug("more_loaded %s : len(self._items) %s", self.id(), len(self._items) )
        if is_complete:
            self.log_item()
            self._load_complete = True
        self._more_loaded.set()

    def doLoad_deferred_p(self):
        # returns defered
        return self._client.do_browse_container( self, 0 )

    def check_for_loaded(self):
        # returns defered if not yet loaded
        if self._loaded_at_update_id is None or self._loaded_at_update_id <> self._last_seen_update_id:
            _log.debug("check_for_loaded %s %s %s", self.id(), self._loaded_at_update_id, self._last_seen_update_id )
            self.reset_container()
            return self._client.do_browse_container( self, 0 )
        return None

    def startLoading(self):
        # do not wait in here as called to do preload of container
        if self._loaded_at_update_id is None or self._loaded_at_update_id <> self._last_seen_update_id:
            _log.debug("startLoading %s %s %s", self.id(), self._loaded_at_update_id, self._last_seen_update_id )
            self.reset_container()

            # we need to handle this on the reactor thread as it will
            # very likely make network calls to a UPNP device that MUST
            # be processed on the reactor thread.
            # defer import to here so we can install alternate reactors.
            from twisted.internet import reactor
            reactor.callFromThread( self.doLoad_deferred_p )

    def waitForMore(self):
        # TODO, this is being called from the twisted event loop if the
        # container has not been loaded already.
        # maximum block 1 second
        self._more_loaded.clear()
        if not self._load_complete:
            _log.debug("waitForMore %s %s (%s)", self.id(), self._loaded_at_update_id, self._last_seen_update_id )
            if not threadable.isInIOThread():
                self._more_loaded.wait(1)   # lets avoid a possible race condition
            else:
                # naughty, nauhgty
                raise Exception("waitForMore is in event loop")
        
    def enumItems(self):
        self.startLoading() # may no op. added as failsafe

        nextIdx = 0
        # keep going whilst we have more already to return
        # or we have yet to get load complete and may have more to return
        while nextIdx < len(self._items) or not self._load_complete:
            _log.debug("enumItems %s:%s (%s)", nextIdx, len(self._items), self._load_complete)
            if nextIdx >= len(self._items):
                self.waitForMore()
            while nextIdx < len(self._items):
                yield self._items[nextIdx]
                nextIdx = nextIdx + 1
        # drop out of outer while when we 

    def enumContainers(self):
        self.startLoading() # may no op. added as failsafe

        nextIdx = 0
        # keep going whilst we have more already to return
        # or we have yet to get load complete and may have more to return
        while nextIdx < len(self._containers) or not self._load_complete:
            _log.debug("enumContainers %s:%s (%s)", nextIdx, len(self._containers), self._load_complete)
            if nextIdx >= len(self._containers):
                self.waitForMore()
            while nextIdx < len(self._containers):
                yield self._containers[nextIdx]
                nextIdx = nextIdx + 1

    def size(self):
        return len(self._items)+len(self._containers)

    def log_item(self ):
        super(UPNP_Container, self).log_item()
        if self._containers:
            for ctr in self._containers:
                ctr.log_item()
        if self._items:
            for itm in self._items:
                itm.log_item()

view_container_id = 0

class UPNP_ViewContainer( UPNP_Container_interface ):
    # this is a massage of the UPNP tree.
    def __init__(self, title ):
        self._containers = list()
        global view_container_id
        view_container_id = view_container_id + 1
        self._item = {'title':title, 'id':"UPNP_ViewContainer_%s" % (view_container_id)}
        self._items = list()
        
    def add_container(self, ntry):
        self._containers.append(ntry)
        ntry._item['parent_id'] = self.id()
        
    def add_item(self, ntry):
        self._items.append(ntry)
        ntry._item['parent_id'] = self.id()
        
    def enumItems(self):
        for itm in self._items:
            yield itm

    def enumContainers(self):
        for ctr in self._containers:
            yield ctr

    def size(self):
        return len(self._items)+len(self._containers)

    def artist(self):
        return ''

    def creator(self):
        return ''

    def album(self):
        return ''

    def title(self):
        return self._item['title']

    def log_item(self ):
        _log.debug( "%s", self._item )
        for itm in self._containers:
            itm.log_item()

    def id(self):
        return self._item['id']

class UPNP_LineInContainer( UPNP_ViewContainer ):
    # this combines all the active line in inputs
    def __init__(self, svrs ):
        super(UPNP_LineInContainer,self).__init__('Line In Sources')
        self._servers = svrs    # a dictionary of current servers

    def enumItems(self):
        # check servers
        for srvk in self._servers:
            srv = self._servers[srvk]
            #if line in valid 
            # create container and yield
            ctr = srv.get_container_by_native_id('AI:')
            _log.debug( "%s %s", srv, ctr)
            for subctr in ctr.enumItems():
#                if subctr.title() == 'Line-In':
#                    # update title to include 
#                    subctr._item['title'] = 'Line In %s'%(srv.server_name())

                subctr._item['title'] = '%s : %s'%(subctr.title(),srv.server_name())
                yield subctr

#    def log_item(self ):
#        _log.debug( "%s", self._item )
#        for itm in self._servers:
#            pass

class UPNP_Directory(object):
    """
    This is used to hold a local copy of some or all of the UPNP directory tree.
    """
    def __init__(self):
        self._servers = {}

    def addClient(self, client, udn):
        self._servers[udn] = UPNP_Container(client, { 'id':0 })
        self._servers[udn].startLoading()   # start loading root.

    def getContainer(self, renderer_name):
        # do we create special context for this renderer
        # or use the global.
        pass


class CachingContentDirectoryClient(ContentDirectoryClient):

    def __init__(self, service):
        ContentDirectoryClient.__init__(self,service)
        #super( CachingContentDirectoryClient, self).__init__(service)

        global SERVER_SEQ
        SERVER_SEQ = SERVER_SEQ + 1
        self._server_id = SERVER_SEQ

        self._containers = {}   # keyed by container native id
        # create some default root containers

        service.subscribe_for_variable("ContainerUpdateIDs", 0, self.container_update_ids, True)
        service.subscribe_for_variable("SystemUpdateID", 0, self.system_update_id, True)

    def __str__(self):
        return "CachingContentDirectoryClient %s %s" % (self._server_id, self.service)

    def container_update_ids(self, variable):
        # we have received container update ids.
        self.debug("container_update_ids '%s' (%r)", variable.value, variable )
        ids = variable.value.split(',')
        # assume 1 for now.
        for idx in range(0, len(ids), 2):
            if self._containers.has_key(ids[idx]):
                self._containers[ids[idx]].new_update_id(ids[idx+1])

    def system_update_id(self, variable):
        # we have received a system update id.
        self.debug("system_update_id %s (%r)", variable.value, variable )

    def browse_fail(self, error, ctr):
        _log.error("browse_fail on %s, %s", ctr, error.getTraceback())
        # is anything waiting for this?
        ctr.more_loaded( True ) # with error

    def metadata_fail(self, error, ctr):
        _log.error("metadata_fail on %s, %s", ctr, error.getTraceback())

    def handle_result(self, result, ctr, starting_index ):
        try:
            returned_cnt = int(result['number_returned'])
            total_cnt = int(result['total_matches'])
            update_id = result['update_id']
            _log.debug( "handle_result client - %s %s of %s (%s)", self, returned_cnt, total_cnt, update_id )
            # result['items'] is a dictionary
            # result['items'] is now a list
#            for key,item in result['items'].iteritems():
#            keys = result['items'].keys()
#            keys.sort()
#            for key in keys:
            for item in result['items']:
#                _log.debug( "item %s", item )
#                item = result['items'][key]
#                key = item['id']
#                _log.debug( "%s %s", key,item )
                if item['upnp_class'].startswith( 'object.container' ):
                    newctr = UPNP_Container(self, item)
                    ctr._containers.append( newctr )
                    self._containers[newctr.id()] = newctr
                else:
                    ctr._items.append( UPNP_Item(self, item) )
            
            next_index = returned_cnt+int(starting_index)
            #_log.debug( "%s %s %s", returned_cnt, total_cnt, next_index )
            if next_index < total_cnt:
                # continue browse
                ctr.more_loaded( False )
                return self.do_browse_container(ctr, next_index )
            else:
                # is anything waiting for this?
                _log.debug( "Browse Complete" )
                ctr.more_loaded( True )
        except Exception, ex:
            _log.exception(ex)

    def do_browse_container(self, ctr, starting_index ):
        _log.info( "do_browse_container client - %s:%s:%s", self, ctr.id(), starting_index )
        defered = self.browse(ctr.id(),
                #browse_flag='BrowseDirectChildren',
                #filter='*', 
                #sort_criteria='',
                #requested_count=0,
                #process_result=True,
                #backward_compatibility=False,
                starting_index=starting_index
                )
        defered.addCallback( self.handle_result, ctr, starting_index=starting_index ).addErrback(self.browse_fail,ctr)
        return defered

    def handle_metadata(self, result, itm ):
        try:
            _log.info("handle_metadata %s", result )
            # update itm with metadata
            # update container store etc.
            itm._last_seen_update_id = result['UpdateID']
            #result['Result']    # is the didl lite bit
        except Exception, ex:
            _log.exception(ex)

    def do_browse_metadata(self, itm ):
        _log.info( "do_browse_metadata client - %s:%s", self, itm.id() )
        defered = self.browse(itm.id(),
                browse_flag='BrowseMetadata',
                #filter='*', 
                #sort_criteria='',
                #requested_count=0,
                process_result=False,
                #backward_compatibility=False,
                #starting_index=starting_index
                )
        defered.addCallback( self.handle_metadata, itm ).addErrback(self.metadata_fail,itm)
        return defered

    def get_container(self, id=0):
        if not self._containers.has_key(id):
            # create, then browse
            # need to get meta data?
            ctr = UPNP_Container(self, { 'id':id} )
            self._containers[id]= ctr
            self.do_browse_metadata(ctr)

        if self._containers.has_key(id):
            return self._containers[id]
        return None


class MultipleContentDirectoryClient():
    # Manage multiple content directory servers and provide a single view of the resources
    # This view may depend on which rendering client is your current context.

    def __init__(self):
        pass

class UPNP_Server( object ):
    def __init__(self, client):
        self._client = client
        self._server_id = client.content_directory._server_id
        self._containers = list()
        self._xref = dict()

        # do these now so get known internal ids.
        self._my_view = UPNP_ViewContainer("")  #then picks up server name.
        self.add_container(self._my_view)   # index 0

        self._level2 = UPNP_ViewContainer("Music Library")
        self._my_view.add_container(self._level2)
        self.add_container(self._level2)    # index 1

    def __str__(self):
        return "UPNP_Server %s %s" % (self._server_id, device_name(self._client) )

    def server_name( self ):
        return device_name(self._client)

    def get_container_by_native_id( self, id ):
        return self._client.content_directory.get_container(id)

    def load_complete(self):
        # initial load completed
        _log.debug( "UPNP_Server load_complete %s", self._server_id )

        #TODO move this to be part of the initial server load, from upnp.xml
        preload1 = [ 
                    { 'id':'Q:0', 'title':'Current Queue'},
                    { 'id':'S:', 'title':'Folders'},
                    #{ 'id':'Q:', 'title':'Sonos Playlists'},
                    { 'id':'SQ:', 'title':'Saved Playlists'},
                    { 'id':'R:', 'title':'Internet Radio'}
            ]

        #TODO move this to be part of the initial server load, from upnp.xml
        preload2 = [ { 'id':'A:ARTIST', 'title':'Artists'},
                    { 'id':'A:ALBUM', 'title':'Albums'},
                    { 'id':'A:COMPOSER', 'title':'Composers'},
                    { 'id':'A:GENRE', 'title':'Genres'},
                    { 'id':'A:TRACKS', 'title':'Tracks'}
            ]

        for ntry in preload1:
            ctr = self.get_container_by_native_id(ntry['id'])
            ctr._item['title'] = ntry['title']
            self.add_container(ctr)
            self._my_view.add_container(ctr)

        for ntry in preload2:
            ctr = self.get_container_by_native_id(ntry['id'])
            ctr._item['title'] = ntry['title']
            self.add_container(ctr)
            self._level2.add_container(ctr)

        # now start background browse of all containers.
        # update line input title
        #itm = self.get_container_by_native_id('AI:0')

        #from twisted.internet import reactor
        #reactor.callLater(0.1, self.background_browse, 0)

    def background_browse(self, idx):
        # browse all the containers
        while idx < len(self._containers):
            if isinstance(self._containers[idx], UPNP_Container) and not self._containers[idx]._loaded:
                break
            # keep going here until we find an unloaded container or fall of the end
            idx = idx + 1

        if idx < len(self._containers):
            # load this one
            _log.debug( "browse_container %i %s", idx, self._containers[idx] )
            df = self.do_browse_container(self._containers[idx])
            if df:
                df.addCallback(self.background_browse_done, idx)

    def background_browse_done(self, result, thisidx):
        # browse all the containers
        ctr = self._containers[thisidx]
        self.add_container(ctr)
        from twisted.internet import reactor
        reactor.callLater(0.1, self.background_browse, thisidx+1)

    def add_container(self,ctr):
        # allow multiple calls.
        if not self._xref.has_key(ctr.id()):
            _log.info( "add_container %s", ctr.id() )
            self._xref[ctr.id()] = len(self._containers)
            self._containers.append( ctr )

        # we do not want the load to occur, just the entries in the cross ref
        if ctr._containers:
            for subctr in ctr._containers:
                self.add_container( subctr )

    def add_container_to_my_view(self,ctr):
        self._my_view.add_container( ctr )
        self.add_container( ctr )

    def get_id( self ):
        if self._client and self._client.device:
            return self._client.device.get_id()
        return None

    def get_default_container_id( self ):
        # in the case of Sonos the current Queue
        if self._xref.has_key("Q:0"):
            return makeId(self._server_id, self._xref["Q:0"])
        return None

    def get_top_level_container_id( self ):
        # Our massaged view.
        return makeId(self._server_id, 0)

    def get_container_p( self, ids ):
        if ids and len(ids) >= 2 and ids[1] < len(self._containers):
            ctr = self._containers[ids[1]]
            if isinstance( ctr, UPNP_Container_interface ):
                # already a container
                return ctr
            # ctr is actually an id from the server
            return self._client.content_directory.get_container(ctr)
        else:
            #return self._containers[0]  # default root container?
            pass
        return None # no such container

    def get_container( self, id_str ):
        if id_str:
            ids = splitId(id_str)
            return self.get_container_p(ids)
        return None # no such container

    def get_item( self, id_str ):
        ids = splitId(id_str)
        ctr = self.get_container_p(ids)
        if ctr and len(ids) >= 3:
            tid = 0
            for itm in ctr.enumItems():
                if tid == ids[2]:
                    return itm
                tid = tid + 1
        return ctr

    def enum_container( self, ctr, skipCount=0, limit=sys.maxint ):
        # yield dictionaries of attributes
        # Add support to skip the first n entries
        # Bit crude for now.
        if ctr is None:
            ctr = self.get_container_by_native_id(0) # go to root
        ctr_id = ctr.id()
        _log.debug( "enum_container %s : %s", ctr_id, ctr )

        idx = 0

        # items first, they tend to be bigger lists
        # and otherwise the ctr.enumContainers() blocks until the list is loaded.
        #
        # TODO combine the enumertate into a single call and have a flag
        # on the returned item to identify containers/items.
        tid = 0

        # cannot play queue entries. cannot queue radio stations
        # TODO use regular expression to define these and load from configuration.

        for itm in ctr.enumItems():
            id = itm.id()
            _log.debug( "Item %s", id )
            if itm:
                idx = idx + 1
                if skipCount < idx:

                    playFlag = not ( id.startswith("Q:") or ( id.startswith("R:") and (id.find('/') < 0) ) )
                    qFlag = playFlag and not id.startswith("AI:") and not id.startswith("R:")

                    res = dict(itm._item)
                    res['id'] = makeId(self._server_id, self._xref[ctr_id], tid)
                    res['isContainer'] = False
                    res['canQueue'] = qFlag
                    res['canPlay'] = playFlag
                    _log.debug( "a item result %s", res )
                    yield res
                tid=tid+1

        for subctr in ctr.enumContainers():
            idx = idx + 1
            if skipCount < idx:
                id = subctr.id()
                self.add_container( subctr )
                res = dict(subctr._item)
                res['id'] = makeId(self._server_id, self._xref[id])
                res['isContainer'] = True
                # Cannot queue entries in the queue or radio station containers
                res['canQueue'] = not id.startswith("Q:") and not id.startswith("R:")
                if id.startswith("UPNP_ViewContainer_") \
                        or id in ['A:ARTIST', 'A:ALBUM', 'A:COMPOSER', 'A:GENRE', 'A:TRACKS',
                                        'Q:0', 'S:','Q:','SQ:','R:' ]:
                    res['canQueue'] = False

                res['canPlay'] = res['canQueue']
                _log.debug( "a container result %s", res )

                yield res
            # else we are skipping this one
        # done.

    def do_browse_container(self, ctr):
        return self._client.content_directory.do_browse_container(ctr,0)

    def do_browse_metadata(self, ctr):
        return self._client.content_directory.do_browse_metadata(ctr)

    def get_breadcrumb_trail(self, ctr):
        bcrumb = list()
        # skip self in breadcrumb trail?
        _log.debug( "get_breadcrumb_trail start %s", ctr )
        while ctr and ctr.parent_id() and self._xref.has_key( ctr.parent_id() ):
            ctr = self._containers[self._xref[ctr.parent_id()]]
            _log.debug( "get_breadcrumb_trail %s", ctr )
            bcrumb.append( (ctr.title(), makeId(self._server_id, self._xref[ctr.id()])) )

        bcrumb.reverse()
        return bcrumb

class UPNP_MediaServerList():
    """
    This is used to hold a local copy of some or all of the UPNP directory tree.
    """
    def __init__(self):
        self._servers = {}
        self._line_in_container = UPNP_LineInContainer(self._servers)

    def initial_directory_browse(self, server):
        # here as there are cross over details, we want to create a single view including stuff from 
        # multiple media servers

        def line_inputs_loaded( result, ctr ):
            # update line input title
            # now create my view
            try:
                _log.debug("initial_directory_browse line_inputs_loaded %s", server)

#                ctr = server.get_container_by_native_id('AI:0')
#                if not ctr.title():
#                    # give it a title for now.
#                    ctr._item['title'] = 'Line In %s'%(device_name(client))
#                self._line_in_container.add_item( ctr )

                server.load_complete()

                #li = { 'id':'AI:0', 'title':'Line In %s'%(device_name(client))}
                #_log.debug( "Line In %s", li )
                #lic = UPNP_Item(client, li)

                server.add_container_to_my_view(self._line_in_container)
                # Done.
                _log.debug("initial_directory_browse complete %s", server)
            except Exception, ex:
                _log.exception(ex)

        def attributes_loaded( result, ctr ):
            _log.debug("initial_directory_browse attributes_loaded %s", server)
            if not server._client.content_directory._containers.has_key('AI:'):
                # Should not happen
                _log.info("initial_directory_browse root_children_loaded no AI: container %s", server)
                pass
            subctr = server._client.content_directory.get_container('AI:')
            df = server.do_browse_container(subctr)
            df.addCallback( line_inputs_loaded, ctr )

        def root_children_loaded( result, ctr ):
            _log.debug("initial_directory_browse root_children_loaded %s", server)
            # locate A: container
            # load
            for k in server._client.content_directory._containers:
                _log.debug("initial_directory_browse current entries %s", k)
                
            if not server._client.content_directory._containers.has_key('A:'):
                # Should not happen
                _log.info("initial_directory_browse root_children_loaded no A: container %s", server)

            subctr = server._client.content_directory.get_container('A:')
            df = server.do_browse_container(subctr)
            df.addCallback( attributes_loaded, ctr )

        def root_metadata_loaded( result, ctr ):
            # success ?
            _log.debug("initial_directory_browse root_metadata_loaded %s", server)
            df = server.do_browse_container(ctr)
            df.addCallback( root_children_loaded, ctr )

        def load_root():
            # browse 0.
            ctr = UPNP_Container(self, { 'id':0 })
            df = server.do_browse_metadata(ctr)
            df.addCallback( root_metadata_loaded, ctr )

        # and load
        _log.debug("initial_directory_browse %s", server)
        load_root()

    def add_server(self, client, udn):
        _log.debug("add_server %s %s", udn, client)

        if isinstance(client.content_directory, CachingContentDirectoryClient):
            # for now the caching client is tied to Sonos
            for k in self._servers:
                if self._servers[k].get_id() == udn:
                    _log.debug( "Update server already exists id %s", udn )
                    return

            srv = UPNP_Server(client)
            self._servers[srv._server_id] = srv
            self.initial_directory_browse(srv)

    def remove_server(self, client, udn ):
        for k in self._servers:
            if self._servers[k].get_id() == udn:
                _log.debug( "removed server id %s", udn )
                del self._servers[k]
                break

    def get_server(self, id_str):
        ids = splitId(id_str)
        sid = ids[0]
        if self._servers.has_key(sid):
            return self._servers[sid]
        return None

    def get_servers(self):
        for k in self._servers:
            sname = self._servers[k].server_name()
            yield { 'id':k, 'title':sname }

    def default_server_for_renderer(self, rname):
        for k in self._servers:
            sname = self._servers[k].server_name()
            if rname == sname:
                return self._servers[k]
        return None

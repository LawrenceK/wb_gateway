# $Id: WbUdpCommands.py 2612 2008-08-11 20:08:49Z graham.klyne $

import socket, logging, string

# UDP port the siteplayer receives on.
wbPort = 26482

def sendUdpCommand(ipAddr, value):
    """

    This sends commands to webbrick using UDP. the advantage of this is that commands
    can be broadcast and reach webbricks where more than one have come up on the same IP address.

    parameters are the ipAddr to send to to
    value the text string command, see webbrick documentation.

    see siteplayer documentation for delivering UDP packets to siteplayer objects, specifically
    the COM port that is connected to webbrick PIC chip.

    """
    cmd = value
    if ( value[0] != ':' ):
        cmd = ":" + value
    if ( value[-1] != ':' ):
        cmd = cmd + ":"

    frameLen = len(cmd)


    FrameData = chr(frameLen) + chr(255-frameLen) + '\x19\xFF' + cmd + '\x00\x00'
    wbsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    wbsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    idx = ipAddr.find(":")
    port = wbPort
    if idx >= 0:
        # has port component
        port = int(ipAddr[idx+1:])
        ipAddr = ipAddr[:idx]
    logging.debug( 'ipAddr %s wbPort %s frameLen %i data: %s' % (ipAddr, port, frameLen, cmd ) )
    wbsocket.sendto(FrameData, (ipAddr, port))
    return 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print "send %s to %s " % ( sys.argv[2], sys.argv[1])
        sendUdpCommand(sys.argv[1], sys.argv[2])
    
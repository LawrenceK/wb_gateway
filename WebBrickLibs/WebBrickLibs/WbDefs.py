# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

# $Id: WbDefs.py 2612 2008-08-11 20:08:49Z graham.klyne $
#
# WebBrickSystems.com
#
"""
Class to hold constants for webbricks.
"""

def checkRange(idx,lo,hi):
    """
    idx must be greater or equal to lo and less than hi
    """
    if (idx<lo) or (idx>=hi):
        raise ValueError, "Index %i given, must be in range (%i,%i)" % (idx, lo, hi-1)

# PIC sets this address
DEFAULT_IP_ADR = "10.100.100.100"
# Siteplayer has this address in its image
DEFAULT_SP_ADR = "10.100.100.251"

# Action types.
"""
These are constants for the possible actions that a webbrick trigger can perform.
"""
AT_NONE = 0
AT_OFF = 1
AT_ON = 2
AT_MOMENTARY = 3
AT_TOGGLE = 4
AT_DWELL = 5
AT_DWELLALWAYS = 5
AT_DWELLCAN = 6
AT_NEXT = 7
AT_PREV = 8
AT_SETLOW = 9
AT_SETHIGH = 10
AT_ADJUSTLOW = 11
AT_ADJUSTHIGH = 12
AT_SENDIR = 13
AT_STEPUP = 14
AT_STEPDOWN = 15
AT_SETDMX = 16
AT_COUNT = 17
AT_DWELLON = 18
AT_DWELLOFF = 19
AT_SPARE = 14
AT_SPARE65 = 20

# Additional values for internal use only
AT_NEXTSCENE = 0x80+AT_NEXT
AT_PREVSCENE = 0x80+AT_PREV

ActionStrs = [ "None"
            , "Off", "On", "Momentary", "Toggle"
            , "Dwell", "Dwell-Can"
            , "Next", "Prev"
            , "SetLowThreshold", "SetHighThreshold"
            , "AdjustLowThreshold", "AdjustHighThreshold"
            , "SendIR"
            , "14", "15"
            ]

ActionStrs65 =  [ "None"
            , "Off", "On", "Momentary", "Toggle"            # 1-4
            , "Dwell-alw", "Dwell-can"                      # 5-6
            , "Next", "Prev"                                # 7-8
            , "SetLowThreshold", "SetHighThreshold"         # 9-10
            , "AdjustLowThreshold", "AdjustHighThreshold"   # 11-12
            , "SendIR"                                      # 13
            , "Step-up", "Step-down"                        # 14-15
            , "SetDMX"                                      # 16
            , "Count"                                       # 17
            , "Dwell-on", "Dwell-off"                       # 18-19
            , "20", "21", "22", "23"
            , "24", "25", "26", "27"
            , "28", "29", "30", "31"
            ]

# UDP types.
"""
These are constants for the possible UDP packet types a webbrick trigger can send.
Along with a set of strings for display.
"""
UDPT_NONE    = 0
UDPT_GENERAL = 1
UDPT_ALARM   = 2
UDPT_REMOTE  = 3
UDPRemStrs   = [ "None", "General", "Remote", "Alarm" ]

UDPT_65_NONE = 0
UDPT_65_SEND = 1
UDPRemStrs65 = [ "None", "General" ]

# Event action target types.
"""
These are constants for the possible trigger target type.
Along with a set of strings for display.
"""
TT_DIGITAL     = 0
TT_SCENE       = 1
TT_ANALOG      = 2
TT_ANALOGUE    = 2
TT_TEMPERATURE = 3
TTCommandTags   = ["D", "S", "A", "T"]
ChannelTypeStrs = ["Digital", "Scene", "Analogue", "Temperature" ]

# Set points
"""
These are constants for the possible set point values
"""
SP_0 = 0
SP_1 = 1
SP_2 = 2
SP_3 = 3
SP_4 = 4
SP_5 = 5
SP_6 = 6
SP_7 = 7
SP_8 = 8
SP_9 = 9
SP_10 = 10
SP_11 = 11
SP_12 = 12
SP_13 = 13
SP_14 = 14
SP_15 = 15

# Dwells
"""
These are constants for the possible dwell identifiers
"""
DW_0 = 0
DW_1 = 1
DW_2 = 2
DW_3 = 3
DW_4 = 4
DW_5 = 5
DW_6 = 6
DW_7 = 7

"""
These are constants that define the number of each entity in a webbrick.
"""
ROTARYCOUNT = 2
DWELLCOUNT = 4
SPCOUNT = 8
DICOUNT = 12
MONCOUNT = 4
AICOUNT = 4
DOCOUNT = 8
MIMICCOUNT = 8
AOCOUNT = 4
TEMPCOUNT = 5
SCHEDCOUNT = 16
SCENECOUNT = 12


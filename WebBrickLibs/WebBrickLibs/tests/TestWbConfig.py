# $Id: TestWbConfig.py 3182 2009-06-01 16:22:23Z philipp.schuster $
"""
WebBrick test configuration settings
"""

class TestWbConfig:

    WbFactoryPw = "installer"
    #WbFactoryPw = "password"

    WbNoAddress = "10.199.100.100"    # no webbrick here
    WbAddress = "10.100.100.100"    # default
    WbNetMask = "10.100.100.100/8"  # default
    #WbAddress = "193.123.216.121"   # GK network
    #WbNetMask = "193.123.216.64/26" # GK network

    # Expected digital inputs
    ExpectedDigIn = [True]*12
    
    # LPK V7 hardware have pulldowns on the monitor inputs.
    ExpectedDigInV7Hw = [True]*8+[False]*4
    
    ExpectedTemp = ( 21.3, 21.7,0.0, 0.0, -1000.0 )
    # WbVersion   = "6.1.967"
    #WbVersion   = "6.2.1391" # GK network
    #WbVersion   = "6.5.2093"
    WbVersions   = ["6.1.967", "6.2.1391", "6.4.1898", "6.5.2093", "6.6.2120"]

    #TODO: initialize default logging for unit tests?

# End. $Id: TestWbConfig.py 3182 2009-06-01 16:22:23Z philipp.schuster $

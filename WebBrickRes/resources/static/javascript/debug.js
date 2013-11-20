
// Hack as default is no limit and default firebug off
MochiKit.Logging.logger.useNativeConsole = true;
MochiKit.Logging.logger.maxSize = 2000;
initPoller( 120.0 );

REM clean all files. include build eggs
DEL /S /Q .\WebBrickConfig\dist\*
DEL /S /Q .\WebBrickConfig\WebBrickConfig.egg-info\*
DEL /S /Q .\WebBrickDoc\dist\*
DEL /S /Q .\WebBrickDoc\WebBrickDoc.egg-info\*
DEL /S /Q .\WebBrickGateway\dist\*
DEL /S /Q .\WebBrickGateway\WebBrickGateway.egg-info\*
DEL /S /Q .\WebBrickLibs\dist\*
DEL /S /Q .\WebBrickLibs\WebBrickLibs.egg-info\*
DEL /S /Q .\WebBrickRes\dist\*
DEL /S /Q .\WebBrickRes\WebBrickRes.egg-info\*
CALL cleanpostbuild.bat


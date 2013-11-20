REM clean files generated as part of build process, leaves new eggs intact
DEL /S /Q .\WebBrickConfig\build\*
DEL /S /Q .\WebBrickDoc\build\*
DEL /S /Q .\WebBrickDoc\*.html
REM carefull there are a few tex files that are not autio generated. Mainly under gateway
DEL /S /Q .\WebBrickDoc\eventinterfaces\*.tex
DEL /S /Q .\WebBrickDoc\events\*.tex
DEL /S /Q .\WebBrickDoc\samples\*.tex
DEL /S /Q .\WebBrickDoc\webbrick\*.pdf

DEL /S /Q .\WebBrickGateway\build\*
DEL /S /Q .\WebBrickLibs\build\*
DEL /S /Q .\WebBrickRes\build\*

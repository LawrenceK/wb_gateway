SET TARGET=%1%

cd WebBrickLibs
DEL dist\*.egg
DEL /S /Q /F build\*.*
CALL MakeEgg.bat
copy /Y dist\*.egg ..\%TARGET%\*
cd ..

cd WebBrickRes
DEL dist\*.egg
DEL /S /Q /F build\*.*
CALL MakeEgg.bat
copy /Y dist\*.egg ..\%TARGET%\*
cd ..

cd WebBrickConfig
DEL dist\*.egg
DEL /S /Q /F build\*.*
CALL MakeEgg.bat
copy /Y dist\*.egg ..\%TARGET%\*
cd ..

cd WebBrickGateway
DEL dist\*.egg
DEL /S /Q /F build\*.*
CALL MakeEgg.bat
copy /Y dist\*.egg ..\%TARGET%\*
cd ..

cd WebBrickDoc
DEL dist\*.egg
DEL /S /Q /F build\*.*
CALL MakeEgg.bat
copy /Y dist\*.egg ..\%TARGET%\*
cd ..

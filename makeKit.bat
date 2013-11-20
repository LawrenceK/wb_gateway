CALL env.bat
SET TARGET=.\..\..\GatewayCd
mkdir %TARGET%
DEL %TARGET%\*.egg
DEL %TARGET%\setup.exe

CALL clean

REM get latest build number (svn log number)
svn info | grep Revision > version.txt
sed -i -e 's/Revision: /# Revision: /' version.txt

COPY /Y readme.txt %TARGET%\
COPY /Y install.txt %TARGET%\
COPY /Y license.txt %TARGET%\
COPY /Y version.txt %TARGET%\
COPY /Y WebBrickGateway\resources\webbrick.* %TARGET%\linux

COPY /Y setup.sh %TARGET%\setup
TYPE version.txt >> %TARGET%\setup

COPY /Y setup.debian %TARGET%\setup.debian
TYPE version.txt >> %TARGET%\setup.debian

REM build and copy eggs
CALL build.bat %TARGET%

CD Install\Win32
ISCC.exe Gateway.iss
REM C:\WIN32APP\InnoSetup5\Compil32.exeISCC Gateway.iss
CD ..\..

REM Unzip WebBrickDoc egg into Docs
unzip -o %TARGET%\WebBrickDoc-2.0-py2.5.egg -d %TARGET%\docs

COPY /Y .\Install\Win32\Output\setup.exe %TARGET%

SET TARGET=

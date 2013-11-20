svn info | grep Revision > WebBrickDoc\version.py
sed -i -e 's/Revision: /__VERSION__ = /' WebBrickDoc\version.py

mkdir build
REM CD latex
REM CALL Build.bat
REM CD ..
lore.py --config template=template.tpl --inputext=.lore
lore.py --config template=template.tpl --inputext=.lore --output=latex --config section


CD eventinterfaces
CD ..

CD Gateway
CD User
REM CALL Build.bat
texify --language=LaTeX --pdf --clean User.tex
CD ..
CD Reference
REM CALL Build.bat
texify --language=LaTeX --pdf --clean Reference.tex
CD ..
CD Appliance
REM CALL Build.bat
texify --language=LaTeX --pdf --clean Appliance.tex
CD ..
CD touchscreen
REM CALL Build.bat
texify --language=LaTeX --pdf --clean TouchScreen.tex
CD ..
CD DataSheet
REM CALL Build.bat
texify --language=LaTeX --pdf --clean DataSheet.tex
CD ..
CD ..

REM fixup image references
COPY /Y ..\..\..\WebBrick\Trunk\Documentation\*.pdf .\WebBrick\*

python setup.py bdist_egg --exclude-source-files 
REM --executable /usr/bin/python


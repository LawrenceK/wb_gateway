svn info | grep Revision > WebBrickGateway\version.py
sed -i -e 's/Revision: /__VERSION__ = /' WebBrickGateway\version.py

REM Generate the framework pages and xml for samples2.

REM NOT IN USE AT THE MEOMENT
REM CD .\resources\samples2\template_files
REM CALL AllZones
REM CD ..\..\..

ATTRIB /S -R *
python setup.py bdist_egg --exclude-source-files 
REM --executable /usr/bin/python


svn info | grep Revision > WebBrickRes\version.py
sed -i -e 's/Revision: /__VERSION__ = /' WebBrickRes\version.py

python setup.py bdist_egg --exclude-source-files 
REM --executable /usr/bin/python


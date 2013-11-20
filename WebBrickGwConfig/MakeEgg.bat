svn info | grep Revision > WebBrickGwConfig\version.py
sed -i -e 's/Revision: /__VERSION__ = /' WebBrickGwConfig\version.py

python setup.py bdist_egg --exclude-source-files


svn info | grep Revision > WebBrickLibs\version.py
sed -i -e 's/Revision: /__VERSION__ = /' WebBrickLibs\version.py

python setup.py bdist_egg --exclude-source-files

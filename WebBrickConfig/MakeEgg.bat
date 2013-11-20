svn info | grep Revision > WebBrickConfig\version.py
sed -i -e 's/Revision: /__VERSION__ = /' WebBrickConfig\version.py

python setup.py bdist_egg --exclude-source-files


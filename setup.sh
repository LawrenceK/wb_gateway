#!/bin/bash
#
# THIS FILE MUST BE SAVED IN UNIX FORMAT i.e. LF end of line.
#
# Update to do install using python eggs.
installDir="/opt/webbrick"
logDir="/var/log/webbrick"

if [ -f /etc/init.d/webbrick ]
then
	# already installed
	/etc/init.d/webbrick stop
	killall python
fi

# ensure default install exists.
if [ ! -e $installDir ]
then
	mkdir $installDir
fi
if [ ! -e $logDir ]
then
	mkdir $logDir
fi

# install Turbogears
# if this fails it may be due to lack of GCC or python-dev
cd Turbogears
python ./tgsetup.py
cd ..

# install the webbrick python eggs
easy_install WebBrickLibs-2.0-py2.5.egg
easy_install WebBrickRes-2.0-py2.5.egg
easy_install WebBrickConfig-2.0-py2.5.egg
easy_install WebBrickGateway-2.0-py2.5.egg
easy_install WebBrickDoc-2.0-py2.5.egg


# copy over boot start script
if [ ! -f /etc/init.d/webbrick ]
then
cp webbrick.init /etc/init.d/webbrick
fi
rc-update add webbrick default

# still having issues with an SSL connection.
#openssl req -new -x509 -nodes -out server.crt -keyout server.key

# update apache configuration.
if [ ! -f /etc/apache2/vhosts.d/webbrick.conf ]
then
    # this config needs updating to point to the python install location.
    cp apache.webbrick.conf /etc/apache2/vhosts.d/webbrick.conf
    /etc/init.d/apache2 stop
    /etc/init.d/apache2 start
fi
# /etc/init.d/apache2 restart should work but not confident.

# start webbrick gateway
/etc/init.d/webbrick start
#
echo Install completed
echo gateway should of started
echo documentation available on line.


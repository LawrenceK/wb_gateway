# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

from setuptools import setup, find_packages
from turbogears.finddata import find_package_data

import os
#execfile(os.path.join("WebBrickLibs", "release.py"))

setup(
    name="WebBrickLibs",
    version="2.0",
    
    # uncomment the following lines if you fill them out in release.py
    description="Support libraries for WebBrick Gateway software",
    author="Graham Klyne, Lawrence Klyne",
    author_email="info@WebBrickSystems.com",
    url="http://www.WebBrickSystems.com/",
    #download_url=download_url,
    #license=license,
    
    install_requires = [
    ],
    scripts = [ ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    package_data = find_package_data(where='WebBrickLibs',
                                     package='WebBrickLibs'),
#    entry_points = {
#        'console_scripts': [
#          'taskrunner = WebBrickLibs.TaskRunner:main',
#          'upnp_tester = coherence.upnp_tester:main'
#        ],
#    },

    entry_points="""
        [coherence.plugins.backend.media_server]
        ElisaMediaStore = coherence.backends.elisa_storage:ElisaMediaStore
        FlickrStore = coherence.backends.flickr_storage:FlickrStore
        AxisCamStore = coherence.backends.axiscam_storage:AxisCamStore
        BuzztardStore = coherence.backends.buzztard_control:BuzztardStore
        IRadioStore = coherence.backends.iradio_storage:IRadioStore
        LastFMStore = coherence.backends.lastfm_storage:LastFMStore
        AmpacheStore = coherence.backends.ampache_storage:AmpacheStore

        [coherence.plugins.backend.media_renderer]
        ElisaPlayer = coherence.backends.elisa_renderer:ElisaPlayer
        BuzztardPlayer = coherence.backends.buzztard_control:BuzztardPlayer

        [coherence.plugins.backend.binary_light]
        SimpleLight = coherence.backends.light:SimpleLight

        [coherence.plugins.backend.dimmable_light]
        BetterLight = coherence.backends.light:BetterLight

    """,
    
    keywords = [
        # Use keywords if you'll be adding your package to the
        # Python Cheeseshop
        
        # if this has widgets, uncomment the next line
        # 'turbogears.widgets',
        
        # if this has a tg-admin command, uncomment the next line
        # 'turbogears.command',
        
        # if this has identity providers, uncomment the next line
        # 'turbogears.identity.provider',
    
        # If this is a template plugin, uncomment the next line
        # 'python.templating.engines',
        
        # If this is a full application, uncomment the next line
        # 'turbogears.app',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite = 'WebBrickLibs.tests.TestAll.getTestWebBrickConfigSuite',
    )
    
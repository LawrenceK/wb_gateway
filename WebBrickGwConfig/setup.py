# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

from setuptools import setup, find_packages
from turbogears.finddata import find_package_data

import os
#execfile(os.path.join("WebBrickGwConfig", "release.py"))

wb_packages = find_packages() + ["resources"]

wb_package_data = find_package_data(where='WebBrickGwConfig', 
                                    package='WebBrickGwConfig')
                                    
wb_resource_data = find_package_data(where='resources', 
                                     package='resources', 
                                     exclude=["*.zip"], 
                                     exclude_directories=['.*', "Development"])
                                     
wb_package_data.update(wb_resource_data)

setup(
    name="WebBrickGwConfig",
    version="2.0",
    
    # uncomment the following lines if you fill them out in release.py
    description="Configuration Library for WebBrick Gateway software",
    author="Philipp Schuster",
    author_email="philipp.schuster@webbricksystes.com",
    url="http://www.WebBrickSystems.com/",
    #download_url=download_url,
    #license=license,
    
    install_requires = [
    ],
    scripts = [ ],
    zip_safe=False,
    include_package_data=True,
    packages=wb_packages,
    package_data = wb_package_data,

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
    test_suite = 'WebBrickGwConfig.tests.TestAll.getTestWebBrickConfigSuite',
    )
packages=find_packages()
print "Packages %s" % packages
package_data = find_package_data(where='WebBrickGwConfig',
                                     package='WebBrickGwConfig')
print "Package_data %s" % package_data
    

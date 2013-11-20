# Copyright L.P.Klyne 2013 
# Licenced under 3 clause BSD licence 

from setuptools import setup, find_packages
from turbogears.finddata import find_package_data, standard_exclude

import os
#execfile(os.path.join("WebBrickGateway", "release.py"))

subpackages = [
        "resources", 

        "resources/eventdespatch",
            "resources/eventdespatch/System",
            "resources/eventdespatch/Generic",

        "resources/misc",
            "resources/misc/eventdespatch",
                "resources/misc/eventdespatch/optional_files",
                "resources/misc/eventdespatch/Samples",
                "resources/misc/eventdespatch/template_files",
            "resources/misc/templates",
                "resources/misc/templates/ipod",
                "resources/misc/templates/voipphone",

        "resources/site",
            "resources/site/wbconf",
                "resources/site/wbconf/samples",
            "resources/site/wbproxy",
            "resources/site/eventdespatch",
            "resources/site/templates",
            "resources/site/templates/round",
                "resources/site/templates/round/optional_files",
                "resources/site/templates/round/template_files",
            "resources/site/templates/square",
            "resources/site/templates/tabbed",
        
        "resources/site_builders",
            "resources/site_builders/round",
                "resources/site_builders/round/eventdespatch",
                "resources/site_builders/round/template_files",
                "resources/site_builders/round/templates",
            "resources/site_builders/tabbed",
                "resources/site_builders/tabbed/eventdespatch",
                "resources/site_builders/tabbed/site_generator",
                    "resources/site_builders/tabbed/site_generator/to_copy",
                "resources/site_builders/tabbed/templates",
                 
        ]

my_exclude = ('*.py', '*.pyc', '*~', '.*', '*.bak', '*.xhtml', '*.lore', '*.tex', '*.zip' )
my_exclude_directories=['.*', "Thirtover1", "spike"]

wb_packages = find_packages() + subpackages

wb_package_data = find_package_data(where='WebBrickGateway', package='WebBrickGateway', exclude=my_exclude, exclude_directories=my_exclude_directories)
                                     
for sp in subpackages:
    wb_resource_data = find_package_data(where=sp, package=sp, exclude=my_exclude, exclude_directories=my_exclude_directories )
    wb_package_data.update(wb_resource_data)

#print "wb_packages %s\n" % (wb_packages)
#for k in wb_package_data:
#    print "wb_package_data %s" % (k)
#    for n in wb_package_data[k]:
#        print "\t%s" % (n)

setup(
    name="WebBrickGateway",
    version="2.0",
    
    # uncomment the following lines if you fill them out in release.py
    description="Webbrick Gateway",
    author="Lawrence Klyne",
    #author_email=email,
    url="http://www.h2m8.com",
    #download_url=download_url,
    #license=license,
    
    install_requires = [
        "TurboGears >= 1.0.1",
        "WebBrickConfig >= 2.0",
        "WebBrickRes >= 2.0",
        "WebBrickLibs >= 2.0",
    ],
    entry_points = {
        'console_scripts': [
          'webbrick_util = WebBrickGateway.webbrick_util:main',
#          'webbrick_util = WebBrickGateway.webbrick_util:main',
        ],
    },
    scripts = ["start-WebBrickGateway.py", "WebBrickGateway/webbrick_util.py" ],
    # data_files = [ ('', ['prod.cfg']) ],
    zip_safe=False,
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
        'Framework :: TurboGears',
        # if this is an application that you'll distribute through
        # the Cheeseshop, uncomment the next line
        # 'Framework :: TurboGears :: Applications',
        
        # if this is a package that includes widgets that you'll distribute
        # through the Cheeseshop, uncomment the next line
        # 'Framework :: TurboGears :: Widgets',
    ],
    # test_suite = 'nose.collector',
    )
    

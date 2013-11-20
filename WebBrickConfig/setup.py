from setuptools import setup, find_packages
from turbogears.finddata import find_package_data

import os
#execfile(os.path.join("WebBrickConfig", "release.py"))

wb_packages = find_packages() + ["resources"]

## + ["resources/wbconf/"+d for d in ["Example-1","Example-2","Example-3","Thirtover"] ]

wb_package_data = find_package_data(where='WebBrickConfig', package='WebBrickConfig')
wb_resource_data = find_package_data(where='resources', package='resources', 
                                     exclude=["*.zip"], 
                                     exclude_directories=['.*', "Thirtover1"])
wb_package_data.update(wb_resource_data)


# wb_package_data.update({'log': []})
# wb_package_data.update({'': ["prod.cfg"]})

# ["wbconf/"+d+"/*.xml" for d in ["Example-1","Example-2","Example-3","Thirtover"] ]

setup(
    name="WebBrickConfig",
    version="2.0",
    
    description="WebBrick Configuration Server",
    author="Graham Klyne",
    author_email="gk-config@webbricksystems.com",
    url="http://www.webbricksystems.com/",
    #download_url=download_url,
    #license=license,
    install_requires = [
        "TurboGears >= 1.0.1",
        "WebBrickLibs >= 2.0",
    ],
    scripts = ["start-WebBrickConfig.py"],
    data_files = [ ('', ['prod.cfg']) ],
    zip_safe=False,
    #include_package_data=True,
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
    test_suite = 'WebBrickConfig.tests.TestWebBrickConfig.getTestWebBrickConfigSuite',
    # test_suite = 'nose.collector',
    )
    

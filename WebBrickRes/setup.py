from setuptools import setup, find_packages
from turbogears.finddata import find_package_data

wb_packages = find_packages() + ["resources"]
wb_package_data = find_package_data(where='WebBrickRes', package='WebBrickRes')
wb_resource_data = find_package_data(where='resources', package='resources', 
                                     exclude=["*.zip", "MochiKit.uncompressed.js", ],
                                     exclude_directories=['.*', "Thirtover1", "images_source", "classic_images_source", "new_images_source", "imagesDrop_source", "Source" ])
wb_package_data.update(wb_resource_data)

setup(
    name="WebBrickRes",
    version="2.0",
    
    description="Webbrick Gateway Static Resources",
    long_description="""This egg contains graphic resources for the Webbrick Gateway applications, so updates can
 be made to these independant of updates to the application source.""",

    author="oh2m8 Ltd.",
    url="http://www.h2m8.com",
    
    install_requires = [
    ],
    scripts = [],
    zip_safe=False,
    packages=wb_packages,
    package_data = wb_package_data,
    keywords = [
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    )
    

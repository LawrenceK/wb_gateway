from setuptools import setup, find_packages
from turbogears.finddata import find_package_data, standard_exclude

#subpackages = ["events", "wbcnf", "WebBrick", "images"]
subpackages = ["events", "Gateway", "wbcnf", "WebBrick", "Images", "eventinterfaces", "css", "samples", "AppNotes"]

#wb_packages = find_packages()
wb_packages = find_packages() + subpackages

my_exclude = ('*.py', '*.pyc', '*~', '.*', '*.bak', '*.xhtml', '*.lore', '*.tex', '*.doc' )

wb_package_data = find_package_data(where='WebBrickDoc', package='WebBrickDoc', exclude=my_exclude)
#wb_resource_data = find_package_data(where="Gateway", package="Gateway", exclude=my_exclude )
#wb_package_data.update(wb_resource_data)

for sp in subpackages:
    wb_resource_data = find_package_data(where=sp, package=sp, exclude=my_exclude )
    wb_package_data.update(wb_resource_data)

print "wb_packages %s" % (wb_packages)
print "wb_package_data %s" % (wb_package_data)

setup(
    name="WebBrickDoc",
    version="2.0",
    
    description="Webbrick Documentation",
    long_description="""This egg contains documentation resources.""",

    author="WebBrickSystems Ltd.",
    url="http://www.WebBrickSystems.com",
    
    install_requires = [
    ],
    entry_points = {
#        'console_scripts': [
#          'webbrick_doc = WebBrickDoc.webbrick_doc:main',
#        ],
        'gui_scripts': [
          'webbrick_doc = WebBrickDoc.webbrick_doc:main',
        ],
    },
    scripts = [],
    zip_safe=False,
    data_files = [ ('', ['index.html']) ],
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
    

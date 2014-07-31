#!/opt/rocks/bin/python
#
#

from distutils.core import setup
import os

version = os.environ.get('ROCKS_VERSION')

# 
# main configuration of distutils
# 
setup(
    name = 'rocks-command-kvm',
    version = version,
    description = 'Rocks KVM python library extension',
    author = 'Phil Papadopoulos',
    author_email =  'philip.papadopoulos@gmail.com',
    maintainer = 'Luca Clementi',
    maintainer_email =  'luca.clementi@gmail.com',
    platforms = ['linux'],
    url = 'http://www.rocksclusters.org',
    #long_description = long_description,
    #license = license,
    #main package, most of the code is inside here
    packages = [line.rstrip() for line in open('packages')],
    #data_files = [('etc', ['etc/rocksrc'])],
    package_data={'rocks.db.mappings': ['*.sql']},
    # disable zip installation
    zip_safe = False,
    #the command line called by users    
    scripts=['rocks-create-vm-disks'],
)

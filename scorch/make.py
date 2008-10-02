# usage: setup.py py2exe

from distutils.core import setup
import py2exe
import os, sys
import glob
import zipfile
import shutil

packageName = 'scorcher'
version = '1.0'

if 'py2exe' not in sys.argv:
    sys.argv += ['py2exe']

shutil.rmtree(packageName, 1)       # in case it was left from last time
shutil.rmtree('build', 1)

setup(console=['scorcher.py', 'wikilist.py', 'setup.py'], \
    data_files=[('', [])], \
    options={'py2exe':{'dist_dir': packageName}})

# ~~~~ Create zip file

zipName = '%s%sr%s' % (packageName, version, os.popen('svnversion').read().strip().replace(':', '-'))

print
print 'Creating zip file %s.zip' % zipName

zip = zipfile.ZipFile(zipName+'.zip', 'w')
for directory in os.walk(packageName):
    prefix = directory[0]
    for filename in directory[2]:
        path = prefix+os.sep+filename
        zip.write(path, path[len(packageName)+1:])

print 'Removing the build directories'
shutil.rmtree(packageName)
shutil.rmtree('build')

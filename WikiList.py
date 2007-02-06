#! /usr/local/bin/python

import sys, os
from glob import glob
import fnmatch

def link(song):
    link = song.replace(' ', '_').replace(';', '%3b')
    return 'http://hymnal.ws/public/Songs/%s.htm' % link

def listPsalms(dest, filename):
    print >>sys.stderr, 'Working on "%s"' % filename
    song = os.path.basename(filename).replace('.htm', '')
    song = song.replace('_', ' ')
    if song.lower().startswith('psalm'):
        num = song[5:].split()[0]
        num = str(int(num[0:3])) + num[3:]
        name = ' '.join(song.split()[1:])
        print >>dest, '%s: %s' % (num, name),
    else:
        print >>dest, song,
    print >>dest, '- [%s view]' % link(song)
    print >>dest, ' * -'
    print >>dest

def main():
    argv = sys.argv

    if not sys.stdin.isatty():
        argv += sys.stdin.read().split()

    if not argv[1:]:
        print 'Usage: WikiList.py <list-htm-files>'
        print 'Wildcards are allowed'
        sys.exit(1)

    dest = sys.stdout
    for arg in argv[1:]:
        for filename in glob(arg):
            listPsalms(dest, filename)
    dest.close()


if __name__ == '__main__':
    main()

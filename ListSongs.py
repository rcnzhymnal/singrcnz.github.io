#! /usr/local/bin/python

"""See Songs\0Readme.txt for the .sib file naming requirements"""

import sys
from glob import glob
import fnmatch

songType = None                 # set to 'psalm' or 'Hymn' before running functions below

def titleSplit(title):
    title = title.replace('_', ' ')
    title2 = ''
    split = title.split(';', 1)
    title1 = split[0].strip()
    if len(split)>1:
        title2 = ';\xa0\xa0\xa0' + split[1].strip()
    return title1, title2

def coming(number, title=''):
    html = """<tr><td>coming</td><td></td><td>%s %s <i>%s</i>%s</td></tr>\n"""
    return html % ((songType.capitalize(), number) + titleSplit(title))

def proofing(name, number, title=''):
    html = """<tr><td>proofing</td><td>%s %s %s %s</td><td>%s %s <i>%s</i>%s</td></tr>\n"""

    satb = tuple( map(part, [name]*4, 'SATB') )

    return html % (satb + (songType.capitalize(), number) + titleSplit(title))

def withheld(name, number, title):
    html = """<tr><td><a href="Withheld.htm">withheld</a></td><td>%s %s %s %s</td><td>%s %s <i>%s</i>%s</td></tr>\n"""

    satb = tuple( map(part, [name]*4, 'SATB') )

    return html % (satb + (songType.capitalize(), number) + titleSplit(title))

def checkHtmExists(name):
    if not glob(name+'.htm'):
        print >>sys.stderr, 'Warning: %s.sib has no .htm' % name
        return False
    return True

def part(name, part):
    html = """ <a href="%s.htm">%s</a>"""

    basename = (name+' ').split(' ')[0]
    basename = basename.split('_')[0]

    if '/hymn' in basename.lower():
        basename = name

    partPattern = basename.replace('Songs/', 'Songs/parts/') + ('[_ ]*%s.sib' % part)
    partnames = glob(partPattern)

    if len(partnames) > 1:
        print >>sys.stderr, 'Warning: Using first of too many parts matching %s: %s' % (basename, partnames)
    if not partnames:
        return ''
    partname = partnames[0].replace('.sib', '').replace('\\', '/')
    if not checkHtmExists(partname):
        print >>sys.stderr, 'Warning: skipped file: no .htm file matching %s.sib' % partname
        return ''

    partname = partname.replace(' ', '%20').replace(';', '%3b')
    return html % (partname, part)

def view(name, number, title):
    html = """<tr><td><a href="%s">view/play</a></td><td>%s %s %s %s</td><td>%s %s <i>%s</i>%s</td></tr>\n"""

    checkHtmExists(name)
    link = (name+'.htm').replace(' ', '%20').replace(';', '%3b')
    satb = tuple( map(part, [name]*4, 'SATB') )
    return html % ((link,) + satb + (songType.capitalize(), number) + titleSplit(title))

def listSongs(songs):
    output = ''
    for filename in songs:
        name = filename.replace('\\', '/')
        name = name.split('.', 1)[0]

        number, title = (name.replace(' ', '_')+'_').split('_', 1)
        number = number.lstrip('Songs/%s' % songType)
        number = number.lstrip('0')

        if filename.endswith('.coming'):
            if filename.replace('.coming', '') in songs:
                print >>sys.stderr, 'Warning: %s file has no .sib' % filename
            output += coming(number, title)
        elif filename.endswith('.withheld'):
            output += withheld(name, number, title)
        elif filename.endswith('.proofed'):
            if filename.replace('.proofed', '.withheld') not in songs:
                output += view(name, number, title)
        else:
            if filename + '.proofed' not in songs and \
               filename + '.withheld' not in songs:
                output += proofing(name, number, title)

    return output

def psalm(n):
    songs = glob('Songs/%s%03d*.sib*' % (songType, n))
    if not songs:
        return coming(n)
    songs.sort()
    return listSongs(songs)

def listPsalms(dest):
    global songType
    songType = 'psalm'

    for n in range(1, 151):
        print >>dest, psalm(n)
        if n%10==0: print >>dest, '<tr><td>\xa0</td></tr>'

def listHymns(dest):
    global songType
    songType = 'Hymn'

    songs = glob('Songs/%s*.sib*' % songType)
    songs.sort()

    print >>dest, listSongs(songs)

def main():
    header = """<html><head><style type='text/css'>td {padding: 0 5}</style></head><body><table>"""
    footer = """</table></body></html>"""

    psalms = file('Psalms.htm', 'w')
    print >>psalms, header
    print >>psalms, "<h1>Psalms</h1>"
    listPsalms(psalms)
    print >>psalms, footer

    hymns = file('Hymns.htm', 'w')
    print >>hymns, header
    print >>hymns, "<h1>Hymns</h1>"
    print >>hymns, "<p>The only hymns listed here are ones that were associated with a psalm but we decided to put them in as a hymn.</p>"
    listHymns(hymns)
    print >>hymns, footer


if __name__ == '__main__':
    main()

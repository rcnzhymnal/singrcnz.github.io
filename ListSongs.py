#! /usr/local/bin/python

"""See Songs\0Readme.txt for the .sib file naming requirements"""

import sys
from glob import glob
import fnmatch

def titleSplit(title):
    title2 = ''
    split = title.split(';', 1)
    title1 = split[0].strip()
    if len(split)>1:
        title2 = ';\xa0\xa0\xa0' + split[1].strip()
    return title1, title2

def coming(number, title=''):
    html = """<p class=MsoNormal style='tab-stops:3.0cm right 219.75pt'><span lang=EN-AU>coming<span
        style='mso-tab-count:1'>""" + '\xa0'*21 + """</span>
        Psalm %s <i style='mso-bidi-font-style:normal'>%s</i>%s</span></p>\n"""
    return html % ((number,) + titleSplit(title))

def proofing(name, number, title=''):
    html = """<p class=MsoNormal style='tab-stops:3.0cm right 219.75pt'><span lang=EN-AU>proofing<span
        style='mso-tab-count:1'> \xa0%s %s %s %s%s\xa0\xa0 </span>
        Psalm %s <i style='mso-bidi-font-style:normal'>%s</i>%s</span></p>\n"""

    satb = tuple( map(part, [name]*4, 'SATB') )
    spaces = 4 - sum( [l!='' for l in satb] )
    spaces = '\xa0' * int(spaces * 3.6)

    return html % (satb + (spaces, number) + titleSplit(title))

def withheld(name, number, title):
    html = """<p class=MsoNormal style='tab-stops:3.0cm right 219.75pt'><span lang=EN-AU><a
        href="Withheld.htm">withheld</a><span style='mso-tab-count:1'> \xa0%s %s %s %s%s\xa0\xa0 </span>
        Psalm %s <i style='mso-bidi-font-style:normal'>%s</i>%s</span></p>\n"""

    satb = tuple( map(part, [name]*4, 'SATB') )
    spaces = 4 - sum( [l!='' for l in satb] )
    spaces = '\xa0' * int(spaces * 3.6)

    return html % (satb + (spaces, number) + titleSplit(title))

def checkHtmExists(name):
    if not glob(name+'.htm'):
        print >>sys.stderr, 'Warning: %s.sib has no .htm' % name
        return False
    return True

def part(name, part):
    html = """ <a href="%s.htm">%s</a>"""

    basename = (name+' ').split(' ')[0]
    basename = basename.split('_')[0]

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
    html = """<p class=MsoNormal style='tab-stops:3.0cm right 219.75pt'><span lang=EN-AU><a
        href="%s">view/play</a><span style='mso-tab-count:1'> %s %s %s %s%s""" + '\xa0'*2 + """ </span>
        Psalm %s <i style='mso-bidi-font-style:normal'>%s</i>%s</span></p>\n"""

    checkHtmExists(name)
    link = (name+'.htm').replace(' ', '%20').replace(';', '%3b')
    satb = tuple( map(part, [name]*4, 'SATB') )
    spaces = 4 - sum( [l!='' for l in satb] )
    spaces = '\xa0' * int(spaces * 3.6)
    return html % ((link,) + satb + (spaces, number) + titleSplit(title))

def psalm(n):
    songs = glob('Songs/psalm%03d*.sib*' % n)
    parts = fnmatch.filter(songs, 'Songs/psalm%03d_*.sib' % n)
    songs = [song for song in songs if song not in parts]

    if not songs:
        return coming(n)
    output = ''
    for filename in songs:
        name = filename.replace('\\', '/')
        name = name.split('.', 1)[0]

        number, title = (name+' ').split(' ', 1)
        number = number.lstrip('Songs/psalm')
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

def listPsalms(dest):
    for n in range(1, 151):
        print >>dest, psalm(n)
        if n%10==0: print >>dest, '<p></p>'

def main():
    source=file('Header.htm')
    dest = file('Songs.htm', 'w')

    for line in source:
        if line.strip() == '</div>':
            listPsalms(dest)
        print >>dest, line,

    dest.close()
    source.close()


if __name__ == '__main__':
    main()


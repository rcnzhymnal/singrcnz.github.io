#! /usr/local/bin/python

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

def withheld(number, title):
    html = """<p class=MsoNormal style='tab-stops:3.0cm right 219.75pt'><span lang=EN-AU><a
        href="Withheld.htm">withheld</a><span style='mso-tab-count:1'>""" + '\xa0'*19 + """ </span>
        Psalm %s <i style='mso-bidi-font-style:normal'>%s</i>%s</span></p>\n"""
    return html % ((number,) + titleSplit(title))

def part(name, part):
    html = """ <a href="%s_%s.htm">%s</a>"""

    basename = (name+' ').split(' ')[0]
    basename = basename.split('_')[0]

    if glob('%s_%s.sib' % (basename, part)):
        return html % (basename, part, part)
    return ''

def view(name, number, title):
    html = """<p class=MsoNormal style='tab-stops:3.0cm right 219.75pt'><span lang=EN-AU><a
        href="%s">view/play</a><span style='mso-tab-count:1'> %s %s %s %s%s""" + '\xa0'*2 + """ </span>
        Psalm %s <i style='mso-bidi-font-style:normal'>%s</i>%s</span></p>\n"""

    link = (name+'.htm').replace(' ', '%20')
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
            output += coming(number, title)
        elif filename.endswith('.withheld'):
            output += withheld(number, title)
        else:
            if filename + '.withheld' not in songs:
                output += view(name, number, title)

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

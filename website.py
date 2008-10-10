from glob import glob
import os, sys

Cd = False              # Whether --cd option is given to produce CD files
Ext = 'sib'
Songdir = 'Songs'
Partsdir = 'Songs/parts/'
Types = ['psalm', 'Hymn']
Stats = ['coming', 'withheld', 'proofed']
Ignore = ['Psalm Template.sib', 'sample---unprintable.sib']  # Files to ignore
IncludeExt = 'inc'
Templates = [ f.rsplit('.', 1)[0] for f in glob('*.inc') ]

def urljoin(*pieces):
    if not pieces: return ''

    if pieces[0].startswith('/'): start = True
    else: start = False
    if pieces[-1].endswith('/'): end = True
    else: end = False

    url = ''
    for p in pieces:
        url += '/' + p.strip('/')
    if not start: url = url.lstrip('/')
    if end: url += '/'
    return url

def path2url(path):
    return path.replace(os.path.sep, '/')

def normtype(typ):
    for t in Types:
        if typ.lower() == t.lower(): typ = t
    return typ

def filename2name(filename, folder):
    """ Given a single filename, with possible 'typ', '.status' and '.sib'
        prefixes/suffixes, return num_name.
        Strips possible directory prefix, and typ, .status, .sib
    """
    filename = os.path.split(filename)[1]
    for typ in Types:
        if filename.lower().startswith(typ.lower()): filename = filename[len(typ):]
    for stat in Stats:
        if (filename.endswith('.' + stat)): filename = filename.rsplit('.', 1)[0]
    if filename.endswith('.'+Ext): filename = filename.rsplit('.', 1)[0]
    return filename

def num2name(n, folder):
    """ Return the name of song n
    """
    song = glob(os.path.join(folder, '*%s_*.sib') % n)
    dot = glob(os.path.join(folder, '*%s_*.sib.*') % n)
    if song: return filename2name(song[0], folder)
    elif dot: return filename2name(dot[0], folder)
    return None

def normalize(numorname, folder):
    """ Take either a song number or a full song name, and return num_name
    """
    numorname = numorname.replace(' ', '_')
    song = glob(os.path.join(folder, '*%s.sib') % numorname)
    dot = glob(os.path.join(folder, '*%s.sib.*') % numorname)
    if song or dot: return numorname

    return num2name(numorname, folder)

class Song(object):
    file = ''       # primary .sib file for the given song, excluding directory & extension
    type = ''
    files = []      # all the files relevant to this song (except parts), excluding directory, but including extension
    stats = []      # all the statuses relevant to this song
    name = ''       # name of given song
    num = ''        # number of the given song
    title = ''
    folder = ''     # directory this song is in
    def __init__(self, name, folder=Songdir):
        name = normalize(name, folder)
        self.folder = folder
        filename = glob(os.path.join(self.folder, '*%s.sib') % name)[0]
        self.file = os.path.split(filename)[1].rsplit('.', 1)[0]

        self.type = ''
        for t in Types:
            if self.file.startswith(t): self.type = t

        self.files = glob(os.path.join(self.folder, '*%s*') % name)
        self.files = [ os.path.split(f)[1] for f in self.files ]
        self.stats = []
        for f in self.files:
            for stat in Stats:
                if f.endswith('.' + stat): self.stats += [stat]
        self.name = name.split('_', 1)[1]
        self.num = name.split('_', 1)[0]
        self.title = self.name.replace('_', ' ')

    @classmethod
    def all(cls, typ=None, folder=Songdir):
        """ Return a list of all songs, whatever status, as a list of num_names
        """
        if typ is None: typ = ''
        typ = normtype(typ)
        songs = glob(os.path.join(folder, '%s*.sib') % (typ))
        dotnames = glob(os.path.join(folder, '%s*.sib.*') % (typ))
        songs = sorted([ filename2name(f, folder) for f in songs if (os.path.split(f)[1] not in Ignore) ])
        for dot in dotnames:
            dot = filename2name(dot, folder)
            if dot not in songs: songs += [dot]
        return [ Song(song) for song in songs ]

    def checkfile(self, ext):
        """ Check that the file of type 'ext' corresponding to this song exists
        """
        return os.path.exists(os.path.join(self.folder, self.file+'.'+ext))

    def partfile(self, part):
        """ Returns the part's filename, excluding prefixes & suffixes
            Looks in Partsdir
            Tries (in this order):
                1. typ_name_PART
                2. typnum_PART
                3. typnum_name_PART
        """
        part = part.upper()
        totry = ['%s_%s_%s' % (self.type, self.name, part),
                 '%s%s_%s' % (self.type, self.num, part),
                 '%s%s_%s_%s' % (self.type, self.num, self.name, part)]
        for t in totry:
            if os.path.exists(os.path.join(Partsdir, t+'.sib')): return t
        return None

class output:
    # (link, X)
    satb = """<a href="%s.htm">%s</a>&nbsp;"""

    # (link, clickme, SATB, typ, num, title)
    viewable = """<tr><td><a href="%s.htm">%s</a></td><td>%s</td><td><b>%s %s</b>&nbsp;&nbsp;<i>%s</i></td></tr>\n"""

    hymntext = "<h1>Hymns</h1>\n<p>The only hymns listed here are ones that were associated with a psalm but we decided to put them in as a hymn.</p>"
    psalmtext = "<h1>Psalms</h1>"

    # (title, id, mainmenu, submenu)
    header = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>

<head>
<title>RCNZ Psalter Hymnal: %s</title>

<link rel="stylesheet" type="text/css" href="main.css" />
<body id="%s"><div id="container">
<div id="header">
<div id="header-left"></div>

<div id="header-right"></div>
</div>

%s

%s
<div id="content">
"""

    # ()
    mainmenu = """<div id="mainMenu">
<div class="header">
<h3>Reformed Churches</h3>
</div>

<ul>
<li class="background1"><a href="Start.htm">Hymnal homepage</a></li>

<li class="background1"><a href="Songs.htm">Brief info on songs</a></li>

<li class="background1"><a href="Psalms.htm">Browse psalms</a></li>

<li class="background1"><a href="Hymns.htm">Browse hymns</a></li>

<li class="background1"><a href="Contributions.htm">Contribute</a></li>
</ul>

<ul>
<li class="background5"><a href="http://rcnz.org.nz">RCNZ Homepage</a></li>

<li class="background5"><a href="http://hymnal.ws/trac">Committee Login</a></li>

</ul>

<ul>
<li class="background5"></li>

<li class="background5">
<div class="connector"></div>
</li>

</ul>

<div class="footer">
<div id="source-link">web development by<a target="_blank" href="http://brush.co.nz">Brush Technology</a></div>
</div>
</div>
"""
    # ()
    submenu = """<div id="subMenu">
<div class="corner TL"></div>

<div class="corner TR"></div>

<div class="corner BR"></div>

<div class="corner BL"></div>

<div class="connector"></div>

<div class="container"><a href="Psalms.htm">Browse psalms</a><a href="Hymns.htm">Browse hymns</a></div>
</div>
"""

    # ()
    footer = """</div>
</div></body>
</html>
"""
    @classmethod
    def parts(cls, song):
        satb = ''
        for p in ['S', 'A', 'T', 'B']:
            f = song.partfile(p)
            if f: satb += cls.satb % (urljoin(path2url(Partsdir), f), p)
        return satb


    @classmethod
    def listing(cls, song):
        parts = cls.parts(song)
        link = urljoin(path2url(Songdir), song.file)
        clickme = 'view/play'

        if 'coming' in song.stats:
            parts = ''
            link = 'Coming'
            clickme = 'coming'
        elif 'withheld' in song.stats and not Cd:
            parts = ''
            link = 'Withheld'
            clickme = 'withheld'
        elif 'proofed' not in song.stats:
            parts = ''
            link = 'Proofing'
            clickme = 'proofing'

        return cls.viewable % (link, clickme, parts, song.type.capitalize(), song.num.lstrip('0'), song.title)

    @classmethod
    def listsongs(cls, typ, toptext):
        out = output.header % (typ.capitalize()+'s', typ, output.mainmenu, output.submenu)
        out += toptext
        songs = Song.all(typ)
        out += '<table class="songs">'
        num = 1
        for s in songs:
            print >>sys.stderr, s.name
            out += cls.listing(s)
            try: num = int(s.num)
            except ValueError: pass
            if num%10 == 0: out += '<tr><td><br /></td></tr>\n'
        out += '</table>'
        out += output.footer
        return out

    @classmethod
    def template(cls, fname):
        f = file(fname+'.'+IncludeExt)
        return cls.header % (fname.capitalize(), fname.lower(), cls.mainmenu, cls.submenu) + f.read() + cls.footer

def main():
    f = file('Psalms.htm', 'w')
    print >>f, output.listsongs('psalm', output.psalmtext)
    f = file('Hymns.htm', 'w')
    print >>f, output.listsongs('hymn', output.hymntext)
    for t in Templates:
        f = file(t+'.htm', 'w')
        print >>f, output.template(t)

if __name__ == '__main__':
    if ('--cd' in sys.argv):
        Cd = True

    main()

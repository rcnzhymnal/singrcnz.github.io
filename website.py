#!/usr/bin/env python2

from glob import glob
import os, sys, time

import projectable

Cd = False              # Whether --cd option is given to produce CD files
Ext = 'sib'
Songdir = 'Songs'
Hymndir = 'Hymns'
Pptdir = 'slides'
Pdfdir = 'Songs/PsalmsPDF'
Pdfdir2 = 'Hymns'
Partsdir = 'Songs/parts/'
Types = ['psalm', 'Hymn']
Stats = ['coming', 'music_withheld', 'words_withheld', 'proofed']
Ignore = ['Psalm Template.sib', 'sample---unprintable.sib', 'Hymn Template.sib']  # Files to ignore
IncludeExt = 'tmpl.html'
Templates = [ f.rsplit('.', 2)[0] for f in glob('*.tmpl.html') ]

Warnings = []

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
    """ Given a single filename, with possible 'typ' prefix (psalm/hymn) and
        possible suffix (.coming, .music_withheld, .words_withheld, .proofed), return number_name.
        Strips possible directory prefix and typ and .coming, .music_withheld, .words_withheld, .proofed
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

def np_if_exists(path):
    """ return no-print path if it exists instead of path """
    if os.path.exists(path.replace('.pdf', '.np.pdf')):
        path = path.replace('.pdf', '.np.pdf')
    return path


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
        global Warnings
        oldname = name
        name = normalize(name, folder)
        if name == None:
            raise Exception("problem normalizing file %s (spaces, perhaps?)" % oldname)
        self.folder = folder
        try:
            filename = glob(os.path.join(self.folder, '*%s.sib') % name)[0]
        except IndexError:
            Warnings += ["Warning: skipped song because no .sib file found in '%s' for file '%s'\b" % (self.folder, name)]
            self.file = None
            return
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
        self.num = name.split('_', 1)[0].split('-', 1)[0]
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
        songs = [ Song(song, folder) for song in songs ]
        return [ song for song in songs if song.file is not None ]

    def checkfile(self, ext, folder=None):
        """ Check that the file of type 'ext' corresponding to this song exists
        """
        if folder == None: folder = self.folder
        return os.path.exists(os.path.join(folder, self.file+'.'+ext))

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
    link = """<a href="%s">%s</a>"""

    # (link, clickme, SATB, typ, num, title, filelinks)
    viewable = """<tr><td><a href="%s">%s</a></td><td>%s</td><td><b>%s %s</b>&nbsp;&nbsp;<i>%s</i></td><td>%s</td></tr>\n"""

    hymntext2 = """<h1>Hymns</h1>
        <p>Below are playable or pdf versions of the Hymns.
        These also have certain <a href="Copyright.html">Copyright restrictions</a>.
        You <b>must</b> refer to these restrictions before reproducing copyrighted music or lyrics.
        </p>
        $update"""
    psalmtext = """<h1>Psalms</h1>
        <p>Below are playable or pdf versions of the Psalms.
        These also have certain <a href="Copyright.html">Copyright restrictions</a>.
        You <b>must</b> refer to these restrictions before reproducing copyrighted music or lyrics.
        </p>"""

    # (title, id, mainmenu, submenu)
    header = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>

<head>
<title>RCNZ Psalter Hymnal: {title}</title>

<link rel="stylesheet" type="text/css" href="main.css" />
<body id="{id}"><div id="container">
<div id="header">
<div id="header-left"></div>

<div id="header-right"></div>
</div>

{mainmenu}

{submenu}
<div id="content" class="songlist">
"""

    # ()
    mainmenu = """<div id="mainMenu">
<div class="header">
<h3>Reformed Churches</h3>
</div>

<ul>
<li class="background1"><a href="Start.html">Hymnal homepage</a></li>
<li class="background1"><a href="Psalms.html">Browse psalms</a></li>
<li class="background1"><a href="Hymns.html">Browse hymns</a></li>
<li class="background1"><a href="Musicians.html">Musicians page</a></li>
<li class="background1"><a href="About.html">About the hymnal</a></li>
<li class="background1"><a href="Contacts.html">Contact</a></li>
</ul>

<ul>
<li class="background5"><a href="http://rcnz.org.nz">RCNZ Homepage</a></li>
<li class="background5"><a href="login.html">Committee Login</a></li>
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
<div class="container"><a href="Psalms.html">Browse psalms</a><a href="Hymns.html">Browse hymns</a></div>
</div>
"""

    # ()
    footer = """</div>
</div></body>
</html>
"""
    @classmethod
    def parts(cls, song):
        satb = []
        for p in ['S', 'A', 'T', 'B']:
            f = song.partfile(p)
            if f: satb += [cls.link % (urljoin(path2url(Partsdir), f+'.htm'), p)]
        satb = '&nbsp;'.join(satb)
        return satb


    pdf = None
    @classmethod
    def listing(cls, song, folder):
        parts = cls.parts(song)
        link = urljoin(path2url(folder), song.file+'.htm')
        clickme = 'view/play'

        files = []
        # workaround for Jessica's different naming scheme
        strange_nums = {
            '051b1': '051b',
            '051b2': '051b',
            '072+72b': '072b',
            '119v025b': '119v025-032 b',
        }
        if song.num in strange_nums:
            song.num = strange_nums[song.num]
        pptfile = glob(os.path.join(Pptdir, song.num + '*.ppt*'))

        if song.checkfile('pdf', Pdfdir):
            cls.pdf = cls.link % (np_if_exists(urljoin(path2url(Pdfdir), song.file+'.pdf')), 'PDF')
        # hack to handle alternate_layout hymns laid out for web view only
        elif os.path.exists(os.path.join(Pdfdir2, 'alternate_layout_'+song.file+'.pdf')):
            cls.pdf = cls.link % (np_if_exists(urljoin(path2url(Pdfdir2), 'alternate_layout_'+song.file+'.pdf')), 'PDF')
        elif song.checkfile('pdf', Pdfdir2):
            cls.pdf = cls.link % (np_if_exists(urljoin(path2url(Pdfdir2), song.file+'.pdf')), 'PDF')
        else:
            global Warnings
            if 'music_withheld' not in song.stats:
                Warnings += ["Warning: pdf missing for %s %s %s; linking to previous pdf instead" % (song.type, song.num, song.title)]
        if ('music_withheld' in song.stats or 'words_withheld' in song.stats) and not Cd:
            files += ['']
        else:
            files += [cls.pdf]

        projectable_status = projectable.status(song.num)
        if pptfile:
            if 'words_withheld' in song.stats and not Cd:
                files += ['Powerpoint:', cls.link % ('Projection.html', '<i>Contact</i>')]
            else:
                files += [cls.link % (path2url(pptfile[0]), 'Powerpoint:')]
                if projectable_status.facr and projectable_status.ccli:
                    files += [cls.link % ("Copyright.html", "CCLI reqd.")]
                else:
                    files += [cls.link % ("Copyright.html", "free to use")]
        else:
            files += ['?']

        if 'coming' in song.stats:
            parts = ''
            link = 'Coming.html'
            clickme = 'coming'
        elif 'music_withheld' in song.stats and not Cd:
            parts = ''
            link = 'Withheld.html'
            clickme = 'withheld'
        elif 'proofed' not in song.stats:
            parts = ''
            link = 'Proofing.html'
            clickme = 'proofing'

        files = '</td><td>'.join(files)

        result = cls.viewable % (link, clickme, parts, song.type.capitalize(), song.num.lstrip('0'), song.title, files)
        return result

    @classmethod
    def listsongs_top(cls, typ):
        return output.header.format(title=typ.capitalize()+'s', id=typ, mainmenu=output.mainmenu, submenu=output.submenu, redirect=typ.lower()+'s')

    @classmethod
    def listsongs(cls, typ):
        out = ''
        songs = Song.all(typ)
        out += '<table class="songs">'
        num = 1
        for s in songs:
            print s.name
            try: num = int(s.num)
            except ValueError: num = 0
            if num%10 == 0 and num != 0: out += '<tr><td style="border:none"><br /></td></tr>\n'
            out += cls.listing(s, Songdir)
        out += '</table>'
        return out

    @classmethod
    def listpsalms(cls, typ, toptext):
        out = cls.listsongs_top(typ)
        out += toptext
        out += cls.listsongs(typ)
        out += output.footer
        return out

    @classmethod
    def listhymns(cls, typ):
        out = ''
        songs = Song.all(typ, Hymndir)
        out += '<table class="songs">'
        num = 0
        prev = None
        for s in songs:
            if s.num == prev:       # skip some hymns that are doubled because the second one in the repository is a double-page version
                continue
            print s.name
            if num%10 == 0 and num != 0: out += '<tr><td style="border:none"><br /></td></tr>\n'
            num = num+1
            out += cls.listing(s, Hymndir)
            prev = s.num
        out += '</table>'
        return out

    @classmethod
    def template(cls, fname):
        f = file(fname+'.'+IncludeExt)
        content = cls.header.format(title=fname.capitalize(), id=fname.lower(), mainmenu=cls.mainmenu, submenu=cls.submenu, redirect=fname.lower()) + f.read() + cls.footer
        if fname == 'Contacts':
            yaml = "---\ntitle: Contacts\nredirect_from:\n- /contacts\n- /contact\n---\n"
            content = yaml + content
        return content

def main():
    # define locals to pass into templates
    date = time.strftime('%d %B %Y')
    if Cd:
        update = """
            <p class='alert-message'>Updates of this page will be
            <a href="http://hymnal.rcnz.org.nz/public/$page">available on the web here</a>.</p>
            """
        cdheader = """
            <h3>QuickStart</h3>
            <p>You can view the entire contents of the printed book in several formats:<br />
            <ul>
             <li><a href='Songs/Lyrics/Sing%20to%20the%20Lord%20-%20words%20only.doc'>MS-Word</a>
             | <a href='Songs/Lyrics/Sing%20to%20the%20Lord%20-%20words%20only.txt'>text</a>
             | <a href='Sing%20to%20the%20Lord%20-%20provisional.pdf'>PDF-score</a>
             (if needed, install this <a href='FoxitReader23_setup.exe'>PDF viewer</a>)</li>
             <li>Browse and play
              <font color='red'>
               (You&rsquo;ll need to install the &ldquo;Scorch&rdquo; software; choose your operating system:
               <a href="ScorchInstallers/Scorch521AllBrowsersInstaller.msi">Windows XP</a> |
               <a href="ScorchInstallers/SibeliusScorch521.dmg">Macintosh</a>).
              </font>
             </li>
            </ul>
            <hr />
            """
        copyright = """
            <p>
             This CD contains the PDF (score) and text (lyrics) files of the whole printed book.
             It is important to note that copyright for these are tied up with the book and you may
             copy neither them nor this CD beyond the number of books that you own.</p>
            """
    else:
        update = ''
        cdheader = ''
        copyright = ''


    if not '--templates-only' in sys.argv:
        f = file('Psalms.html', 'w')
        print >>f, output.listpsalms('psalm', output.psalmtext)

        f = file('Hymns.html', 'w')
        print >>f, output.listsongs_top('hymn')
        print >>f, output.hymntext2.replace('$update', update).replace('$page','Hymns.html')
        print >>f, output.listhymns('hymn')
        print >>f, output.footer

    for t in Templates:
        f = file(t+'.html', 'w')
        text = output.template(t)
        text = text.replace('$update', update)
        text = text.replace('$cdheader', cdheader)
        text = text.replace('$copyright', copyright)
        text = text.replace('$date', date)
        text = text.replace('$page', t+'.html')
        print >>f, text

if __name__ == '__main__':
    if ('--cd' in sys.argv):
        Cd = True

    main()
    print
    print >>sys.stderr, '\n'.join(Warnings)


#!/usr/bin/env python3
# Hymnal website builder: generates html files for all the sibelius songs in the Psalms and Hymns 'sib' subfolders.

"""
This script works by finding all .sib files in the Psalms folder and then again in the Hymns folder.
For each file found, it creates a Song object with attribute fields:
    .file: the filename without path or extension
    .files: list of existing filenames related to this song without path but with extension
    .type: ('psalm' or 'Hymn')
    .stats: list of strings which match Stats ('proofed', 'coming', etc) for which there is a file in the stats folder with a matching extension
    .name: name of given song taken from the filename but without the hymn+number prefix and without the extension
    .title: same as name but with underscores changed to space
    .num: number (text) of the given song
    .folder: directory this song is in (Hymns or Psalms)
For each Song object, adds it to a table row in Hymns.html or Psalms.html containing a table of songs (Hymns.html or Psalms.html).
The table entries vary depending on the stats (see above).
"""

import os
import sys
import time
import re
import argparse
import subprocess, shlex

from glob import glob

import templates
import projectable

Ext = 'sib'
Songdir = 'Psalms'
Hymndir = 'Hymns'
Pptdir = 'slides'
Pdfdir = 'Psalms/pdf'
Pdfdir2 = 'Hymns/pdf'
Partsdir = 'Psalms/parts/'
Types = ['psalm', 'Hymn']
Stats = ['coming', 'music_withheld', 'words_withheld', 'proofed', 'single_song.sib']
Ignore = ['Psalm Template.sib', 'sample---unprintable.sib', 'Hymn Template.sib']  # Files to ignore
IncludeExt = 'tmpl.html'

Warnings = []

required_version = (3, 5) # required for subprocess.run
if sys.version_info < required_version:
    print(f"Python version must be at least {'.'.join(str(s) for s in required_version)} to run this script.")
    sys.exit(1)

def urljoin(*pieces):
    if not pieces: return ''

    start = pieces[0].startswith('/')
    end = pieces[-1].endswith('/')

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
    song = glob(os.path.join(folder, 'sib', '*%s_*.sib') % n)
    dot = glob(os.path.join(folder, 'sib', '*%s_*.sib.*') % n)
    if song: return filename2name(song[0], folder)
    elif dot: return filename2name(dot[0], folder)
    return None

def normalize(numorname, folder):
    """ Take either a song number or a full song name, and return num_name
    """
    numorname = numorname.replace(' ', '_')
    song = glob(os.path.join(folder, 'sib', '*%s.sib') % numorname)
    song_single = glob(os.path.join(folder, 'sib', '*%s.single_song.sib') % numorname)
    dot = glob(os.path.join(folder, 'sib', '*%s.sib.*') % numorname)
    if song or song_single or dot: return numorname

    return num2name(numorname, folder)

def run(*args, exit_code=False):
    """ Run program specified by args and return combined stdout/stderr as a string
         If exit_code is true, return the exit code rather than the string
    """
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if exit_code:
        return p.returncode
    if p.returncode:
        print(f"\nError {p.returncode} running command:")
        print(' '.join(shlex.quote(s) for s in args))
        print(p.stdout.strip(), end='')
        sys.exit(p.returncode)
    return p.stdout.strip()

def np_if_exists(path):
    """ return no-print path if it exists instead of path """
    no_print = path.replace('.pdf', '.np.pdf')
    if os.path.exists(no_print):
        # If necessary, regenerate the .np.pdf from the .pdf file to ensure it has print disabled
        # First check git modified date to see if it needs updating
        np_date = run('git', 'log', '-1', '--format=%cd', '--date=iso', '--', no_print)
        date = run('git', 'log', '-1', '--format=%cd', '--date=iso', '--', path)
        modified = run('git', 'diff', '-s', '--exit-code', path, exit_code=True)
        if np_date < date or modified:
            print(" Generating non-printable version:", no_print)
            run('cpdf', '-encrypt', '40bit', 'prohibit', '', '-no-print', path, '-o', no_print)
        path = path.replace('.pdf', '.np.pdf')
    return path


class Song(object):
    file = ''       # primary .sib file for the given song, excluding directory & extension
    type = ''
    files = []      # all the files relevant to this song (except parts), excluding directory, but including extension
    stats = []      # all the statuses relevant to this song
    name = ''       # name of given song taken from the filename but without the hymn+number prefix and without the extension
    title = ''      # same as name but with underscores changed to space
    num = ''        # number (text) of the given song
    folder = ''     # directory this song is in (Hymns or Psalms)
    def __init__(self, name, folder=Songdir):
        global Warnings
        oldname = name
        name = normalize(name, folder)
        if name == None:
            raise Exception("problem normalizing file %s (spaces, perhaps?)" % oldname)
        self.folder = folder
        try:
            filename = (glob(os.path.join(self.folder, 'sib', '*%s.sib') % name) + glob(os.path.join(self.folder, 'sib', '*%s.single_song.sib') % name))[0]
        except IndexError:
            Warnings += ["Warning: skipped song because no .sib file found in '%s' for file '%s'\b" % (self.folder, name)]
            self.file = None
            return
        self.file = os.path.split(filename)[1].rsplit('.', 1)[0]

        self.type = ''
        for t in Types:
            if self.file.startswith(t): self.type = t

        # Find this Song in /sib subfolder
        self.files = glob(os.path.join(self.folder, 'sib', '*%s*') % name)
        self.files = [ os.path.split(f)[1] for f in self.files ]
        # Find any matching 'stats' files in the 'stats' directory
        self.statsfiles = glob(os.path.join(self.folder, 'stats', '*%s*') % name)
        self.statsfiles = [ os.path.split(f)[1] for f in self.statsfiles ]
        self.stats = []
        for f in self.statsfiles:
            for stat in Stats:
                if f.endswith('.' + stat): self.stats += [stat]
        self.name = name.split('_', 1)[1]
        self.num = name.split('_', 1)[0].split('-', 1)[0]
        self.title = self.name.replace('_', ' ').replace('.single_song.', '.')

    @classmethod
    def all(cls, typ=None, folder=Songdir):
        """ Return a list of all songs, whatever status, as a list of num_names
        """
        if typ is None: typ = ''
        typ = normtype(typ)
        songs = glob(os.path.join(folder, 'sib', '%s*.sib') % (typ))
        songs = [song.replace('.single_song.', '.') for song in songs]
        dotnames = glob(os.path.join(folder, 'sib', '%s*.sib.*') % (typ))
        songs = sorted([ filename2name(f, folder) for f in songs if (os.path.split(f)[1] not in Ignore) ])
        for dot in dotnames:
            dot = filename2name(dot, folder)
            if dot not in songs: songs += [dot]
        songs = [ Song(song, folder) for song in songs ]
        return [ song for song in songs if song.file is not None ]

    def checkfile(self, ext):
        """ Check that the file of type 'ext' corresponding to this song exists
        """
        dir = 'other'
        if ext=='pdf': dir='pdf'
        if ext=='sib': dir='sib'
        if ext=='htm': dir=''
        return os.path.exists(os.path.join(self.folder, dir, self.file+'.'+ext))

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
    @classmethod
    def parts(cls, song):
        satb = []
        for p in ['S', 'A', 'T', 'B']:
            f = song.partfile(p)
            if f: satb += [templates.link % (urljoin(path2url(Partsdir), f+'.htm'), p)]
        satb = '&nbsp;'.join(satb)
        return satb


    pdf = None
    @classmethod
    def listing(cls, song, typ, folder):
        parts = cls.parts(song)
        link = urljoin(path2url(folder), song.file+'.htm')
        clickme = 'view/play'

        files = []
        # workaround for Jessica's different naming scheme
        strange_nums = {
            '051b1': '051b',
            '051b2': '051b',
            '119v025b': '119v025-032 b',
        }
        if song.num in strange_nums:
            song.num = strange_nums[song.num]

        # Find .pptx file -- hacky translation of "_PartN" to " part N"
        match = re.match("psalm"+song.num+"_part([0-9])", song.file, re.IGNORECASE)
        if match:
            pptfile = glob(os.path.join(Pptdir, song.num + ' part '+match.group(1)+'*.ppt*'))
        else:
            if 'v' in song.num:
                pptfile = glob(os.path.join(Pptdir, song.num + '*.ppt*'))
            else:
                pptfile = glob(os.path.join(Pptdir, song.num + ' *.ppt*'))
        pptfile.sort()

        # hack to handle .single-song.pdf hymns laid out for web view only
        if os.path.exists(os.path.join(song.folder, 'pdf', song.file+'.single_song.pdf')):
            cls.pdf = templates.link % (np_if_exists(urljoin(song.folder, 'pdf', song.file+'.single_song.pdf')), 'PDF')
        elif song.checkfile('pdf'):
            cls.pdf = templates.link % (np_if_exists(urljoin(song.folder, 'pdf', song.file+'.pdf')), 'PDF')
        else:
            global Warnings
            if 'music_withheld' not in song.stats:
                Warnings += ["Warning: pdf missing for %s %s %s; linking to previous pdf instead" % (song.type, song.num, song.title)]
        if ('music_withheld' in song.stats or 'words_withheld' in song.stats) and not Args.cd:
            files += ['']
        else:
            files += [cls.pdf]

        projectable_status = projectable.status(song.num)
        if pptfile:
            if 'words_withheld' in song.stats and not Args.cd:
                files += ['Powerpoint: ', templates.link % ('Projection.html', '<i>contact</i>')]
            else:
                files += [templates.link % (path2url(pptfile[0]), 'Powerpoint:')]
                if projectable_status.facr and projectable_status.ccli:
                    files += [templates.link % ("Copyright.html", "CCLI&nbsp;reqd.")]
                else:
                    files += [templates.link % ("Copyright.html", "free&nbsp;to&nbsp;use")]
        else:
            files += ['?']

        if 'coming' in song.stats:
            parts = ''
            link = 'Coming.html'
            clickme = 'coming'
        elif 'music_withheld' in song.stats and not Args.cd:
            parts = ''
            link = 'Withheld.html'
            clickme = 'withheld'
        elif 'proofed' not in song.stats:
            parts = ''
            link = 'Proofing.html'
            clickme = 'proofing'

        files = '</td><td>'.join(files)

        result = templates.viewable % (link, clickme, parts, song.type.capitalize(), song.num.lstrip('0'), song.title, files)
        return result

    @classmethod
    def listsongs_header(cls, typ):
        return templates.header.format(title=typ.capitalize()+'s', id=typ, mainmenu=templates.mainmenu, submenu=templates.submenu, redirect=typ.lower()+'s')

    @classmethod
    def listpsalms(cls, typ):
        out = ''
        songs = Song.all(typ, Songdir)
        out += '<table class="songs">'

        for s in songs:
            if not Args.quiet: print(s.name)
            try: num = int(s.num)
            except ValueError: num = 0
            if num%10 == 0 and num != 0: out += '<tr><td style="border:none"><br /></td></tr>\n'
            out += cls.listing(s, type, Songdir)
        out += '</table>'
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
            if not Args.quiet: print(s.name)
            if num%10 == 0 and num != 0: out += '<tr><td style="border:none"><br /></td></tr>\n'
            num = num+1
            out += cls.listing(s, typ, Hymndir)
            prev = s.num
        out += '</table>'
        return out

    @classmethod
    def template(cls, fname):
        f = open(fname+'.'+IncludeExt)
        content = templates.header.format(title=fname.capitalize(), id=fname.lower(), mainmenu=templates.mainmenu, submenu=templates.submenu, redirect=fname.lower()) + f.read() + templates.footer
        if fname == 'Contacts':
            yaml = "---\ntitle: Contacts\nredirect_from:\n- /contacts\n- /contact\n---\n"
            content = yaml + content
        return content


def main():
    # If run from the builder directory, move into root directory where the song directories are
    if os.getcwd().endswith('/builder'):
        os.chdir('..')

    # define locals to pass into templates
    date = time.strftime('%d %B %Y')

    update = cdheader = copyright = ''
    if Args.cd:
        update = templates.cdupdate
        cdheader = templates.cdheader
        copyright = templates.cdcopyright

    if not Args.nosongs:
        with open('Psalms.html', 'w') as f:
            print(output.listsongs_header('psalm') + templates.psalmtext + output.listpsalms('psalm') + templates.footer, file=f)

        with open('Hymns.html', 'w') as f:
            hymntext = templates.hymntext.replace('$update', update).replace('$page','Hymns.html')
            print(output.listsongs_header('hymn') + hymntext + output.listhymns('hymn') + templates.footer, file=f)

    for t in [ f.rsplit('.', 2)[0] for f in glob('*.tmpl.html') ]:
        print(t)
        text = output.template(t)
        text = text.replace('$update', update)
        text = text.replace('$cdheader', cdheader)
        text = text.replace('$copyright', copyright)
        text = text.replace('$date', date)
        text = text.replace('$page', t+'.html')
        with open(t+'.html', 'w') as f:
            print(text, file=f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create website html files listing all the hymns')
    parser.add_argument('--cd', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('--nosongs', action='store_true')
    Args = parser.parse_args()
    main()
    if not Args.quiet:
        print()
    print('\n'.join(Warnings), file=sys.stderr)

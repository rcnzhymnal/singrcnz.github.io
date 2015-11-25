""" Determine how freely projectable a song is from the CCLI spreadsheet (.csv file) """

import os, sys, csv, collections

CCLI_CSV_FILE = 'CCLI Index Spreadsheet 3-12-13.csv'
Songs = {}
Song = collections.namedtuple('Song', 'num, name, ccli, facr, sortkey')

def load_csv(filename):
    """ Load csv file and extract only songs with FACR lyrics and flag whether they are projectable """

    songs = {}
    with open(filename) as f:
        reader = csv.reader(f, dialect='excel')
        reader.next()   # skip first row
        for field in reader:
            num, name, text_admin, ccli_no = field[0], field[3], field[4], field[5]
            if name in ['']:
                continue
            ccli = 'n/a' in ccli_no.lower()
            facr = 'FACR' in text_admin.upper()
            if not ccli and not facr:
                continue
            num = num.replace(' ', '')
            sortkey = (num+',').replace(':', ',').replace('part', ',').replace('b', ',').replace('c', ',').split(',')
            sortkey = (int(sortkey[0]),) + tuple(sortkey[1:])
            songs[num] = Song(num, name, ccli, facr, sortkey)
    ordered = collections.OrderedDict(sorted(songs.items(), key=lambda k: k[1].sortkey))
    return ordered

def status(number):
    """ Return namedtuple containing a song song's lyrics' CCLI status and whether it is owned by FACR as attributes .ccli and .facr """
    number = str(number).lstrip('0')
    global Songs
    if not Songs:
        Songs = load_csv(CCLI_CSV_FILE)
    if number not in Songs:
        return Song(number, 'unknown', False, False, number)
    return Songs[number]

if __name__ == '__main__':
    songs = load_csv(CCLI_CSV_FILE)
    print "CCLI Required FACR songs:"
    for num, status in songs.iteritems():
        if not status.facr or status.ccli:
            continue
        print "%s: %s" % (num, status)
    print "Free to use FACR songs:"
    for num, status in songs.iteritems():
        if not status.facr or not status.ccli:
            continue
        print "%s: %s" % (num, status)

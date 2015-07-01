import os, glob

psalms = "5 6 13 25b 26 42 48 50 60 64 65 66 69 81b 86b 94 118b 144"   # note: removed 43 because it is on same pdf as 42
hymns = "178 199 296 304 328 368 387 472 485 511 518 521 522"

svnadd = True

def alter_pdf(infile):
    """ Make given pdf infile non-printable """
    outfile = infile.replace('.pdf', '.np.pdf')
    command = '''pdftk "%s" output "%s" owner_pw "hymnal" allow ModifyContents allow CopyContents allow ScreenReaders allow ModifyAnnotations''' % (infile, outfile)
    print command
    os.system(command)

    command = 'svn add "%s"' % outfile
    if not svnadd:
        print '#',
    print command
    if svnadd:
        os.system(command)

def find_files(numbers, path):
    """ Find files in path matching list of numbers and alter matching pdfs """
    for n in numbers:
        n, suffix, _dummy = n.partition('b')
        pattern = "{}{:0>3}{}_*.pdf".format(path, n, suffix)
        filenames = glob.glob(pattern)
        filenames = [f for f in filenames if not f.endswith('.np.pdf')]
        if len(filenames) > 1:
            raise Exception('''More than one filename found with pattern "{}": {}'''.format(pattern, filenames))
        if not filenames:
            raise Exception('''No file found to match pattern "{}"'''.format(pattern, filenames))
        alter_pdf(filenames[0])

def main():
    find_files(psalms.split(), 'Songs/PsalmsPDF/psalm')
    find_files(hymns.split(), 'Hymns/Hymn')

if __name__ == '__main__':
    main()

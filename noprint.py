import os, glob

files = "6 13 25b 26 42 43 48 50 52 60 64 65 66 69 81b 86b 94 118b 144 178 199 296 328 368 387 472 511 518 521 522"

def apply(infile):
    """ Make given pdf infile non-printable """
    outfile = infile.replace('.pdf', '.np.pdf')
    command = '''pdftk "%s" output "%s" owner_pw "hymnal" allow ModifyContents allow CopyContents allow ScreenReaders allow ModifyAnnotations''' % (infile, outfile)
    os.system(command)

def main():
    apply("Songs/Psalms and Hymns PDF/psalm006_LORD,_chasten_not_in_anger.pdf")

if __name__ == '__main__':
    main()

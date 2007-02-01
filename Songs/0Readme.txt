Notes on file naming scheme in this directory and the parts directory:

Files must be named according to this scheme for the automatic web-page generator to
work.

1. Files must be named "psalmXXX_This_is_the_Title.sib".  Note that all
spaces must be changed to underscores _.

2. If you want a song to be withheld, also make an empty file with a
matching name: "psalmXXX_This_is_the_Title.sib.withheld"

3. In order to actually appear on the public website, a .sib file must have a
matching name: "psalmXXX_This_is_the_Title.sib.proofed"

4. If no file is present for a particular Psalm, that Psalm nubmer will be
listed as "Coming".  If you'd like it to be listed as coming but with a
title, simply create an empty file called "psalmXXX_This_is_the_Title.sib.coming"

5. Each .sib file must have a matching "psalmXXX_This_is_the_Title.htm"
file that can be created with Berwyn's script "scorcher.py -q *.sib"

If you are technically inclined enough to be able to install python, you
can run the automatic web page generator from the parent directory.  It is
"python ListSongs.py" which takes the content of Header.htm and appends all
the songs, creating the hymns page file called start.htm

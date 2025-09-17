# File naming scheme in this directory

Files must be named according to this scheme for the automatic web-page generator to
work.

1. Files must be named `psalmXXX_This_is_the_Title.htm`.

  * Note that all spaces must be changed to underscores _. The filenames must not contain semicolons or web page links don't work right. Use commas instead.

  * There must be a matching `sib/psalmXXX_This_is_the_Title.sib` in the `sib` folder.
  * The `.htm` file can be created from the `.sib` file using the script in `../scorch/scorcher.py -q <filename>`

2. If you want a song to have words or music withheld from the website, make empty files with a matching name like:

  * `stats/psalmXXX_This_is_the_Title.sib.words_withheld`
  * `stats/psalmXXX_This_is_the_Title.sib.music_withheld`

3. In order to actually appear on the public website, a .sib file must have a matching name: `stats/psalmXXX_This_is_the_Title.sib.proofed`

4. If no file is present for a particular Psalm, that Psalm number will be listed as "Coming".  If you'd like it to be listed as coming but with a title, simply create an empty file called `stats/psalmXXX_This_is_the_Title.sib.coming`


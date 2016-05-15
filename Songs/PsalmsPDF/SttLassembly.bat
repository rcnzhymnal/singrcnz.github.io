rem Build SttL hymnal from pdfs

rem Temporarily get rid of 'non-publishable' (.np) files during assembly process
ren *.np.pdf *.tmp
ren ..\..\Hymns\*.np.pdf *.tmp

pause


call SttL-psalm-list
call java -cp * tool.pdf.Merge SttLfrontpages.pdf SubtitlePsalms.pdf blankpage.pdf %psalms% blankpage.pdf SubtitleHymn.pdf ..\..\Hymns\Hymn*.pdf SttLbackpages1.pdf Guitar.pdf SttLbackpages2.pdf
call java -cp * tool.pdf.Compress SttLfrontpages-m.pdf
del SttLfrontpages-m.pdf
move /y SttLfrontpages-m-o.pdf "SttL.pdf" && echo Created "SttL.pdf"

rem Restore 'non-publishable' (.np) files
ren *.np.tmp *.pdf
ren ..\..\Hymns\*.np.tmp *.pdf



pause

rem Build SttL hymnal from pdfs

call SttL-psalm-list
call java -cp * tool.pdf.Merge SttLfrontpages.pdf SubtitlePsalms.pdf blankpage.pdf %psalms% blankpage.pdf SubtitleHymn.pdf ..\..\Hymns\Hymn*.pdf SttLbackpages1.pdf Guitar.pdf SttLbackpages2.pdf
call java -cp * tool.pdf.Compress SttLfrontpages-m.pdf
del SttLfrontpages-m.pdf
move /y SttLfrontpages-m-o.pdf "SttL.pdf" && echo Created "SttL.pdf"
pause

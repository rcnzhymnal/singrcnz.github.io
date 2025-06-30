@echo off
rem Build SttL-provisional hymnal from pdfs

rem Temporarily get rid of 'non-publishable' (.np) file-flags during assembly process
ren *.np.pdf *.tmp

call SttL-psalm-list
call java -cp * tool.pdf.Merge Title.pdf Copyright.pdf Preface.pdf blankpage.pdf %psalms% Based_on_Psalms.pdf Copyright_Holders.pdf Index.pdf
call java -cp * tool.pdf.Compress Title-m.pdf

rem Restore (.np) file-flags
ren *.np.tmp *.pdf

del Title-m.pdf
move /y Title-m-o.pdf "SttL-provisional.pdf" && echo Created "SttL-provisional.pdf"

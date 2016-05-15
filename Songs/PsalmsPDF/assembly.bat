@echo off
rem Build SttL-provisional hymnal from pdfs

call SttL-psalm-list
call java -cp * tool.pdf.Merge Title.pdf Copyright.pdf Preface.pdf blankpage.pdf %psalms% Based_on_Psalms.pdf Copyright_Holders.pdf Index.pdf
call java -cp * tool.pdf.Compress Title-m.pdf

del Title-m.pdf
move /y Title-m-o.pdf "SttL-provisional.pdf" && echo Created "SttL-provisional.pdf"

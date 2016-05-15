@echo off
for %%f in (..\*.withheld) do call :rename1 "%%~nf"

rem Exclude Ps. 16 specifically because it has 16b on it
echo Renaming "psalm016_Protect_me,_O_my_God.pdf"
ren "psalm016_Protect_me,_O_my_God.pdf" "psalm016_Protect_me,_O_my_God.pdf.temp"

rem Temporarily get rid of 'non-publishable' (.np) files during assembly process
ren *.np.pdf *.tmp

call SttL-psalm-list
call java -cp * tool.pdf.Merge Title-web.pdf Copyright.pdf Preface.pdf blankpage.pdf %psalms% Based_on_Psalms.pdf Copyright_Holders.pdf Index.pdf
call java -cp * tool.pdf.Compress Title-web-m.pdf

rem Restore 'non-publishable' (.np) files
ren *.np.tmp *.pdf

echo Restoring "psalm016_Protect_me,_O_my_God.pdf"
ren "psalm016_Protect_me,_O_my_God.pdf.temp" "psalm016_Protect_me,_O_my_God.pdf"
for %%f in (..\*.withheld) do call :rename2 "%%~nf"

del Title-web-m.pdf
move /y Title-web-m-o.pdf "Sing to the Lord - provisional - web.pdf" && echo Created "Sing to the Lord - provisional - web.pdf"
goto :EOF

:rename1
  echo Renaming "%~n1.pdf"
  ren "%~n1.pdf" "%~n1.pdf.temp"
  goto :EOF

:rename2
  echo Restoring "%~n1.pdf"
  ren "%~n1.pdf.temp" "%~n1.pdf"
  goto :EOF

@echo off
rem make html files for .sib files given on command line (wildcards ok)
for %%i in (%*) do if exist %%i make-html %%i

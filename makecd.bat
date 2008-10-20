rem svn export . CD
rem xcopy /y "Z:\work\Archive\Sound\Notation\Scorch\Scorch CD installers" CD\ScorchInstallers\
rem xcopy /y "Z:\work\Hymnal\Publications\Interim\Sing to the Lord - provisional.pdf" CD
rmdir /s /q CD\Hymns
rmdir /s /q CD\scorch
cd CD
python website.py --cd
cd ..

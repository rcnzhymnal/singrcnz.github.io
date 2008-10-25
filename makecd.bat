svn export . CD
xcopy /y "Z:\work\Archive\Sound\Notation\Scorch\Scorch CD installers" CD\ScorchInstallers\
xcopy /y "Z:\work\Hymnal\Publications\Interim\Sing to the Lord - provisional.pdf" CD
xcopy /y "Z:\work\Archive\Application\PDF\foxit\FoxitReader23_setup.exe" CD
rmdir /s /q CD\Hymns
rmdir /s /q CD\scorch
cd CD
python ../website.py --cd
cd ..

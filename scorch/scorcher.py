# Python program to create html file for a sibelius file


# ~~~~ Program follows html data

html = """\xef\xbb\xbf<!-- saved from url=(0022)http://internet.e-mail -->
<html>
<head>
<title>    </title>
<meta
http-equiv="Content-Type" content="text/html;
charset=utf-8">
<style
type="text/css">
<!--
body {  background-color: #FFFFFF}
h1 {
font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 18pt;
font-style: normal; font-weight: bold; color: #CCFFFF}
h2 {
font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 14pt;
font-style: normal; font-weight: bold; color: #FFFFFF}
a:link {
color: #CC0000}
a:active {  color: #ffcc33}
a:visited {  color:
#cc6600}
td {  font-family: Verdana, Arial, Helvetica, sans-serif;
font-size: 10pt; font-style: normal; font-weight: normal; color:
#000000}
-->
</style>
</head>

<body>
<table  border="0"
cellspacing="0" cellpadding="0">
  <tr>
    <td width="12"
height="13">&nbsp;</td>
    <td width="2"
bgcolor="#FF9900">&nbsp;</td>
    <td width="16">&nbsp;</td>

<td>&nbsp;</td>
  </tr>
  <tr valign="middle">
    <td colspan=3
bgcolor="#003399">&nbsp; </td>
    <td bgcolor="#003399">

<table border="0" cellspacing="0" cellpadding="4">
        <tr>

<td>
            <h2>    </h2>
          </td>

</tr>
      </table>

    </td>
  </tr>
  <tr>

<td>&nbsp;</td>
    <td bgcolor="#FF9900">&nbsp;</td>

<td>&nbsp;</td>
    <td valign=top align=center width="15"> <br>
            <object id="ScorchPlugin"
                    classid="clsid:A8F2B9BD-A6A0-486A-9744-18920D898429"
                    width="604"
                    height="893"
                    codebase="http://www.sibelius.com/download/software/win/ActiveXPlugin.cab#3,0,0,4">
            <param name="src" value="%s">
            <param name="type" value="application/x-sibelius-score">
            <param name="scorch_minimum_version" value="3000">
            <param name="scorch_preferred_version" value="3000">
            <param name="scorch_shrink_limit" value="100">
            <param name="scorch_shrink_limit" value="100">
            <param name="SplitPlayBack" value="0">
            <param name="SplitView" value="0">
            <param name="SplitNumSystems" value="1">
            <embed src="%s"
                     scorch_minimum_version="3000"
                     scorch_preferred_version="3000"
                     scorch_shrink_limit="100"
                     width="604"
                     height="893"
                     type="application/x-sibelius-score"
                     pluginspage="http://www.sibelius.com/cgi/plugin.pl"
                     SplitView="0"
                     SplitNumSystems="1"
                     SplitPlayBack="0">
            </embed>
            </object>
        </td>

</tr>
  <tr valign="bottom" align="center">
    <td>&nbsp;</td>

<td bgcolor="#FF9900">&nbsp;</td>
    <td>&nbsp;</td>
    <td nowrap><br>
If you can't see the score or it says "The score did not load successfully",<br>
then <a href="http://www.sibelius.com/download/software/win/InstallScorch.exe">get
the Sibelius Scorch plug-in here</a>
or if that doesn't work, try <a href="http://www.sibelius.com/scorch/">here</a>.</td>

</tr>
</table>

</body>
</html>
"""


# ~~~~ Program

import sys
import os
import glob


def createHtml(sib, tempPath=''):
    if '.sib' in sib:
        htm = sib.replace('.sib', '.htm')
    else:
        htm = sib + '.htm'

    if tempPath:
        if tempPath[-1] != os.sep:
            tempPath += os.sep
        htm = tempPath + os.path.basename(htm)
        sib = 'file:///' + os.path.abspath(sib)
    else:
        sib = os.path.basename(sib)

    sib = sib.replace(';', '%3b')           # make filenames with semicolons work in Firefox
    data = html % (sib, sib)

    f = file(htm, 'w')
    print >>f, data
    f.close()
    return htm

def openHtml(htm):
    os.startfile(htm)

def main():
    if len(sys.argv)<2 or '-h' in sys.argv or '--help' in sys.argv or '/?' in sys.argv:
        print 'Usage: scorcher [-q] musicfile1.sib [musicfile2.sib] [*.sib]'
        print 'Generate .htm file to match sibelius .sib file'
        print "  -q means quiet: don't open the .htm files (creating them in the system's temp folder)"
        sys.exit(1)

    quiet = '-q' in sys.argv
    if quiet:
        del sys.argv[sys.argv.index('-q')]
    if not quiet:
        tempPath = os.getenv('TEMP', os.getenv('TMP', os.getenv('windir', '')))

    files = [j   for i in sys.argv[1:]   for j in glob.glob(i)]

    for i in files:
        if not quiet:
            print i,
            openHtml(createHtml(i, tempPath))
        else:
            print i, '->', createHtml(i)

if __name__ == '__main__':
    main()

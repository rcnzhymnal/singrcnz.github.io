#!/usr/bin/env python3

# (link, X)
link = """<a href="%s">%s</a>"""

# (link, clickme, SATB, typ, num, title, filelinks)
viewable = """<tr><td><a href="%s">%s</a></td><td>%s</td><td><b>%s %s</b>&nbsp;&nbsp;<i>%s</i></td><td>%s</td></tr>\n"""

hymntext = """<h1>Hymns</h1>
    <p>Below are playable or pdf versions of the Hymns.
    These also have certain <a href="Copyright.html">Copyright restrictions</a>.
    You <b>must</b> refer to these restrictions before reproducing copyrighted music or lyrics.
    </p>
    $update"""
psalmtext = """<h1>Psalms</h1>
    <p>Below are playable or pdf versions of the Psalms.
    These also have certain <a href="Copyright.html">Copyright restrictions</a>.
    You <b>must</b> refer to these restrictions before reproducing copyrighted music or lyrics.
    </p>"""

# (title, id, mainmenu, submenu)
header = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>

<head>
<title>RCNZ Psalter Hymnal: {title}</title>

<link rel="stylesheet" type="text/css" href="main.css" />
<body id="{id}"><div id="container">
<div id="header">
<div id="header-left"></div>

<div id="header-right"></div>
</div>

{mainmenu}

{submenu}
<div id="content" class="songlist">
"""

# ()
mainmenu = """<div id="mainMenu">
<div class="header">
<h3>Reformed Churches</h3>
</div>

<ul>
<li class="background1"><a href="Start.html">Hymnal homepage</a></li>
<li class="background1"><a href="Psalms.html">Browse psalms</a></li>
<li class="background1"><a href="Hymns.html">Browse hymns</a></li>
<li class="background1"><a href="Musicians.html">Musicians page</a></li>
<li class="background1"><a href="About.html">About the hymnal</a></li>
<li class="background1"><a href="Contacts.html">Contact</a></li>
</ul>

<ul>
<li class="background5"><a href="http://rcnz.org.nz">RCNZ Homepage</a></li>
<li class="background5"><a href="login.html">Committee Login</a></li>
</ul>

<ul>
<li class="background5"></li>

<li class="background5">
<div class="connector"></div>
</li>

</ul>

<div class="footer">
<div id="source-link">web development by<a target="_blank" href="http://brush.co.nz">Brush Technology</a></div>
</div>
</div>
"""
# ()
submenu = """<div id="subMenu">
<div class="corner TL"></div>
<div class="corner TR"></div>
<div class="corner BR"></div>
<div class="corner BL"></div>
<div class="connector"></div>
<div class="container"><a href="Psalms.html">Browse psalms</a><a href="Hymns.html">Browse hymns</a></div>
</div>
"""

# ()
footer = """</div>
</div></body>
</html>
"""

cdupdate = """
<p class='alert-message'>Updates of this page will be
<a href="http://hymnal.rcnz.org.nz/public/$page">available on the web here</a>.</p>
"""

cdheader = """
<h3>QuickStart</h3>
<p>You can view the entire contents of the printed book in several formats:<br />
<ul>
 <li><a href='Songs/Lyrics/Sing%20to%20the%20Lord%20-%20words%20only.doc'>MS-Word</a>
 | <a href='Songs/Lyrics/Sing%20to%20the%20Lord%20-%20words%20only.txt'>text</a>
 | <a href='Sing%20to%20the%20Lord%20-%20provisional.pdf'>PDF-score</a>
 (if needed, install this <a href='FoxitReader23_setup.exe'>PDF viewer</a>)</li>
 <li>Browse and play
  <font color='red'>
   (You&rsquo;ll need to install the &ldquo;Scorch&rdquo; software; choose your operating system:
   <a href="ScorchInstallers/Scorch521AllBrowsersInstaller.msi">Windows XP</a> |
   <a href="ScorchInstallers/SibeliusScorch521.dmg">Macintosh</a>).
  </font>
 </li>
</ul>
<hr />
"""

cdcopyright = """
<p>
 This CD contains the PDF (score) and text (lyrics) files of the whole printed book.
 It is important to note that copyright for these are tied up with the book and you may
 copy neither them nor this CD beyond the number of books that you own.</p>
"""

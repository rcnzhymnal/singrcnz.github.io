# Sing to the Lord Hymnal Website Maintenance

## Building the website

The website is built from templates called `*.tmpl.html`. The website `.html` files will need to be rebuilt when any of these templates changes or when a change is made to any of the song file names.

First you will need to install:

* Install [Python 3.5](https://www.python.org/downloads/) or newer
* Install [cpdf](https://community.coherentpdf.com/)
* Install [git](https://git-scm.com/downloads)

To rebuild the website, download the git repository and run the Python site builder script called `builder/site.py`:

```sh
git clone git@github.com:rcnzhymnal/singrcnz.github.io.git hymnal-public
cd hymnal-public
cd builder

# Now run the rebuilder script
python site.py
```

This will create or update the `.html` files and other files such as  `.np.pdf` files (which stands for the non-print versions of the pdf files where web pdf files many not be printed for copyright reasons).

## Building the PDF

For instructions on building the hymnal PDF for printing, see the hymnal committee's private repository in the folder [Publications/Final/README.md](https://github.com/rcnzhymnal/private/tree/master/Publications/Final/README.md).


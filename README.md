# Sing to the Lord Hymnal Website Maintenance

## Building the website

The website is built from templates called `*.tmpl.html`. The website `.html` files will need to be rebuilt when any of these templates changes or when a change is made to any of the song file names.

To rebuild the website, run the Python script called `builder/site.py`.

First you will need to install:

* Install [Python 3.5](https://www.python.org/downloads/) or newer
* Install [cpdf](https://community.coherentpdf.com/)

Then run python `builder/site.py`

## Building the PDF

For instructions on building the hymnal PDF for printing, see the hymnal committee's private repository in the folder [Publications/Final/README.md](https://github.com/rcnzhymnal/private/tree/master/Publications/Final/README.md).


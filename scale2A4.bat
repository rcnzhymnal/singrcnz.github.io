@rem Increase size of pdf page contents from hymnbook size to full A4 page size
cpdf -scale-contents 1.3 %1 -o %~dpn1-A4.pdf

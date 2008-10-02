# Script that creates setup.exe

import os

regfile = """REGEDIT4

[HKEY_CLASSES_ROOT\.sib]
@="Sibelius.Score"

[HKEY_CLASSES_ROOT\Sibelius.Score\shell]
@="Open"

[HKEY_CLASSES_ROOT\Sibelius.Score\shell\CreateHtm]

[HKEY_CLASSES_ROOT\Sibelius.Score\shell\CreateHtm\command]
@="\\\"%s\\\" -q \\\"%%L\\\""

[HKEY_CLASSES_ROOT\Sibelius.Score\shell\OpenWithScorch]

[HKEY_CLASSES_ROOT\Sibelius.Score\shell\OpenWithScorch\command]
@="\\\"%s\\\" \\\"%%L\\\""
"""

def createRegfile():
    """Create registry file"""

    filename = 'scorcher.reg'

    path = os.getcwd()
    if not path.endswith('\\'):
        path += '\\'
    path = path.replace('\\', '\\\\')

    exename = path+'scorcher.exe'
    if os.path.exists('scorcher.py'):
        exename = 'c:\\\\python25\\\\python.exe\\\" \\\"'+path+'scorcher.py'

    f = file(filename, 'w')
    f.write(regfile % (exename, exename))
    f.close()

    return filename

def updateReg():
    filename = createRegfile()
    os.system ('regedit.exe /s %s' % filename)

def main():
    updateReg()
    print 'Setup complete.'
    print
    print 'Now you can create .htm files by right-clicking on a .sib file and selecting CreateHtm'
    print 'or you can open .sib files directly with Scorch by selecting OpenWithScorch'
    print
    print 'Press <Enter>'
    raw_input()


if __name__ == '__main__':
    main()

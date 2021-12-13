'''Small scripts to check for files and folders'''

import codecs
import datetime
import os


def is_folder_writable(folder):
    '''Function to check if folder is writable'''
    tmppath = folder+'/.tstfile.' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.tmp'
    try:
        with codecs.open(tmppath, 'w', 'utf-8') as tmpfile:
            tmpfile.write('Testcontent')
    except PermissionError:
        return False

    if os.path.exists(tmppath):
        os.remove(tmppath)

    return True

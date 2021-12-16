'''Small scripts to check for files and folders'''

import codecs
import datetime
import os


def is_folder_writable(folder):
    '''Check if folder is writable'''
    tmppath = folder+'/.tstfile.' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.tmp'
    try:
        with codecs.open(tmppath, 'w', 'utf-8') as tmpfile:
            tmpfile.write('Testcontent')
    except PermissionError:
        return False

    if os.path.exists(tmppath):
        os.remove(tmppath)

    return True


def folder_exists(folder):
    '''Check if a folder exists'''
    if os.path.isdir(folder):
        return True
    return False


def file_exists(file):
    '''Check if a file exists'''
    if os.path.isfile(file):
        return True
    return False

def is_file_writable(file):
    '''Check if file can be opened for writing'''
    try:
        testfile = codecs.open(file, 'a', 'utf-8')
        testfile.close()
    except PermissionError:
        return False

    return True

def get_files_folder(file):
    '''Return a (full path) folder of given file'''
    fullname = os.path.realpath(file)
    return os.path.dirname(fullname)

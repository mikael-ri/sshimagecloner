'''Module to validate the sshimagecloner inputs etc.'''

import os
import re


class ValidatorResult:
    '''A validator result object that implements bool and contains error message'''
    def __init__(self, result, value, message):
        self.result = result
        self.value = value
        self.message = message

    def __repr__(self):
        if self.result:
            return str(self.result) + ' ' + str(self.value)
        else:
            return str(self.result) + ' ' + self.message

    def __bool__(self):
        return self.result

def backup_name(name):
    '''Validate backup name'''
    pat = re.compile(r'^[a-zA-Z0-9]{1}[-\w\.]{0,18}[-\w]$')

    msg = 'Backup name max length is 20 char, it must start with alphanumeric character, ' \
        'and can only contain a-z A-Z 0-9 . - _ and cannot end with .'

    return ValidatorResult(bool(pat.match(name)), name, msg)


def file_read(file):
    '''Check that file exists and is readable.

    Arguments:
    file -- Path object representing the file
    '''
    value = file
    message = ''
    if file.is_file():
        if os.access(file, os.R_OK):
            result = True
        else:
            message = 'File ' + str(file) + ' cannot be read, no access'
            result = False
    else:
        message = 'File ' + str(file) + ' does not exist'
        result = False

    return ValidatorResult(result, value, message)

def file_write(file):
    '''Check that file exists and is writable.

    Arguments:
    file -- Path object represeting the file
    '''
    value = file
    message = ''
    if file.is_file():
        if os.access(file, os.W_OK):
            result = True
        else:
            message = 'File ' + str(file) + ' does not have write permission'
            result = False
    else:
        message = 'File ' + str(file) + ' does not exist'
        result = False

    return ValidatorResult(result, value, message)

def folder_write(folder):
    '''Check that folder exists and is writable

    Arguments:
    folder -- Path object representing the folder
    '''
    value = folder
    message = ''
    if folder.is_dir():
        if os.access(folder, os.W_OK):
            result = True
        else:
            message = 'Folder ' + str(folder) + ' does not have write permission'
            result = False
    else:
        message = 'Folder ' + str(folder) + ' does not exist'
        result = False

    return ValidatorResult(result, value, message)

def log_file(file):
    '''Check that either log file exists and is writable, or the folder for log file is writable

    Arguments:
    file -- Path object represeting the log file
    '''
    value = file
    message = ''
    if file.is_file():
        if os.access(file, os.W_OK):
            result = True
        else:
            message = 'File ' + str(file) + ' exists but does not have write permissions'
            result = False
    else:
        log_dir = os.path.dirname(file)
        if os.path.isdir(log_dir):
            if os.access(log_dir, os.W_OK):
                result = True
            else:
                message = 'Folder ' + str(log_dir) + ' does not have write permission'
                result = False
        else:
            message = 'Folder ' + str(log_dir) + ' does not exist'
            result = False

    return ValidatorResult(result, value, message)

def log_level(level):
    '''Check if the log level is valid value'''
    result = False
    if level >= 0 and level <= 2:
        result = True

    msg = 'Log level must be a number 0, 1 or 2'

    return ValidatorResult(result, level, msg)

def versions(vers):
    '''Check that versions is a valid number'''
    result = False

    if vers > 0:
        result = True

    msg = 'Version amount must be a positive integer number'

    return ValidatorResult(result, vers, msg)

def remote_login(name):
    '''Check the validity of username'''
    pat = re.compile(r'^[a-z_]([a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$')

    msg = 'remote_login name must comply with linux username naming, ' \
        r'regex: ^[a-z_]([a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$'

    return ValidatorResult(bool(pat.match(name)), name, msg)

def ip_address_or_host(str_in):
    '''Check that input is valid IP-address'''
    pat_ip = re.compile(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
        r'([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')

    pat_hn = re.compile(r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*'
        r'([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$')

    msg = 'Input must either be a valid IP-address between 0.0.0.0 and 255.255.255.255' \
        ' or RFC 1123 compliant hostname'

    result = False

    if pat_ip.match(str_in) or pat_hn.match(str_in):
        result = True

    return ValidatorResult(result, str_in, msg)

def target_file(name):
    '''Validate target_file name'''
    pat = re.compile(r'^[a-zA-Z0-9]{1}[-\w\.]{0,28}[-\w]$')

    msg = 'Target file name max length is 30 char, it must start with alphanumeric character, ' \
        'and can only contain a-z A-Z 0-9 . - _ and cannot end with .'

    return ValidatorResult(bool(pat.match(name)), name, msg)

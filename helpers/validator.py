'''Module to validate the sshimagecloner inputs etc.'''

import re

class ValidatorResult():
    '''A validator result object that implements bool and contains error message'''
    def __init__(self, result, message):
        self.result = result
        self.message = message

    def __repr__(self):
        if self.result:
            return str(self.result)
        else:
            return str(self.result) + ' ' + self.message

    def __bool__(self):
        return self.result


def backup_name(str_in):
    '''Validate backup name'''
    pat = re.compile(r'^[a-zA-Z0-9]{1}(\w|-|\.){0,19}$')

    msg = 'Backup name max length is 20 char, it must start with alphanumeric character, ' \
        'and can only contain a-z A-Z 0-9 . - _ '

    return ValidatorResult(bool(pat.match(str_in)), msg)

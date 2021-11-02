'''This module writes a log to a specified file in a certain format.'''

import datetime
import codecs
import math
from contextlib import contextmanager

class Logger:
    '''Class for Logger, to write a log file.'''
    # constants for a log, can be changed as per preference
    _ROWLENGTH = 100
    _WHITE_SPACES = 5
    _TYPES = {'N':'', 'I':'[INFO] ', 'E':'[ERROR] ', 'D':'[DEBUG] '}
    verbose = False

    def __init__(self, path, verb):
        # path to the logfile
        self.logfilepath = path
        # length of the indentation of log rows (including timestamp)
        self.indentlen = len(datetime.datetime.now().strftime('%H:%M:%S')) + self._WHITE_SPACES
        # set verbose, if so, all is also printed in stdout.
        self.verbose = verb
        # logfile variable
        self.logfile = None


    def open(self):
        '''Function to open the log file for appending text'''
        self.logfile = codecs.open(self.logfilepath, 'a', 'utf-8')

    @contextmanager
    def log_writer(self):
        '''Log writer to return the object to be used with "with" statement'''
        # open the log file and return for writing.
        try:
            self.open()
            yield self
        finally:
            self.close()


    # Method to start logging, opens the file for append and writes the startrow
    def write_starting_row(self, message):
        '''Method to start the log, writes the first row including datetime.'''
        # create specific startrow for this log instance
        startrow = '-' * self._ROWLENGTH + '\n'
        midtext = ' New log started at '
        midtext += datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        padlength = self._ROWLENGTH - len(midtext)
        text = '-' * math.floor(padlength / 2)
        text += midtext

        if padlength % 2 == 0:
            text += '-' * (math.floor(padlength / 2)) + '\n'
        else:
            text += '-' * (math.floor(padlength / 2) + 1) + '\n'

        self.logfile.write(startrow)
        self.logfile.write(text)
        self.write_log(message)
        self.logfile.flush()
        if self.verbose:
            print(startrow + text + message)

    # Method to write messages to log, messages will be splitted to certain length
    def write_log(self, message, msgtype = 'N'):
        '''Write an entry to the log file.'''
        logtext = self.format_lines(self._TYPES[msgtype] + message, self._ROWLENGTH)
        self.logfile.write(logtext)
        self.logfile.flush()
        if self.verbose:
            print(logtext)

    # Method to write given line to log with the indent to match normal rows
    def write_line_with_indent(self, message, msgtype = 'N'):
        '''Write a raw line to log with intendation, without text wrapping'''
        msg = ' ' * self.indentlen + self._TYPES[msgtype] + message
        self.logfile.write(msg)
        self .logfile.flush()
        if self.verbose:
            print(msg)

    # Method to write unformatted text to log, mainly error messages
    def write_line_unformatted(self, message):
        '''Write a raw line to log as passed to the function'''
        self.logfile.write(message)
        self.logfile.flush()
        if self.verbose:
            print(message)

    # Method to split lines to given length, splits the message from last whitespace
    # (' ' to be specific) or, if there is no whitespace, then just cuts the text at length
    # also adds timestamp in the beginning of each message, and inserts sufficient indentation
    def format_lines(self, text, length):
        '''Format the input to match the row length and intendation'''
        textlen = length - self.indentlen
        if len(text) <= textlen:
            return datetime.datetime.now().strftime('%H:%M:%S') \
                + ' ' * self._WHITE_SPACES + text + '\n'

        firstline = datetime.datetime.now().strftime('%H:%M:%S') + ' ' * self._WHITE_SPACES
        firstlineset = False
        returntext = ''
        proctext = text
        splitindex = 0
        while len(proctext) > textlen:
            if proctext[:textlen].rfind(' ') == -1 or proctext[:textlen].rfind(' ') == 0:
                splitindex = textlen
            else:
                splitindex = proctext[:textlen].rfind(' ')

            if not firstlineset:
                firstline += proctext[:splitindex] + '\n'
                firstlineset = True
            else:
                returntext += '             ' \
                    + proctext[1 if proctext[:1] == ' ' else 0:splitindex] + '\n'

            proctext = proctext[splitindex:]

        returntext += ' ' * self.indentlen + proctext[1 if proctext[:1] == ' ' else 0:] + '\n'
        return firstline + returntext

    # closes the logfile
    def close(self):
        '''Close the log file and flush the contents.'''
        self.logfile.flush()
        self.logfile.close()

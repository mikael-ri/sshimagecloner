#!/usr/bin/python3
'''ssh image cloner, to clone images from remote host over ssh'''

###############################################################################
##                             ssh image cloner                              ##
##                                                                           ##
## Python program to clone images from remote host over ssh                  ##
## Author: mikali-ri                                                         ##
## Created: 2021-11-01                                                       ##
## License: GNU General Public License v3                                    ##
##                                                                           ##
###############################################################################


###############################################################################
## Imports                                                                   ##
###############################################################################
import os
import sys
import datetime
import getopt
import collections
import subprocess
import shlex
import yaml
from yaml.scanner import ScannerError



###############################################################################
## Own modules                                                               ##
###############################################################################
import logger


###############################################################################
## My own custom classes                                                     ##
###############################################################################

#------------------------------------------------------------------------------
# Class for writing the logs, this handles the log levels etc.
#------------------------------------------------------------------------------
class LogWriter:
    '''A simple class to handle the verbosity and log writing'''

    def __init__(self, log_object, level, written):
        self.log = log_object
        self.log_level = level
        self.is_log_written = written
        if self.is_log_written:
            with self.log.log_writer() as log_obj:
                log_obj.write_starting_row('Logging initiated, log level set to ' \
                     + str(self.log_level))


    def write(self, message, msgtype = 'N'):
        '''write a message to the log according to level etc.'''
        # if write_log is not set to True, do nothing.
        if not self.is_log_written:
            return

        if msgtype == 'E':
            with self.log.log_writer() as log_obj:
                log_obj.write_log(message, msgtype)
        elif msgtype == 'D' and self.log_level >= 2:
            with self.log.log_writer() as log_obj:
                log_obj.write_log(message, msgtype)
        elif msgtype == 'I' and self.log_level >= 1:
            with self.log.log_writer() as log_obj:
                log_obj.write_log(message, msgtype)
        elif msgtype == 'N':
            with self.log.log_writer() as log_obj:
                log_obj.write_log(message, msgtype)

        return


###############################################################################
## Constants                                                                 ##
###############################################################################

# config file is expected to be in the working directory
CONFIG_FILE_PATH = './sshimagecloner.yaml'


###############################################################################
## Main executable code                                                      ##
###############################################################################

def main(args):
    '''Main function to execute the code'''

    e_cnt = 0
    e_msg = ""

    # Parse the arguments, if any
    e_cnt, e_msg, cmd_args = parse_cmd_arguments(args)

    # End execution if errors in parsing arguments
    if e_cnt > 0:
        print(e_msg)
        return

    # Read and parse the configuration file
    if cmd_args.conf_file is None:
        e_cnt, e_msg, conf, all_backups = parse_config_file(CONFIG_FILE_PATH)
    else:
        e_cnt, e_msg, conf, all_backups = parse_config_file(cmd_args.conf_file)

    # End execution if errors in parsing config file
    if e_cnt > 0:
        print('Errors in parsing the configuration file:\n')
        print(e_msg)
        return

    # If run as configtest, end process here
    if cmd_args.configtest:
        print('Config file content seems to be OK!')
        return

    # Set up logging
    log = logger.Logger(conf.log_file, cmd_args.verbose)
    my_log = LogWriter(log, conf.log_level, conf.is_log_written)

    my_log.write('All arguments and parameters parsed successfully, found ' \
        + str(len(all_backups)) + ' backups')

    my_log.write('Command line arguments are:', 'D')
    my_log.write(str(cmd_args), 'D')
    my_log.write('Configuration parameters are:', 'D')
    my_log.write(str(conf), 'D')
    my_log.write('Backups and parameters are:', 'D')
    my_log.write(str(all_backups), 'D')


    # Actual execution starts from here
    my_log.write('Start to execute backups', 'D')

    # Compare the command line arguments with config file backups
    backups_to_process = {}
    if len(cmd_args.cmd_backups) > 0:
        e_cnt, e_msg, backups_to_process = select_for_processing(cmd_args.cmd_backups, all_backups)
    else:
        backups_to_process = all_backups

    if e_cnt > 0:
        my_log.write(e_msg, 'E')
        print(e_msg)
        return

    # If target_folder is given from command line, then replace it for all backups to be processed
    if cmd_args.target_folder is not None:
        backups_to_process = replace_target_folder(backups_to_process, cmd_args.target_folder)

    # Process through the selected backups
    for key in backups_to_process:
        # Check if the backup-specific folder exists, if not create
        e_cnt, e_msg, path = prepare_path(conf.root_folder, backups_to_process[key].target_folder)
        if  e_cnt > 0:
            my_log.write(e_msg, 'E')
            print(e_msg)
            return
        # Run the backup
        e_cnt, e_msg = run_backup(backups_to_process[key], path, my_log)
        if e_cnt > 0:
            my_log.write(e_msg, 'E')
            print(e_msg)
            return

    # End of def main(args)



#------------------------------------------------------------------------------
# Methof to parse the command line arguments passed
#------------------------------------------------------------------------------

# Parse command line arguments
def parse_cmd_arguments(arg):
    '''Parse command line arguments and return them as namedtuple'''

    usage = 'Usage: sshimagecloner.py [-h | --help] [-v] ' '[-c | --conffile configfile] \n' \
        + '[-f | --folder folder] [backupname_1] [backupname_2] [backupname...n]'

    err_count = 0
    msg = ''

    # Try to read the options and arguments from command line input
    try:
        opts, args = getopt.getopt(arg, 'hc:f:v', ['help', 'conffile=', 'folder='])
    except getopt.GetoptError:
        err_count += 1
        msg += '[ERROR] Could not parse command line options, possibly unrecognized option\n'
        msg += usage
        return err_count, msg, None

    # Process the options given.
    conf_file = None
    target_folder = None
    verbose = False
    for opt, val in opts:
        if opt == '-v':
            verbose = True
        elif opt in ('-h', '--help'):
            err_count +=1
            msg += usage
        elif opt in ('-c', '--conffile'):
            conf_file = val
        elif opt in ('-f', '--folder'):
            target_folder = val
        else:
            print(opt + ' XX ' + val)
            err_count += 1
            msg += 'Unrecognized option'

    # Process the arguments given.
    configtest = False
    cmd_backups = {}
    for val in args:
        if val == 'configtest':
            configtest = True
        else:
            cmd_backups[val] = val

    Arguments = collections.namedtuple('Arguments',
    ['conf_file', 'target_folder', 'verbose', 'configtest', 'cmd_backups'])
    arguments = Arguments(conf_file, target_folder, verbose, configtest, cmd_backups)
    return err_count, msg, arguments

    # End of def parse_cmd_arguments(arg)


#------------------------------------------------------------------------------
# Method to parse the configuration file
#------------------------------------------------------------------------------

# Parse the configuration file to namedtuples
def parse_config_file(path):
    '''Parse config file and return Configuration namedtuple object and backups -list'''
    msg = ''
    err_count = 0

    yaml_conf = {}

    if not os.path.exists(path):
        err_count += 1
        msg += '[ERROR] config file: ' + path + ' does not exist!\n'
    else:
        config_file = open(path)
        try:
            yaml_conf = yaml.load(config_file, Loader=yaml.FullLoader)
        except ScannerError:
            err_count += 1
            msg += '[ERROR] configuration file could not be read in, check syntax\n'


    # FIRST PARSE THE GENERAL CONFIGURATION
    general_config = {}
    if 'general' in yaml_conf:
        general_config = yaml_conf['general']
    else:
        err_count += 1
        msg += '[ERROR] general -section is missing from config file\n'


    # Log file path
    log_file = None
    # Default log level is the minimum
    log_level = 0
    # Default logging is totally off
    is_log_written = False
    # Root folder where the backups are stored, needs to be set
    root_folder = None
    # Default folder naming
    folder_naming = 'backupdir'
    # Default amount of versions is 2
    versions = 2

    #Check through all the parameters needed.
    if 'log_file' in general_config:
        log_file = general_config['log_file']
        is_log_written = True

    if 'log_level' in general_config:
        log_level = general_config['log_level']

    if 'backup_root_folder' in general_config:
        if not os.path.exists(general_config['backup_root_folder']):
            err_count += 1
            msg += '[ERROR] backup_root_folder does not exist\n'
        root_folder = general_config['backup_root_folder']
    else:
        err_count += 1
        msg += '[ERROR] Parameter backup_root_folder not set in config file\n'

    if 'folder_naming' in general_config:
        folder_naming = general_config['folder_naming']

    if 'versions' in general_config:
        versions = general_config['versions']

    Configuration = collections.namedtuple('Config',
    ['log_file', 'log_level', 'is_log_written', 'root_folder', 'folder_naming', 'versions'])

    conf = Configuration(log_file, log_level, is_log_written, root_folder, folder_naming, versions)


    # THEN PARSE THE BACKUP DETAILS
    backup_config = {}
    if 'backups' in yaml_conf:
        backup_config = yaml_conf['backups']
    else:
        err_count += 1
        msg += '[ERROR] backups -section is missing from config file\n'


    if len(backup_config) == 0:
        err_count += 1
        msg += '[ERROR] No backups specified in config file\n'

    all_backups = {}
    Backup = collections.namedtuple('Backup',
    ['name', 'remote_login', 'remote_host', 'remote_file',
    'target_file', 'target_folder', 'block_size'])

    for key in backup_config:
        try:
            r_l = backup_config[key]['remote_login']
        except KeyError:
            r_l = ''
            err_count += 1
            msg += '[ERROR] remote_login not specified for backup: ' + key + '\n'
        try:
            r_h = backup_config[key]['remote_host']
        except KeyError:
            r_h = ''
            err_count += 1
            msg += '[ERROR] remote_host not specified for backup: ' + key + '\n'
        try:
            r_f = backup_config[key]['remote_file']
        except KeyError:
            r_f = ''
            err_count += 1
            msg += '[ERROR] remote_file not specified for backup: ' + key + '\n'
        try:
            t_f = backup_config[key]['target_file']
        except KeyError:
            t_f = ''
            err_count += 1
            msg += '[ERROR] target_file not specified for backup: ' + key + '\n'
        try:
            b_s = backup_config[key]['block_size']
        except KeyError:
            b_s = ''
            err_count += 1
            msg += '[ERROR] block_size not specified for backup: ' + key + '\n'

        all_backups[key] = Backup(key, r_l, r_h, r_f, t_f, key, b_s)


    return err_count, msg, conf, all_backups
    # End of def parse_config_file(path)


# Method to select backups to be processed
def select_for_processing(cmdback, allback):
    '''Function to select the backups to be processed based on cmdline arguments.'''
    err_count = 0
    msg = ""
    backups_to_process = {}
    for key in cmdback:
        if key in allback.keys():
            backups_to_process[key] = allback[key]
        else:
            err_count += 1
            msg += 'Backup: ' + key + ' not found from config file, aborting\n'

    return err_count, msg, backups_to_process
    # Enf of def select_for_processing(cmdback, allback)


def replace_target_folder(backups, folder):
    '''Function to replace the target folder'''

    for key in backups:
        backups[key] = backups[key]._replace(target_folder = folder)

    return backups
    # End of def replace_target_folder(backups, folder)


def prepare_path(root_path, folder):
    '''Function to return the full backup path, and create if it does not exist'''
    err_count = 0
    msg = ""

    backup_folder = root_path + folder

    if os.path.isdir(backup_folder):
        return err_count, msg, backup_folder
    else:
        if os.path.exists(backup_folder):
            err_count += 1
            msg += 'Backup path ' + backup_folder + ' already exists, but is not a directory'
            return err_count, msg, ''
        else:
            try:
                os.makedirs(backup_folder)
            except PermissionError:
                err_count += 1
                msg += 'Cannot create folder: ' + backup_folder + ', no access rights'
                return err_count, msg, ''

    return err_count, msg, backup_folder

    # End of def prepare_path(backup)


# Method to run one backup
def run_backup(backup, path, log):
    '''Function to process one backup.'''
    err_count = 0
    msg = ""

    log.write('Starting to process ' + backup.name + ' : ' + backup.remote_file)

    # Construct the "reading" part of the dd + gzip command
    readcmd = '/usr/bin/ssh ' + backup.remote_login + '@' + backup.remote_host \
        + ' "usr/bin/sudo /usr/bin/dd if='+ backup.remote_file + ' bs=' + backup.block_size \
        + ' | /usr/bin/gzip -1 -"'

    log.write(backup.name + ' read command:', 'D')
    log.write(readcmd, 'D')

    # Create the target filename, full path. ._tmp -extension is used during the write
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_')
    target_file = path + '/' + timestamp + backup.target_file
    target_file_tmp = path + '/' + timestamp + backup.target_file + '._tmp'

    # Construct the write part of overall dd-command.
    writecmd = '/usr/bin/dd of=' + target_file_tmp + ' bs=' + backup.block_size

    log.write(backup.name + ' write command:', 'D')
    log.write(writecmd, 'D')

    # Split the command line options / process commands for subprocess.Popen command
    readsplit = shlex.split(readcmd)
    writesplit = shlex.split(writecmd)

    readproc = None
    writeproc = None

    try:
        # Start the process providing the read stream
        readproc = subprocess.Popen(readsplit,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

        # Pipe the read streams output to write streams input
        writeproc = subprocess.Popen(writesplit,
        stdin=readproc.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

        # Wait until the writing process finishes, and flush everything.
        writeproc.wait()
        writeproc.stdout.flush()
    except OSError:
        err_count += 1
        msg += 'Something went wrong with the read and write processes'
        return err_count, msg

    # Rename the target file to standard name.
    log.write('Renaming ' + target_file_tmp + ' to ' + target_file, 'D')
    os.rename(target_file_tmp, target_file)

    linestoprint = readproc.stderr.readlines() + writeproc.stderr.readlines()

    log.write(backup.name + ' : ' + backup.remote_file + ' successfully')
    log.write('backed up as ' + target_file)
    log.write('with following dd statistics', 'D')
    for line in linestoprint:
        log.write(line.decode('utf-8'), 'D')


    return err_count, msg

    # End of def run_backup(backup):



# Run the main function
if __name__ == "__main__":
    main(sys.argv[1:])

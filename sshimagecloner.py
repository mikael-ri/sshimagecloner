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
import getopt
import collections
import yaml
from yaml.scanner import ScannerError



###############################################################################
## Own modules                                                               ##
###############################################################################
import logger


###############################################################################
## Custom definitions                                                        ##
###############################################################################

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

    # Parse the arguments, if any
    err_count, err_msg, cmd_args = parse_cmd_arguments(args)

    if err_count > 0:
        print(err_msg)
        return

    # Read and parse the configuration file
    if len(cmd_args.conf_file) > 0:
        err_count, err_msg, conf, backups = parse_config_file(cmd_args.conf_file)
    else:
        err_count, err_msg, conf, backups = parse_config_file(CONFIG_FILE_PATH)

    if err_count > 0:
        print('Errors in parsing the configuration file:\n')
        print(err_msg)
        return

    if cmd_args.configtest:
        print('Config file content seems to be OK!')
        return

    # Set up logging
    log = logger.Logger(conf.log_file, cmd_args.verbose)
    my_log = LogWriter(log, conf.log_level, conf.is_log_written)

    my_log.write('All arguments and parameters parsed successfully, found ' \
        + str(len(backups)) + ' backups')

    my_log.write('Command line arguments are:', 'D')
    my_log.write(str(cmd_args), 'D')
    my_log.write('Configuration parameters are:', 'D')
    my_log.write(str(conf), 'D')
    my_log.write('Backups and parameters are:', 'D')
    my_log.write(str(backups), 'D')


    # Actual execution starts from here
    my_log.write('Start to execute backups', 'D')

    # Implement this..



    # End of def main(args)


# Parse command line arguments
def parse_cmd_arguments(arg):
    '''Parse command line arguments and return them as namedtuple'''

    usage = 'Usage: sshimagecloner.py [-h | --help] [-v] ' \
        '[-c | --conffile configfileame] [backupname_1] [backupname_2] [backupname...n]'

    err_count = 0
    msg = ''
    try:
        opts, args = getopt.getopt(arg, 'hc:v', ['help', 'conffile='])
    except getopt.GetoptError:
        err_count += 1
        msg += '[ERROR] Could not parse command line options, possibly unrecognized option\n'
        msg += usage
        return err_count, msg, None

    #print(opts)
    #print('perse')
    #print(args)

    conf_file = None
    verbose = False
    for opt, val in opts:
        if opt == '-v':
            verbose = True
        elif opt in ('-h', '--help'):
            err_count +=1
            msg += usage
        elif opt in ('-c', '--conffile'):
            conf_file = val
        else:
            print(opt + ' XX ' + val)
            err_count += 1
            msg += 'Unrecognized option'

    configtest = False
    cmd_backups = {}
    for val in args:
        if val == 'configtest':
            configtest = True
        else:
            cmd_backups[val] = val

    Arguments = collections.namedtuple('Arguments',
    ['conf_file', 'verbose', 'configtest', 'cmd_backups'])
    arguments = Arguments(conf_file, verbose, configtest, cmd_backups)
    return err_count, msg, arguments

    # End of def parse_cmd_arguments(arg)


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

    backups = {}
    Backup = collections.namedtuple('Backup',
    ['remote_login', 'remote_host', 'remote_file', 'target_file', 'block_size'])

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

            backups[key] = Backup(r_l, r_h, r_f, t_f, b_s)


    return err_count, msg, conf, backups
    # End of def parse_config_file(path)

# Run the main function
if __name__ == "__main__":
    main(sys.argv[1:])

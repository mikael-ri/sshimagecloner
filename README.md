# sshimagecloner
A tool to backup disk images from remote server to local hard drive

## About the project

I started to create this tool to solve the problem of possible sd-card failure (or any other situation of breaking the card / image /installation) of an Raspberry Pi computer, so that I could restore the most recent state to a new sd-card. As I usually don't remember to take the backups manually, I needed to create an automatic solution.

Also, I needed the backup to be done over the network, and while the pi is running.

As there probably exists a lot of good and great tools to accomplish this, this project also serves as a learning / testing project for python. For this reason, the code most likely is not most optimal, as some things are done in certain way just for trying out something, or for the fun of it..

I'm using [rsnapshot](https://rsnapshot.org/) for file backup on the linux virtual machines and Raspberry Pi's, and I can warmly recommend that tool! Certain influences can be seen on the functionality of this tool as well.

## Installation

Easiest way to install the application is to download the `install_imagecloner.sh` -script, make it executable and run it
```bash
wget https://raw.githubusercontent.com/mikael-ri/sshimagecloner/main/auto_install/install_imagecloner.sh
chmod +x install_imagecloner.sh
sudo ./install_imagecloner.sh
```

This script install pre-requisites, clones the repo, moves the files to right folders and then removes the clone

Of course the application can be just clomed from the repo
```bash
git clone https://github.com/mikael-ri/sshimagecloner
```
and then just put either move the config-file to correct folder, give it as command line parameter or change the constant variable `CONFIG_FILE_NAME` to a new value where the script should look for the config file.

## Usage

sshimagecloner has the following command line options and arguments
```
OPTIONS:
-h, --help
        Prints the usage -message for variables

-t, --test
        Does a "test run", i.e. prints out to stdout all commands that it would run but does not
        do any changes

-v
        Verbose mode, prints the same to stdout what is also printed in the log. Level of verbosity
        is defined with log_level in the config file

-c, --conffile CONFIG_FILE
        Takes the config file as parameter and overruns the config file stated in the script

-f, --folder FOLDER
        Uses this folder for backups for this run. The folder must be relative to the
        backup_root_folder set in the config file, it cannot be absolute path. If the folder is
        given as an argument, old versions are not deleted from this folder. This folder must
        exist, and when the backups are running, a subfolder is created for each backup.

ARGUMENTS:
configtest
        Tests the config file contents and passed arguments and then stops. Does not do any
        changes.

backupname_1 backupname_2 backupname...n
        A list of backupnames can be provided, and only these are run. If the -f option is not
        specified, then also the old versions are deleted if the amount exceed the versions
        specified in the config file. These names must match to the backup names declared in the
        config file.

```
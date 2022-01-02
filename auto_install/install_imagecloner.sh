#!/usr/bin/env bash

# -e option tells bash to exit if any command has a non-zero exit status
set -e

# Set variables for the script
SSHIMAGECLONER_TMP_DIR="/tmp/sshimageclonertmp"
SSHIMAGECLONER_EXECUTABLE_FILE="/usr/local/bin/sshimagecloner"
SSHIMAGECLONER_CONFIG_DIR="/etc/sshimagecloner"
SSHIMAGECLONER_CONFIG_FILE="/etc/sshimagecloner/sshimagecloner.yaml"
SSHIMAGECLONER_LOGROTATE_FILE="/etc/logrotate.d/sshimagecloner"


printf "Running apt update and installing python3, pip and git\n"
sudo apt update
sudo apt install python3 python3-pip git -y

# Create temp directory, and change working directory there
printf "Creating a temporary directory where to clone the git repo\n"
[ ! -d $SSHIMAGECLONER_TMP_DIR ] && sudo mkdir $SSHIMAGECLONER_TMP_DIR
pushd $SSHIMAGECLONER_TMP_DIR

printf "Figuring out the module directory"
SSHIMAGECLONER_PYTHON_MODULE_DIR=$(python3 -m site | egrep /usr/local/lib/python*/dist-packages | sed -e "s/,$//" -e "s/'//g")

# Clone the git repository to temp directory
printf "Cloning the git repo to temp directory\n"
sudo git clone https://github.com/mikael-ri/sshimagecloner

printf "Installing required python modules\n"
sudo pip install -r sshimagecloner/auto_install/requirements.txt

# Create config directory, and move the config file there
printf "Creating directory for configuration file\n"
[ ! -d $SSHIMAGECLONER_CONFIG_DIR ] && sudo mkdir $SSHIMAGECLONER_CONFIG_DIR
sudo cp sshimagecloner/auto_install/sshimagecloner_example.yaml $SSHIMAGECLONER_CONFIG_FILE

# Copy the logrotate file
printf "Installing the logrotate file\n"
sudo cp sshimagecloner/auto_install/logrotate.d/sshimagecloner $SSHIMAGECLONER_LOGROTATE_FILE

# Copy the dependent module to the module directory
printf "Copying own modules to correct folder\n"
sudo cp -R sshimagecloner/sic_helpers $SSHIMAGECLONER_PYTHON_MODULE_DIR

# Copy the main script and make sure it is executable
printf "Copying the executable to correct folder\n"
sudo cp sshimagecloner/sshimagecloner $SSHIMAGECLONER_EXECUTABLE_FILE
sudo chmod +x $SSHIMAGECLONER_EXECUTABLE_FILE

popd

# Remove the temporary installation directory
printf "Removing the temporary directory\n"
sudo rm -r $SSHIMAGECLONER_TMP_DIR
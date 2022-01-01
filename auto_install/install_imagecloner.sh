#!/usr/bin/env bash

# -e option tells bash to exit if any command has a non-zero exit status
set -e

# Set variables for the script
SSHIMAGECLONER_TMP_DIR="/tmp/sshimageclonertmp"
SSHIMAGECLONER_EXECUTABLE_FILE="/usr/local/bin/sshimagecloner"
SSHIMAGECLONER_CONFIG_DIR="/etc/sshimagecloner"
SSHIMAGECLONER_CONFIG_FILE="/etc/sshimagecloner/sshimagecloner.yaml"
SSHIMAGECLONER_LOGROTATE_FILE="/etc/logrotate.d/sshimagecloner"

sudo apt update
sudo apt install git python3-pip -y

# Create temp directory, and change working directory there
[ ! -d $SSHIMAGECLONER_TMP_DIR ] && sudo mkdir $SSHIMAGECLONER_TMP_DIR
pushd $SSHIMAGECLONER_TMP_DIR

# Clone the git repository to temp directory
sudo git clone https://github.com/mikael-ri/sshimagecloner

sudo pip install -r sshimagecloner/auto_install/requirements.txt

# Create config directory, and move the config file there
[ ! -d $SSHIMAGECLONER_CONFIG_DIR ] && sudo mkdir $SSHIMAGECLONER_CONFIG_DIR
sudo cp sshimagecloner/auto_install/sshimagecloner_example.yaml $SSHIMAGECLONER_CONFIG_FILE

# Copy the logrotate file
sudo cp sshimagecloner/auto_install/logrotate.d/sshimagecloner $SSHIMAGECLONER_LOGROTATE_FILE

# Copy the main script and make sure it is executable
sudo cp sshimagecloner/sshimagecloner $SSHIMAGECLONER_EXECUTABLE_FILE
sudo chmod +x $SSHIMAGECLONER_EXECUTABLE_FILE

popd

# Remove the temporary installation directory
sudo rm -r $SSHIMAGECLONER_TMP_DIR
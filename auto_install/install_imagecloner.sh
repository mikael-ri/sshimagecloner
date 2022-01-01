#!/usr/bin/env bash

# -e option tells bash to exit if any command has a non-zero exit status
set -e

# Set variables for the script
SSHIMAGECLONER_TMP_DIR="/tmp/sshimageclonertmp"
SSHIMAGECLONER_EXECUTABLE_FILE="/usr/local/bin/sshimagecloner"
SSHIMAGECLONER_CONFIG_DIR="/etc/sshimagecloner"
SSHIMAGECLONER_CONFIG_FILE="/etc/sshimagecloner/sshimagecloner.yaml"
SSHIMAGECLONER_LOGROTATE_FILE="/etc/logrotate.d/sshimagecloner"

# Create temp directory, and change working directory there
sudo mkdir $SSHIMAGECLONER_TMP_DIR
pushd $SSHIMAGECLONER_TMP_DIR

# Clone the git repository to temp directory
git clone https://github.com/mikael-ri/sshimagecloner

# Create config directory, and move the config file there
sudo mkdir $SSHIMAGECLONER_CONFIG_DIR
sudo cp sshimagecloner/sshimagecloner_example.yaml $SSHIMAGECLONER_CONFIG_FILE

# Copy the logrotate file
sudo cp sshimagecloner/auto_install/logrotate.d/sshimagecloner $SSHIMAGECLONER_LOGROTATE_FILE

# Copy the main script and make sure it is executable
sudo cp sshimagecloner/sshimagecloner $SSHIMAGECLONER_EXECUTABLE_FILE
sudo chmod +x $SSHIMAGECLONER_EXECUTABLE_FILE

# Remove the temporary installation directory
sudo rm -r $SSHIMAGECLONER_TMP_DIR

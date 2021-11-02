# sshimagecloner
A tool to backup disk images from remote server to local hard drive

## About the project

I started to create this tool to solve the problem of possible sd-card failure (or any other situation of breaking the card / image /installation) of an Raspberry Pi computer, so that I could restore the most recent state to a new sd-card. As I usually don't remember to take the backups manually, I needed to create an automatic solution.

Also, I needed the backup to be done over the network, and while the pi is running.

As there probably exists a lot of good and great tools to accomplish this, this project also serves as a learning / testing project for python.

I'm using [rsnapshot](https://rsnapshot.org/) for file backup on the linux virtual machines and Raspberry Pi's, and I can warmly recommend that tool! Certain influences can be seen on the functionality of this tool as well.

## Usage
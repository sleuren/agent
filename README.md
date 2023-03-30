# Agent

Server Monitoring (sleuren.com) is a web service that monitors and displays statistics of your server performance.

Agent is OS agnostic software compatible with Python 2.7, 3.5, and 3.6. It's been optimized to have low CPU consumption and comes with an extendable set of useful plugins.

[![Build Status](https://github.com/sleuren/agent/workflows/Agent-Test-And-Deploy/badge.svg?branch=main)](https://github.com/sleuren/agent/actions/workflows/test-and-deploy.yml)

## Documentation

You can find the full documentation at [docs.sleuren.com](https://sleuren.com/docs).

## Automatic Installation (All Linux Distributions)

You can install the default configuration of Sleuren on all Linux distributions with just one click.

1. Connect to your server via SSH.

2. Find your `TOKEN`. To do so, [go to the project installation page](https://sleuren.com/dashboard).

3. Run the following command:

  ```sh
  wget -q -N https://sleuren.com/sleuren.sh && bash sleuren.sh TOKEN
  ```

## Manual Installation

To customize installation options, install sleuren agent manually.

1. Connect to your server via SSH.
2. Run the following command, which differs depending on your server platform:

    - Debian GNU/Linux:

        ```sh
        apt-get install python3-devel python3-setuptools python3-pip
        pip3 install sleuren
        wget -O /etc/sleuren.ini https://sleuren.com/scripts/sleuren.ini
        ```

    - Fedora/CentOS version 6 or earlier (python 2.7):

        ```sh
        yum install python-devel python-setuptools gcc
        easy_install sleuren netifaces psutil
        wget -O /etc/sleuren.ini https://sleuren.com/scripts/sleuren.ini
        ```

    - Fedora/CentOS version 7 and later (python 3):

        ```sh
        yum install python36-devel python36 gcc
        pip3 install sleuren
        wget -O /etc/sleuren.ini https://sleuren.com/scripts/sleuren.ini
        ```

3. Find your `TOKEN`. To do so, [go to the project installation page](https://sleuren.com/dashboard).

4. Run the following command (TOKEN is the one you got during the previous step):

    ```sh
    sleuren hello TOKEN /etc/sleuren-token.ini
    ```

5. Create a systemd service at `/etc/systemd/system/sleuren.service` by adding the following:

    ```ini
    [Unit]
    Description=Sleuren agent
    [Service]
    ExecStart=/usr/local/bin/sleuren
    User=sleuren
    [Install]
    WantedBy=multi-user.target
    ```

6. Run the following command:

    ```sh
    chmod 644 /etc/systemd/system/sleuren.service
    systemctl daemon-reload
    systemctl enable sleuren
    systemctl start sleuren
    ```
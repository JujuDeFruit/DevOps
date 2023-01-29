# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 14:18:48 2020

@author: Julien
"""
# pylint: disable=import-error
# pylint: disable=broad-except
# pylint: disable=too-many-locals
# pylint: disable=cyclic-import
# test

import os
import re

from paramiko import SSHClient, AutoAddPolicy, ssh_exception


class SSH:
    """
    A class to represent a ssh connection.

    ...

    Attributes
    ----------
    data : dict
        data returned by dist server
    client : SSH client
        current ssh client of the connection
    commands : array
        list of commands to be executed by dist server
    server : dict
        configuration of dist server

    Methods
    -------
    connect():
        Connects client to server.
    execute():
        Client execute commands on dist server.
    callback():
        Write data infos from server info json file.
    close():
        Close client connection from dist server.
    set_command(cmd): Array or str
        Set command attr

    """

    def __init__(self, commands_=None, server_=None):
        """
        Constructs all the necessary attributes for the SSH object.

        Parameters
        ----------
            commands_ : array of strings
            all commands to execute on dist server
            server_ : dict
            contains all key to configure connection to dist server

        """
        # data is a dict contains all data printed in json file
        self.data = {}
        # client
        self.client = None

        if server_ is None:
            self.server = {
                "ip": "",
                "user": "",
                "password": "",
                "port": 22,
            }
        else:
            self.server = server_

        # Commands to execute on dist server
        if commands_ is None:
            self.commands = [
                "free",
                "top",
                "ps",
                "vmstat",
                "ifconfig -a",
                "cat /proc/meminfo",
                "cat /proc/cpuinfo",
                "cat /var/log/apache2/access.log",
                "cat /sys/class/net/eth0/statistics/rx_packets",
                "cat /sys/class/net/eth0/statistics/tx_packets",

            ]
        else:
            self.commands = commands_

    # Connect to dist server
    def connect(self):
        """
        Connects client to server.

        Parameters
        ----------
        self

        """
        try:
            # Create ssh process
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy)
            # Connect to server
            self.client.connect(
                self.server["ip"],
                username=self.server["user"],
                password=self.server["password"],
                port=self.server["port"],
            )
            return False
        except ssh_exception.SSHException:
            print("Error while connecting to " + self.server["ip"])
            return True
        except TimeoutError:
            print("Server failed: Timeout error.")
            return True
        except Exception:
            print('Unknown error occured while connecting to ' + self.server["ip"])
            return True

    def execute(self):
        """
        Client execute commands on dist server.

        Parameters
        ----------
        self

        """
        try:
            for cmd in self.commands:
                # Exec command on server
                _, stdout, _ = self.client.exec_command(cmd)
                output = stdout.read().decode("utf-8")
                # Add data array like in the current header command
                self.data[cmd] = []
                for line in output.splitlines():
                    self.data[cmd].append(line)
            # Extract speed response average
            self.data["ping"] = re.sub(r"\D",
                                       "",
                                       os.popen("ping -c 4 " + str(self.server["ip"])).read()
                                       .splitlines()[-1].split()[3].split("/")[1])
            return False
        except ssh_exception.SSHException:
            print(self.server['ip'] + " failed execute " + cmd)
            return True
        except Exception:
            print("Unknown error occur. " + self.server['ip'] + " failed execute " + cmd)
            return True

    def close(self):
        """
        Close client connection from dist server.

        Parameters
        ----------
        self

        """
        if self.client is not None:
            self.client.close()

    def set_command(self, cmd):
        """
        Setter for command parameter.

        Parameters
        ----------
        cmd : string
            Command to set.

        Returns
        -------
        None.

        """
        if isinstance(cmd, list):
            self.commands = cmd
        elif isinstance(cmd, str):
            self.commands = [cmd]
        else:
            raise TypeError("Command must be str or array of srt.")

    def __eq__(self, o):
        """
        Overdefinition of == operator

        Parameters
        ----------
        o: SSH
            Item to compare

        Returns
        -------
        boolean:
            True if equal, else False

        """
        return self.server == o.server

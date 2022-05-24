# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 15:28:54 2020

@authors: Julien, Mathieu
"""
# pylint: disable=no-name-in-module
# pylint: disable=wrong-import-position
# pylint: disable=line-too-long
# pylint: disable=import-error

import unittest2
from connection.connect import SSH
from connection.variable import DEFAULT_SERVER_CONFIG


class ConnectionTest(unittest2.TestCase):
    """
    A class to test SSH class.

    ...

    Attributes
    ----------
    ssh : cls
        attribute contains SSH class
    client : SSH client
        current ssh client of the connection
    commands : array
        list of commands to be executed by dist server
    server : dict
        configuration of dist server

    Methods
    -------
    setUpClass():
        Set up SSH class to unittest.
    test_connectMethod():
        Test connecting method from SSH class.
    test_execute():
        Test to execute commands on server.
    test_callback():
        Check the opening and existing of the file.
    test_close():
        Test closing connection method from SSH class.
    request(cmd):
        Test requesting method equal to format from SSH class.
    test_connection():
        Test connection calback equal to format.
    test_notConnection():
        Test connection callback is null when command is fake.

    """

    @classmethod
    def setUpClass(cls):
        """
        Set up SSH class to unittest.

        Parameters
        ----------
        cls: class

        """
        cls.ssh = SSH(server_=DEFAULT_SERVER_CONFIG)

    def test_connect(self):
        """
        Test connecting method from SSH class.

        Parameters
        ----------
        self

        """
        self.ssh.connect()
        self.assertNotEqual(self.ssh.client, None)

    def test_execute(self):
        """
        Test to execute commands on server.

        Parameters
        ----------
        self

        """
        self.ssh.execute()
        self.assertNotEqual(self.ssh.data, {})

    # Test close method
    def test_close(self):
        """
        Test closing connection method from SSH class.

        Parameters
        ----------
        self

        """
        self.ssh.close()
        self.assertEqual(self.ssh.client, None)

    # Create a request to ssh server
    def request(self, ssh, cmd):
        """
        Test requesting method equal to format from SSH class.

        Parameters
        ----------
        self
        cmd : array
        Command to be executed by dist server
        ssh: SSH
        SSH client

        """
        ssh.set_command(cmd)
        ssh.execute()

        regex = None
        if cmd == "free":
            regex = r"              total        used        free      shared  buff/cache   available"
        elif cmd == "top":
            regex = r""
        elif cmd == "ps":
            regex = r"  PID TTY          TIME CMD"
        elif cmd == "vmstat":
            regex = r"procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----"
        elif cmd == "ifconfig -a":
            regex = r"[\w]+: flags=\d+<[A-Z,]+>  mtu \d+"
        elif cmd == "cat /proc/meminfo":
            regex = r"[\w()_]:[0-9 ]+ kB"
        elif cmd == "cat /proc/cpuinfo":
            regex = r"processor\t: \d+"
        else:
            raise AssertionError()

        if len(ssh.data[cmd]) > 0:
            self.assertRegex(ssh.data[cmd][0], regex)

    def test_connection(self):
        """
        Test connection calback equal to format.

        Parameters
        ----------
        self

        """
        # Connect and execute specific command on ssh server
        ssh = SSH(server_=DEFAULT_SERVER_CONFIG)
        ssh.connect()
        # Create request for each command
        self.request(ssh, "free")
        self.request(ssh, "top")
        self.request(ssh, "ps")
        self.request(ssh, "vmstat")
        self.request(ssh, "ifconfig -a")
        self.request(ssh, "cat /proc/meminfo")
        self.request(ssh, "cat /proc/cpuinfo")
        # close ssh connection
        ssh.close()

    # Test not connection
    def test_not_connection(self):
        """
        Test connection callback is null when command is fake.

        Parameters
        ----------
        self

        """
        cmd = "ertgvbhjk"
        # Connect and execute specific command on ssh server
        ssh = SSH(commands_=[cmd], server_=DEFAULT_SERVER_CONFIG)
        ssh.connect()
        ssh.execute()
        # Check if ssh fake command return null array.
        self.assertEqual(ssh.data[cmd], [])
        ssh.close()

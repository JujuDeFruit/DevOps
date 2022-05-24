# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:08:50 2020

@author: Julien
"""

# pylint: disable=no-name-in-module
# pylint: disable=wrong-import-position
# pylint: disable=cyclic-import


import unittest2
from apachelogs import LogParser
import connection


class LogsTest(unittest2.TestCase):
    """
    A class to test los parsing.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    test_format_logs():
        Test logs formatter.
    test_output_format():
        Test logs parsing.

    """

    def test_format_logs(self):
        """
        Test formatting data

        Parameters
        ----------
        self

        """
        cmd = "cat /var/log/apache2/access.log"
        ssh = connection.connect.SSH(
            commands_=[cmd],
            server_=connection.variable.DEFAULT_SERVER_CONFIG
        )
        err = ssh.connect()
        if err:
            ssh.close()
            raise Exception()

        err = ssh.execute()
        if err:
            ssh.close()
            raise Exception()

        # Format data
        formatted_logs = connection.logs.format_logs(ssh.data[cmd])
        # Test formatted data type
        self.assertEqual(type(formatted_logs), type([]))
        # Test first log regex
        try:
            if len(formatted_logs) > 0:
                self.assertRegex(
                    formatted_logs[0],
                    r"(\d+.){3}\d+ \| .* \| \d{4}-\d{2}-\d{2} (\d{2}:){2}\d{2}\+\d{2}:\d{2} \| \d+"
                )
        except TypeError:
            pass
        finally:
            ssh.close()

    def test_output_format(self):
        """
        Test logs parsing.

        Parameters
        ----------
        self

        """
        # Command to get logs
        cmd = "cat /var/log/apache2/access.log"
        # Connect and get logs command on ssh server
        log = connection.connect.SSH(
            commands_=[cmd],
            server_=connection.DEFAULT_SERVER_CONFIG
        )
        log.connect()
        log.execute()
        # Logs parser
        parser = LogParser('%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"')
        # Test returned log in a certain format to regex
        for data in log.data[cmd]:
            # Get returned log
            line = parser.parse(data)
            formatted = connection.logs.output_format(line)
            if formatted != '':
                try:
                    self.assertRegex(
                        connection.logs.output_format(line),
                        r"(?:\d+.){3}\d+ | (?:[A-Z ]+ [\s\w$&+,:;=?@#|' \\/<>.^*()%!\xad\]"
                        + r"[-]+ [A-Z0-9\/. ]+|[\s\w$&+,:;=?@#|' \\/<>.^*()%!\]\xad[-]+) | "
                        + r"[0-9-]+ [\d{2}:]{8}\+\d{2}:\d{2} | \d{3}",
                    )
                except TypeError:
                    pass
                finally:
                    log.close()
        log.close()

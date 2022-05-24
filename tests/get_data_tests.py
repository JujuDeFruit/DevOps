"""Tests for getting data from functions_interface"""

import unittest2
import connection


class GetDataTest(unittest2.TestCase):
    """A class to test functions in functions_interface.py"""

    def test_cast(self):
        """Test cast function"""
        self.assertEqual(0, connection.functions_interface.cast("0", int))
        self.assertNotEqual("0", connection.functions_interface.cast("0", int))

        self.assertEqual("0", connection.functions_interface.cast(0, str))
        self.assertNotEqual(0, connection.functions_interface.cast(0, str))

    def test_recup_memory(self):
        """Test recup_memory function"""
        ssh = connection.connect.SSH(
            commands_=["cat /proc/meminfo", "cat /proc/cpuinfo"],
            server_=connection.variable.DEFAULT_SERVER_CONFIG
        )
        ssh.connect()
        ssh.execute()
        _, mem_vals, mem_percent, _, cpu_vals, cpu_percent, mem_cpu_cache_total \
            = connection.functions_interface.recup_memory(ssh)
        ssh.close()

        self.assertEqual(type(mem_vals), list)
        self.assertEqual(len(mem_vals), 2)
        self.assertEqual(type(mem_vals[0]), int)
        self.assertEqual(type(mem_vals[1]), int)

        self.assertEqual(type(mem_percent), float)
        self.assertGreater(mem_percent, 0.0)

        self.assertEqual(type(cpu_vals), list)
        self.assertEqual(len(cpu_vals), 2)
        self.assertEqual(type(cpu_vals[0]), int)
        self.assertEqual(type(cpu_vals[1]), int)

        self.assertEqual(type(cpu_percent), float)
        self.assertGreater(cpu_percent, 0)

        self.assertEqual(type(mem_cpu_cache_total), int)
        self.assertGreater(mem_cpu_cache_total, 0)

    def test_recup_rx_tx(self):
        """Test recup_rx_tx function"""
        ssh = connection.connect.SSH(
            commands_=[
                "cat /sys/class/net/eth0/statistics/rx_packets",
                "cat /sys/class/net/eth0/statistics/tx_packets"
            ],
            server_=connection.variable.DEFAULT_SERVER_CONFIG
        )
        ssh.connect()
        ssh.execute()
        rx_backup, tx_backup = connection.functions_interface.recup_rx_tx(ssh)
        ssh.close()

        self.assertEqual(type(rx_backup), str)
        self.assertGreater(int(rx_backup), 0)

        self.assertEqual(type(tx_backup), str)
        self.assertGreater(int(tx_backup), 0)

    def test_recup_response_time(self):
        """Test recup_response_time function"""
        ssh = connection.connect.SSH(
            commands_=[],
            server_=connection.variable.DEFAULT_SERVER_CONFIG
        )
        ssh.connect()
        ssh.execute()
        time = connection.functions_interface.recup_response_time(ssh)
        ssh.close()

        self.assertEqual(type(time), int)
        self.assertGreater(time, 0.0)

    def test_recup_static_infos(self):
        """Test recup_static_infos"""
        ssh = connection.connect.SSH(
            commands_=[
                "cat /proc/cpuinfo",
                "ifconfig -a"
            ],
            server_=connection.variable.DEFAULT_SERVER_CONFIG
        )
        ssh.connect()
        ssh.execute()
        ip_serv, proc, model, freq, nb_cpu = connection.functions_interface.recup_static_infos(ssh)
        ssh.close()

        self.assertEqual(type(ip_serv), str)
        self.assertRegex(
            ip_serv,
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        )

        self.assertEqual(type(proc), str)
        self.assertGreaterEqual(int(proc), 0)

        self.assertEqual(type(model), str)

        self.assertEqual(type(freq), str)
        self.assertGreaterEqual(float(freq), 0)

        self.assertEqual(type(nb_cpu), str)
        self.assertGreaterEqual(int(nb_cpu), 0)

    def test_recup_processes(self):
        """Test recup_processes"""
        ssh = connection.connect.SSH(
            commands_=["ps"],
            server_=connection.variable.DEFAULT_SERVER_CONFIG
        )
        ssh.connect()
        ssh.execute()
        processes = connection.functions_interface.recup_processes(ssh)
        ssh.close()

        self.assertEqual(type(processes), list)
        self.assertGreater(len(processes), 0)
        self.assertEqual(type(processes[0]), list)
        self.assertEqual(len(processes[0]), 3)
        for process in processes[0]:
            self.assertEqual(type(process), str)

    def test_has_values(self):
        """Test has_values function"""
        ssh = connection.connect.SSH(
            server_=connection.variable.DEFAULT_SERVER_CONFIG
        )
        ssh.connect()
        ssh.execute()
        ssh.close()
        self.assertEqual(connection.functions_interface.has_values(ssh), True)

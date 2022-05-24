"""Module to get specific data from all data get from the server"""
# pylint: disable=no-name-in-module
# pylint: disable=too-many-locals
# pylint: disable=broad-except
# pylint: disable=cyclic-import

import re
import logs

MEM_AVAILABLE_STR = "Available Memory"
MEM_USE_STR = "Memory Used"
CPU_CACHE_USE_STR = "CPU Cache Used"


def cast(val, typ):
    """
    Try to cast value in a certain type

    Parameters
    ----------
    val: value to cast
    typ: type of variable to cast to

    Returns
    -------
    casting or "null"

    """
    try:
        ret = typ(val)
    except Exception:
        ret = "null"
    return ret


def recup_memory(ssh):
    """
    Get memory infos

    Parameters
    ----------
    ssh: current ssh client

    Returns
    -------
    Memory informations

    """
    data_mem = ssh.data["cat /proc/meminfo"]
    mem_tot = cast(re.findall("\\d+", data_mem[0])[0], int)
    mem_free = cast(re.findall("\\d+", data_mem[1])[0], int)
    mem_available = cast(re.findall("\\d+", data_mem[2])[0], int)
    mem_cpu_cache_used = cast(re.findall("\\d+", data_mem[35])[0], int)
    data_cpu = ssh.data["cat /proc/cpuinfo"]
    mem_cpu_cache_total = cast(re.findall("\\d+", data_cpu[8])[0], int)
    mem_cpu_cache_available = mem_cpu_cache_total - mem_cpu_cache_used
    mem_use = mem_tot - mem_free
    mem_labs = [MEM_USE_STR, MEM_AVAILABLE_STR]
    mem_vals = [mem_use, mem_available]
    mem_percent = mem_use / mem_tot * 100
    cpu_labs = [CPU_CACHE_USE_STR, "Available CPU Cache"]
    cpu_vals = [mem_cpu_cache_used, mem_cpu_cache_available]
    cpu_percent = mem_cpu_cache_used / mem_cpu_cache_total * 100

    return mem_labs, mem_vals, mem_percent, cpu_labs, cpu_vals, cpu_percent, mem_cpu_cache_total


def recup_rx_tx(ssh):
    """
    Get memory infos

    Parameters
    ----------
    ssh: current ssh client

    Returns
    -------
    Numbers of TX/RX packets

    """
    data = ssh.data
    data_rx = data["cat /sys/class/net/eth0/statistics/rx_packets"]
    data_tx = data["cat /sys/class/net/eth0/statistics/tx_packets"]

    return data_rx[0], data_tx[0]


def recup_response_time(ssh):
    """
    Get ping

    Parameters
    ----------
    ssh: current ssh client

    Returns
    -------
    ping info

    """
    response_time = cast(ssh.data["ping"], int)
    return response_time


def recup_static_infos(ssh):
    """
    Get static informations such as ip, processor, model name ...

    Parameters
    ----------
    ssh: current ssh client

    Returns
    -------
    Static infos

    """
    ip_serv = "null"
    proc = "null"
    model = "null"
    freq = "null"
    nb_cpu = "null"
    # Get ip
    ip_serv = ssh.data["ifconfig -a"][1].split()[1]
    # Browse dict to find corresponding data
    for data in ssh.data["cat /proc/cpuinfo"]:
        if "processor\t:" in data:
            proc = data.split()[-1]
        if "model name\t:" in data:
            model = data.split(":")[-1]
        if "cpu MHz\t\t:" in data:
            freq = data.split()[-1]
        if "cpu cores\t:" in data:
            nb_cpu = data.split()[-1]

    return ip_serv, proc, model, freq, nb_cpu


def recup_processes(ssh):
    """
    Get processes

    Parameters
    ----------
    ssh: current ssh client

    Returns
    -------
    All processes

    """
    processus = []
    # Get all processes and exclude first line
    ps_cmd = ssh.data["ps"][1:]

    for process in ps_cmd:
        # split process by every blank (space, \t ...)
        splitted = process.split()
        pid = splitted[0]
        time = splitted[2]
        cmd = splitted[3]
        processus.append([pid, time, cmd])

    # If value is loaded
    if len(processus) == 0:
        return "null"
    return processus


def recup_logs(ssh):
    """
    Get logs

    Parameters
    ----------
    ssh: current ssh client

    """
    # Get log in ssh client data
    logs_ = ssh.data["cat /var/log/apache2/access.log"]
    # format logs list-like
    formatted_logs = logs.format_logs(logs_)

    if len(formatted_logs) == 0:
        return "null"
    return formatted_logs


def has_values(ssh):
    """
    Check if all values are availables

    Parameters
    ----------
    ssh: current ssh client

    Returns
    -------
    boolean: True if program loaded all values, else False

    """
    val = [
        recup_memory(ssh),
        recup_response_time(ssh),
        recup_static_infos(ssh),
        recup_processes(ssh),
        recup_logs(ssh),
    ]

    if "null" in val:
        return False
    return True

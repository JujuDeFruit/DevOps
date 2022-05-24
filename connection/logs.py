# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 15:28:54 2020

@author: Julien
"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=duplicate-code
# pylint: disable=cyclic-import

from apachelogs import LogParser


def format_logs(datas):
    """
    Format data logs

    Parameters
    ----------
    datas: array of strings
        data to format

    Returns
    -------
    formatted logs

    """
    parser = LogParser('%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"')
    temp = []
    for data in datas:
        line = parser.parse(data)
        temp.append(output_format(line))
    return temp


def output_format(line):
    """
    Line to return on good format.

    Parameters
    ----------
    line: const string
        Command

    """
    output = ""
    try:
        output = (
            line.directives["%h"]
            + " | "
            + line.directives["%r"]
            + " | "
            + str(line.directives["%t"])
            + " | "
            + str(line.directives["%>s"])
        )
    except TypeError:
        pass
    return output

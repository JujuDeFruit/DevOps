# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 09:51:11 2020

@author: Julien
"""


import unittest2
from tests.connection_tests import ConnectionTest
from tests.logs_tests import LogsTest
# from tests.get_data_tests import GetDataTest


def suite():
    """
    Create a test suite to implement runner

    Parameters
    ----------
    None

    """
    suite_ = unittest2.TestSuite()
    test_loader = unittest2.TestLoader()
    suite_.addTests(test_loader.loadTestsFromTestCase(ConnectionTest))
    suite_.addTests(test_loader.loadTestsFromTestCase(LogsTest))
    # suite_.addTests(test_loader.loadTestsFromTestCase(GetDataTest))
    return suite_


if __name__ == "__main__":
    runner = unittest2.TextTestRunner()
    runner.run(suite())

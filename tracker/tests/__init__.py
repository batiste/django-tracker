"""Build test suite"""
import unittest

def suite():
    suite = unittest.TestSuite()
    from tracker.tests.unit_test import UnitTestCase
    suite.addTest(unittest.makeSuite(UnitTestCase))
    return suite

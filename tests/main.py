# ------------------------------------------------------------------------------
# Project: DueDesk
# Module: main
#
# Abstract: 
#   The main host for integration tests. Integration tests validate multiple 
#   components of the system work together in an intended way.
# ------------------------------------------------------------------------------

import unittest

#--- integration-tests ---
class IntegrationTest(unittest.TestCase):
    
    def test_sample_integration(self):
        self.assertEqual(True, True)

import unittest
from modules.const import Keys, AttrKey
import modules.zabbix_smart as zabbix_smart
import json
import glob
import tests.util as util
import os
import tests.const as const

import smart_to_zabbix as main

class TestInterpriters(unittest.TestCase):

    files = []

    def setUp(self):
        cwd = os.getcwd()
        globspec = os.path.join(cwd, const.EXAMPLE_DEVICE_DIR, "*.json")
        self.files = glob.glob(globspec)


    def test_find_interpriter(self):
        """ 
        find_interpriterの単体テスト
        """

        for filename in self.files:
            if util.is_not_test_target(filename):
                continue

            with self.subTest(filename=filename):
                with open(filename) as f:
                    jsonStr = f.read()

                detail = json.loads(jsonStr)

                main.find_interpriter(detail)
                
                self.assertTrue(True)
    

    def test_find_interpriter(self):
        

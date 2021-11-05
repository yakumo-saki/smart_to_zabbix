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
    def test_find_interpriter(self):
        """ 
        find_interpriterの単体テスト
        interpriter判定時に存在しない項目を決め打ちで読みに行ってないかのテスト
        """

        files = util.get_all_json_paths()
        for filename in files:
            with self.subTest(filename=filename):
                with open(filename) as f:
                    jsonStr = f.read()

                detail = json.loads(jsonStr)

                main.find_interpriter(detail)
                
                self.assertTrue(True)
    

    def test_interpriter(self):
        """ 
        interpriterのparse単体テスト
        """

        files = util.get_all_json_paths()
        for filename in files:
            with self.subTest(filename=filename):
                with open(filename) as f:
                    jsonStr = f.read()

                detail = json.loads(jsonStr)

                intp = main.find_interpriter(detail)
                parsed = intp.parse(detail)
                self.assertEqual(parsed[Keys.DISK_MODEL], parsed["model_name"])
 
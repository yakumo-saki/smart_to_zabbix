from dataclasses import replace
import unittest
from modules.const import Keys, AttrKey
import modules.zabbix_smart as zabbix_smart
import json
import glob
import tests.util as util
import os
import tests.const as const

import smart_to_zabbix as main

import logging

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
        self.assertNotEqual(len(files), 0, "No example json files found.")

        for filepath in files:
            with self.subTest(filename=os.path.basename(filepath)):
                expected_filepath = filepath.replace(const.EXAMPLE_DEVICE_DIR, const.EXAMPLE_DEVICE_EXPECTED_DIR)
                with open(expected_filepath) as f:
                    expectedJson = f.read()
                expected = json.loads(expectedJson)

                with open(filepath) as f:
                    inputJson = f.read()
                input = json.loads(inputJson)

                intp = main.find_interpriter(input)
                parsed = intp.parse(input)

                # print(json.dumps(parsed, indent=2))
                self.assertEqual(expected, parsed)

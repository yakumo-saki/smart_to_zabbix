import unittest
from modules.const import Keys, AttrKey
import modules.zabbix_smart as zabbix_smart
import json
import glob
import tests.util as util
import os
import tests.const as const

class TestZabbixSmartListSata(unittest.TestCase):

    files = []

    def setUp(self):
        cwd = os.getcwd()
        globspec = os.path.join(cwd, const.EXAMPLE_DEV_SATA_DIR,"*.json")
        self.files = glob.glob(globspec)


    def test_create_attribute_list_sata(self):
        """ 
        create_attribute_list_sataの単体テスト
        """

        for filename in self.files:
            if util.is_not_test_target(filename):
                continue

            with self.subTest(filename=filename):
                with open(filename) as f:
                    jsonStr = f.read()

                detail = json.loads(jsonStr)
                discovery = {AttrKey.DEV_NAME: "dummy", AttrKey.DISK_NAME: filename}

                zabbix_smart.create_attribute_list_non_nvme(
                    discovery,
                    detail["ata_smart_attributes"]
                )
                
                self.assertTrue(True)
    

    def test_create_value_list_nvme(self):
        """ 
        create_value_list_nvmeの単体テスト
        """
        
        for filename in self.files:
            if util.is_not_test_target(filename):
                continue

            with self.subTest(filename=filename):
                with open(filename) as f:
                    jsonStr = f.read()

                detail = json.loads(jsonStr)
                discovery = {AttrKey.DEV_NAME: "dummy", AttrKey.DISK_NAME: filename}

                zabbix_smart.create_value_list_non_nvme(
                    "dummy",
                    detail["ata_smart_attributes"]
                )
                
                self.assertTrue(True)
                
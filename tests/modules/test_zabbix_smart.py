import unittest
from modules.const import Keys, AttrKey
import modules.zabbix_smart as zabbix_smart
import json
import glob
import tests.util as util

class TestStringMethods(unittest.TestCase):
 
    def test_create_attribute_list_nvme(self):
        """ 
        create_attribute_list_nvmeの単体テスト
        """
        
        nvmes = glob.glob("smart_examples/device_nvme/*.json")
        for filename in nvmes:
            if util.is_not_test_target(filename):
                continue

            with self.subTest(filename):
                with open("smart_examples/device_nvme/samsung_ssd_980.json") as f:
                    jsonStr = f.read()

                detail = json.loads(jsonStr)
                discovery = {AttrKey.DEV_NAME: "dummy", AttrKey.DISK_NAME: filename}

                zabbix_smart.create_attribute_list_nvme(discovery, detail["nvme_smart_health_information_log"])


        

if __name__ == '__main__':
    unittest.main()

import logging

from interpriters.smart.SmartBaseInterpriter import SmartBaseInterpriter
from modules.const import Keys, Unit
from interpriters.tbw_estimate import tbw_estimate

logger = logging.getLogger(__name__)

"""
Sum
"""
class SamsungSSDInterpriter(SmartBaseInterpriter):
    # def __init__(self):
    #     pass

    def isTargetStrict(self, data):
        return False

    def isTargetLoose(self, data):
        if ("model_family" in data):
            return (data["model_family"] == "Samsung based SSDs")
        
        return False

    def parse(self, data):
        ret = self.basic_parse(data)

        # 241 Total_LBAs_Written はその名の通りLBAの数を掛ける
        ret[Keys.SSD_BYTES_WRITTEN] = (self.get_smart_raw_value(data, 241) * data["physical_block_size"])
        ret[Keys.SSD_BYTES_WRITTEN_MAX] = tbw_estimate(data)

        return ret

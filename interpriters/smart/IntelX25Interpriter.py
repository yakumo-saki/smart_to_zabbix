import logging

from interpriters.smart.SmartBaseInterpriter import SmartBaseInterpriter
from modules.const import Keys, Unit
from interpriters.tbw_estimate import tbw_estimate

logger = logging.getLogger(__name__)

"""
SanDisk SSDSSDH3 -> Marvel 88SS1074
"""
class IntelX25Interpriter(SmartBaseInterpriter):
    # def __init__(self):
    #     pass

    def isTargetStrict(self, data):
        if (data["model_family"].startswith("Intel X18-M/X25-M/X25-V G2 SSDs")):
            return True

        return False

    def isTargetLoose(self, data):
        return (data["model_name"].startswith("INTEL"))

    def parse(self, data):
        logger.debug("IntelX25")
        ret = self.basic_parse(data)

        ret[Keys.SSD_LIFESPAN] = self.get_smart_value(data, 233)

        hostWrites = self.get_smart_raw_value(data, 225)
        ret[Keys.SSD_BYTES_WRITTEN] = (hostWrites * 32 * Unit.MB)

        return ret

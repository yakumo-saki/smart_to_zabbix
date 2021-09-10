import logging
from interpriters.nvme.NvmeBaseInterpriter import NvmeBaseInterpriter
from modules.const import Keys, C

logger = logging.getLogger(__name__)

class NvmeBasicInterpriter(NvmeBaseInterpriter):
    """
    最低限の解釈だけを行うInterpriter
    """


    """
    解釈を行います。
    """
    def parse(self, data):
        ret = self.basic_parse(data)

        smart = data[C.SMART_NVME_KEY]

        # minimum parse
        ret[Keys.SSD_LIFESPAN] = smart[C.AVAIL_SPARE]

        return ret


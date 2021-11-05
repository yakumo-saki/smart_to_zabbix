import logging
from modules.zabbix_data import get_empty_data
from modules.const import Keys

logger = logging.getLogger(__name__)

class BaseInterpriter(object):
    """
    Base class interpriters.
    """

    def __init__(self):
        pass

    """デバイスタイプ（SATA,SCSI,NVME)が処理対象かを返す
    一番最初に聞かれる
    """
    def isTargetDeviceType(self, data):
        raise RuntimeError("MustOverride")

    """
    指定されたモデルが解釈可能か否かを返します。
    すべてのInterpriterに対して本メソッドを呼び、最初に見つかったInterpriterに
    解釈を依頼します。
    """
    def isTargetStrict(self, data):
        raise RuntimeError("MustOverride")


    """
    指定されたモデルが解釈可能かもしれないか否かを返します。
    すべてのInterpriterがisTargetStrict = False を返した場合、
    本メソッドを呼び、最初に見つかったInterpriterに解釈を依頼します。
    """
    def isTargetLoose(self, data):
        raise RuntimeError("MustOverride")


    # smartctlから値を安全に取得します。
    def getValue(self, smartctl, key1, key2 = None):
        v1 = smartctl.get(key1) 
        if (v1 == None): 
            return None
        elif (key2 == None):
            #print(v1)
            return v1
        
        v2 = v1.get(key2)
        #print(v2)
        return v2

    """
    解釈を行います。
    """
    def parse(self, data):
        logger.error("BaseInterpriter can not do `parse`")
        raise RuntimeError("Must override")


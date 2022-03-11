from interpriters.smart.IntelX25Interpriter import IntelX25Interpriter
from interpriters.smart.SmartBasicInterpriter import SmartBasicInterpriter
from interpriters.smart.SanDiskInterpriter import SmartSanDiskInterpriter
from interpriters.smart.SamsungSSDInterpriter import SamsungSSDInterpriter
from interpriters.nvme.NvmeBasicInterpriter import NvmeBasicInterpriter


SPECIAL_INTERPRITERS = [SmartSanDiskInterpriter(), IntelX25Interpriter(), SamsungSSDInterpriter()]
BASIC = [SmartBasicInterpriter(), NvmeBasicInterpriter()]
from interpriters.smart.SmartBasicInterpriter import SmartBasicInterpriter
from interpriters.smart.SanDiskInterpriter import SmartSanDiskInterpriter
from interpriters.nvme.NvmeBasicInterpriter import NvmeBasicInterpriter


SPECIAL_INTERPRITERS = [SmartSanDiskInterpriter()]
BASIC = [SmartBasicInterpriter(), NvmeBasicInterpriter()]
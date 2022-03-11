from modules.const import Unit

"""SSDの書き込み許容量(TBW)を適当に決める
"""
def tbw_estimate(smartctl):
    if (smartctl["model_name"].startswith("SanDisk SDSSDH3 500G")):
        return 200 * Unit.TiB  # same as WD BLUE 3D
    if (smartctl["model_name"].startswith("Samsung SSD 850 EVO 250GB")):
        return 75 * Unit.TiB  # https://www.samsung.com/semiconductor/minisite/jp/ssd/consumer/850evo/
    if (smartctl["model_name"].startswith("Samsung SSD 850 EVO 500GB")):
        return 150 * Unit.TiB  # https://www.samsung.com/semiconductor/minisite/jp/ssd/consumer/850evo/

    return None

from operator import concat
import os
import glob
import tests.const as const

def is_test_target(filepath):
    base = os.path.basename(filepath)
    return base.startswith("_") == False


def get_json_paths(dir):
    cwd = os.getcwd()
    globspec = os.path.join(cwd, dir, "*.json")

    all = glob.glob(globspec)
    ret = filter(is_test_target, all)
    
    return list(ret)
    


def get_sata_json_paths():
    all = get_json_paths(const.EXAMPLE_DEV_SATA_DIR)   
    return all

def get_nvme_json_paths():
    all = get_json_paths(const.EXAMPLE_DEV_NVME_DIR)
    return all


def get_all_json_paths():
    sata = get_sata_json_paths()
    nvme = get_nvme_json_paths()
    all = sata + nvme

    return all

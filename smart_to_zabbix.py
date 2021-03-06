import interpriters
import json
import logging
import subprocess
from pprint import pprint

import config as cfg
import smartctl_util as smutil

import modules.zabbix_parsed as zbx_parsed
import modules.zabbix_smart as zbx_smart

logger = logging.getLogger(__name__)


# smartctl --scan を実行して結果を返す
#
def exec_smartctl_scan():

    cmd = None

    import platform
    platform = platform.system()
    if platform == 'Windows':
        cmd = cfg.WIN_SMARTCTL_SCAN_CMD.copy()
    else:
        cmd = cfg.LINUX_SMARTCTL_SCAN_CMD.copy()

    if cmd[0] == 'sudo':
        logger.info("Asking your password by sudo")

    scan = subprocess.run(cmd, stdout=subprocess.PIPE)

    # logger.debug(scan.stdout)
    result = json.loads(scan.stdout)
    # logger.debug(result)
    return result


def get_smartctl_device_info_cmd():
    import platform
    platform = platform.system()
    cmd = None
    if platform == 'Windows':
        cmd = cfg.WIN_SMARTCTL_DETAIL_CMD.copy()
    else:
        cmd = cfg.LINUX_SMARTCTL_DETAIL_CMD.copy()

    return cmd


def exec_smartctl_device_info(device_name, device_type):

    result = None
    retcode = 999

    # call smartctl without any option
    if True:
        cmd = get_smartctl_device_info_cmd()
        cmd.append(device_name)
        logger.debug(cmd)

        if device_type.startswith("megaraid"):
            # megaraid
            cmd.extend(["-d", device_type])
        
        proc_info = subprocess.run(cmd, stdout=subprocess.PIPE)
        retcode = proc_info.returncode
        result = json.loads(proc_info.stdout)
        if (retcode > 4):  # 0 = ok , 1 = maybe USB , 2 = megaraid
            raise RuntimeError(f"smartctl return code = {retcode}. cmd = {cmd}")

    # print(result)

    # Unable to Detect
    if (smutil.is_unknown_device(result)):
        logger.warning("Unknown or Not supported device. Ignored: " + device_name)
        return None

    # Device is MegaRaid volume? then, skip it. (check it later by /dev/bus/0, megaraid,N)
    if (smutil.is_megaraid_device(result)):
        return None

    # retry with "-d sat" if device is behind usb converter
    if (smutil.is_usb_device(result)):
        logger.info(f"{device_name} USB Bridge find. retry with -d sat.")
        cmd = get_smartctl_device_info_cmd()
        cmd.extend(["-d", "sat", device_name])
        logger.debug(cmd)
        proc_info = subprocess.run(cmd, stdout=subprocess.PIPE)
        retcode = proc_info.returncode
        result = json.loads(proc_info.stdout)
        if (retcode > 4):  # maybe retcode = 4.
            raise RuntimeError(f"smartctl(usb) return code = {retcode}. cmd = {cmd}")

    return result



def get_detail(device):

    # sender data
    metrics = []
    for d in device:
        key = f"smartmontools.diskname[{d['KEY']}]"
        logger.debugf("get_detail {key}")
        #metrics.append(ZabbixMetric(ZABBIX_HOST, key, d["VALUE"]))

    zbx_parsed.send_to_zabbix(metrics)

    return None


def find_interpriter(device_info):
    # strict match
    for intp in interpriters.SPECIAL_INTERPRITERS:
        if (intp.isTargetDeviceType(device_info) and intp.isTargetStrict(device_info)):
            return intp

    # loose match
    for intp in interpriters.SPECIAL_INTERPRITERS:
        if (intp.isTargetDeviceType(device_info) and intp.isTargetLoose(device_info)):
            return intp

    # basic
    for intp in interpriters.BASIC:
        if (intp.isTargetDeviceType(device_info)):
            return intp

    logger.error(
        f"No interpriters (No basic interpriter applied) => {dev} {device_info['model_name']}")
    raise RuntimeError("No interpriters")


def assign_device_id(device_info):
    """       
    デバイスを一意に識別できるIDを決める
    /dev/sda などは認識順なので一意ではないのでできれば使いたくない
    """
    # "device": {
    #   "name": "/dev/bus/0",
    #   "info_name": "/dev/bus/0 [megaraid_disk_00] [SAT]",
    #   "type": "sat+megaraid,0",
    # },
    if (device_info.get("serial_number") != None):
        return device_info["serial_number"]   # シリアル番号があればそれ

    # fallback
    dev = device_info["device"]  # さすがにこれがないのは無い
    if dev["name"].startswith("/dev/bus/"):
        return dev["name"] + dev["type"]
        
    return dev["name"]


if __name__ == '__main__':

    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"

    if (cfg.LOG_LEVEL.upper() == "ERROR"):
        logging.basicConfig(level=logging.ERROR, format=fmt)
    elif (cfg.LOG_LEVEL.upper() == "WARN"):
        logging.basicConfig(level=logging.WARN, format=fmt)
    elif (cfg.LOG_LEVEL.upper() == "INFO"):
        logging.basicConfig(level=logging.INFO, format=fmt)
    else:
        logging.basicConfig(level=logging.DEBUG, format=fmt)

    logger.info("START")

    # scan_resultだけでdiscoveryを送信したいが、model_name等情報が足りない
    # のですべての結果を取得するまでdevice discoveryを送信できない
    # scan_resultは明細を取るためだけに使用されて、zabbixへのデータ送信には使われない。
    scan_result = exec_smartctl_scan()

    full_results = {}
    parsed_results = {}

    for device in scan_result["devices"]:
        dev = device["name"]
        dev_type = device["type"]
        logger.info(f"Checking device {dev} type {dev_type}")
        device_info = exec_smartctl_device_info(dev, dev_type)
        if device_info == None:
            # megaraid device
            continue

        dev_id = assign_device_id(device_info)
        
        full_results[dev_id] = device_info
        interpriter = find_interpriter(device_info)
        parsed_results[dev_id] = interpriter.parse(device_info)

    # デバイスディスカバリを送信
    zbx_parsed.send_device_discovery(parsed_results)

    # パース成功したデータを扱う
    zbx_parsed.send_parsed_data(parsed_results)

    # SMART discovery と SMART全データを送信する
    zbx_smart.send_attribute_discovery(full_results)
    zbx_smart.send_smart_data(full_results)

    logger.info("END")

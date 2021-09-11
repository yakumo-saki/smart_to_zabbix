import interpriters
import json
import logging
import subprocess
from pprint import pprint

import config as cfg

import modules.zabbix_parsed as zbx_parsed
import modules.zabbix_smart as zbx_smart

logger = logging.getLogger(__name__)


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


def is_usb_device(smartctl_result):
    if ("smartctl" not in smartctl_result):
        return False

    if ("messages" not in smartctl_result["smartctl"]):
        return False

    for msg in smartctl_result["smartctl"]["messages"]:
        if ("Unknown USB bridge" in msg["string"]):
            return True
    
    return False


def exec_smartctl_device_info(device_name):

    result = None
    retcode = 999

    if True:
        cmd = get_smartctl_device_info_cmd()
        cmd.append(device_name)
        logger.debug(cmd)
        device_info = subprocess.run(cmd, stdout=subprocess.PIPE)
        retcode = device_info.returncode
        result = json.loads(device_info.stdout)

    print(result)

    # retry with "-d sat" if device is behind usb converter
    if (is_usb_device(result)):
        logger.info(f"{device_name}: USB Bridge find. retry with -d sat.")
        cmd = get_smartctl_device_info_cmd()
        cmd.extend(["-d sat", device_name])
        retry_dev_info = subprocess.run(cmd, stdout=subprocess.PIPE)
        retcode = retry_dev_info.returncode


    if (retcode != 0):
        raise RuntimeError(f"smartctl return code = {device_info.returncode}. Command: " + json.dumps(cmd))

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


if __name__ == '__main__':

    if (cfg.LOG_LEVEL.upper() == "ERROR"):
        logging.basicConfig(level=logging.ERROR)
    elif (cfg.LOG_LEVEL.upper() == "WARN"):
        logging.basicConfig(level=logging.WARN)
    elif (cfg.LOG_LEVEL.upper() == "INFO"):
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)

    logger.info("START")

    # scan_resultだけでdiscoveryを送信したいが、model_name等情報が足りない
    scan_result = exec_smartctl_scan()

    full_results = {}
    parsed_results = {}

    for device in scan_result["devices"]:
        dev = device["name"]
        logger.info(f"Checking device {dev}")
        device_info = exec_smartctl_device_info(device["name"])
        full_results[dev] = device_info

        interpriter = find_interpriter(device_info)

        parsed_results[dev] = interpriter.parse(device_info)

    # パース成功したデータを扱う
    zbx_parsed.send_device_discovery(parsed_results)
    zbx_parsed.send_parsed_data(parsed_results)

    # SMART全データを送信する
    zbx_smart.send_attribute_discovery(full_results)
    zbx_smart.send_smart_data(full_results)

    logger.info("END")

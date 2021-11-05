import logging

logger = logging.getLogger(__name__)


# smartctl のエラーメッセージのリストを返します。
# エラーメッセージがない場合は空のリストを返します。
# @return [{"string": "this is message", "severity": "error"}]
def get_smartctl_messages_from_result(smartctl_result):
    if ("smartctl" not in smartctl_result):
        return []

    if ("messages" not in smartctl_result["smartctl"]):
        return []

    return smartctl_result["smartctl"]["messages"]

# エラーメッセージにパラメタの単語が含まれたものが一つでもあるか否かを返します。
def _message_contains(smartctl_result, checkString):
    msgs = get_smartctl_messages_from_result(smartctl_result)
    if msgs == None:
        return False

    for msg in msgs:
        if (checkString in msg["string"]):
            return True

    return False

def is_usb_device(smartctl_result):
    return _message_contains(smartctl_result, "Unknown USB bridge")

def is_megaraid_device(smartctl_result):
    return _message_contains(smartctl_result, "DELL or MegaRaid controller")

def is_unknown_device(smartctl_result):
    return _message_contains(smartctl_result, "Unable to detect device type")
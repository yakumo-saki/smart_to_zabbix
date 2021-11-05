

# smartctl のエラーメッセージのリストを返します。
# エラーメッセージがない場合は空のリストを返します。
# @return [{"string": "this is message", "severity": "error"}]
def get_smartctl_messages_from_result(smartctl_result):
    if ("smartctl" not in smartctl_result):
        return []

    if ("messages" not in smartctl_result["smartctl"]):
        return []

    return smartctl_result["smartctl"]["messages"]

def is_usb_device(smartctl_result):
    msgs = get_smartctl_messages_from_result(smartctl_result)

    for msg in msgs:
        if ("Unknown USB bridge" in msg["string"]):
            return True
    
    return False

def is_megaraid_device(smartctl_result):

    msgs = get_smartctl_messages_from_result(smartctl_result)

    for msg in msgs:
        if ("DELL or MegaRaid controller" in msg["string"]):
            return True
    
    return False

import os
import load_dotenv

load_dotenv.load_env_from_file()

# 環境変数を読む。 
ZABBIX_SERVER = os.environ.get('ZABBIX_SERVER', None)
ZABBIX_PORT = int(os.environ.get('ZABBIX_PORT', "10051"))
ZABBIX_HOST = os.environ.get('ZABBIX_HOST', None)
LOG_LEVEL = os.environ.get('LOG_LEVEL', "DEBUG")

# 以下はZabbixテンプレートと整合性を取る必要がある

#  
LINUX_SMARTCTL_SCAN_CMD = ['sudo', 'smartctl', '--json', '--scan', '-d', 'sat', '-d', 'nvme', '-d', 'ata']
LINUX_SMARTCTL_DETAIL_CMD = ['sudo', 'smartctl', '--json', '-a']

# 
WIN_SMARTCTL_SCAN_CMD = ['smartctl', '--json', '--scan', '-d', 'sat', '-d', 'nvme', '-d', 'ata']
WIN_SMARTCTL_DETAIL_CMD = ['smartctl', '--json', '-a']

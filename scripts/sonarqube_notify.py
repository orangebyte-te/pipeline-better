import json
import os
import sys
import requests

project = sys.argv[1]
skip_error = (sys.argv[2].lower() == 'true') if len(sys.argv) > 2 else False
sonar_host = os.environ['SONAR_HOST_URL'].rstrip('/')
sonar_token = os.environ['SONAR_TOKEN']
dingtalk_webhook = os.environ.get('DINGTALK_WEBHOOK', '')

metrics = 'alert_status,bugs,vulnerabilities,code_smells,new_coverage,duplicated_lines_density,security_hotspots'
url = f"{sonar_host}/api/measures/search?projectKeys={project}&metricKeys={metrics}"
resp = requests.get(url, auth=(sonar_token, ''), timeout=20)
resp.raise_for_status()
data = resp.json()
values = {item['metric']: item.get('value') or item.get('period', {}).get('value', '-') for item in data.get('measures', [])}
status = values.get('alert_status', 'UNKNOWN')
text = (
    f"项目: {project}\n"
    f"状态: {status}\n"
    f"Bug: {values.get('bugs','-')}\n"
    f"漏洞: {values.get('vulnerabilities','-')}\n"
    f"安全热点: {values.get('security_hotspots','-')}\n"
    f"代码异味: {values.get('code_smells','-')}\n"
    f"新代码覆盖率: {values.get('new_coverage','-')}%\n"
    f"重复率: {values.get('duplicated_lines_density','-')}%\n"
    f"详情: {sonar_host}/dashboard?id={project}"
)
print(text)
if dingtalk_webhook:
    requests.post(dingtalk_webhook, json={"msgtype": "text", "text": {"content": text}}, timeout=20).raise_for_status()
if status == 'ERROR' and not skip_error:
    sys.exit(1)

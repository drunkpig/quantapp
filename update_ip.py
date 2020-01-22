import socket
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import time
from datetime import datetime

# 多网卡情况下，根据前缀获取IP（Windows 下适用）
def GetLocalIPByPrefix(prefix):
    localIP = ''
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith(prefix):
            localIP = ip

    return localIP


def update_ip():
    ip = GetLocalIPByPrefix("192.168")
    key = "Ba5LTZnQLZNz2SXf"
    domain = "stockapi.mkmerich.com"
    url = f"https://{domain}:{key}@dyn.dns.he.net/nic/update?hostname={domain}&myip={ip}"

    ctx = requests.get(url)
    print(f"Update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, ip={ip}")
    print(ip)
    print(ctx.text)


if __name__=="__main__":
    time_zone = timezone("Asia/Shanghai")
    scheduler = BackgroundScheduler(timezone=time_zone)
    trigger = CronTrigger.from_crontab("*/5  *  * * *", timezone=time_zone)
    scheduler.add_job(update_ip, trigger)
    scheduler.start()
    while True:
        #print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(50)

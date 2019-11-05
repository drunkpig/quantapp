import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from logging.config import fileConfig
import logging

time_zone = timezone("Asia/Shanghai")
scheduler = BackgroundScheduler(timezone=time_zone)
trigger = CronTrigger.from_crontab(cron, timezone=time_zone)
scheduler.add_job(m_func, trigger, kwargs=func_arg)

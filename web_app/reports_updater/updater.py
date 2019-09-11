from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os

project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
crawler_path = os.path.join(project_root_path, 'web_crawler')

def update_reports_sh():
    bashCommand = "cd " + crawler_path + "\n"
    bashCommand += "python -m scrapy crawl ases --set LOG_LEVEL=WARNING --logfile log.txt\n"
    os.system(bashCommand)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_reports_sh, 'interval', hours=1)
    scheduler.start()
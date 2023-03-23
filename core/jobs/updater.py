from apscheduler.schedulers.background import BackgroundScheduler

from .jobs import check_old_requests

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_old_requests , 'interval' ,  seconds=10)
    scheduler.start()
    
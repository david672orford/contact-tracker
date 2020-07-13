from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import timedelta, date
import logging

from .models import db, Contacts

logger = logging.getLogger(__name__)

def expire_info():
	logger.info("Expiring data...")
	cutoff = (date.today() - timedelta(days=30))
	Contacts.query.filter(Contacts.date < cutoff).delete()
	db.session.commit()

def job_event(event):
	logger.info("Rolling back transaction...")
	db.session.rollback()

logger.info("Staring scheduler...")
scheduler = BackgroundScheduler()
scheduler.add_listener(job_event, EVENT_JOB_ERROR)
scheduler.start()
scheduler.add_job(id="expire_info", func=expire_info, trigger=CronTrigger(hour=0, minute=15))


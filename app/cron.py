#
# Copyright 2020 David Chappell
# This file is part of Content Tracker.
#
# Content Tracker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Content Tracker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Contact Tracker. If not, see <https://www.gnu.org/licenses/>.
#

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


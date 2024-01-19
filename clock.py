#!/usr/bin/env python

from apscheduler.schedulers.blocking import BlockingScheduler

from bot import notify

sched = BlockingScheduler()


@sched.scheduled_job(
    'cron', id='notify', day_of_week='tue,sat', hour=10, timezone='Europe/Rome'
)
def scheduled_job():
    notify()


sched.start()
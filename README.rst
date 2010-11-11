===========================================
Django tracker - Track users actions
===========================================

:Version: 0.0.1

Introduction
============

This package is gonna give you an easy tool to track users
actions on your website. You choose a label for an action and everytime
a user do this action you call the backend tracking method::

    tracker = Tracker()
    tracker.incr_labels("user_connected|user_clicked_button")
    tracker.save()

This action will increment the counter for the "user_connected" and the "user_clicked_button" label.
You can also call the tracker from javascript if you install the tracker view::

    from tracker.views import track, report

    urlpatterns = patterns('',
        ...
        (r'^track/', track),
    )

And then you can visit the `/track/?labels=user_connected|user_clicked_button` and it will have the same effect.

Django tracker is easy on the database and is architectured to use memcache to count every action. To collect the
memcache informations you will need to do one of these::

 * Setup and call the `report` view every 2 minutes
 * Setup a cron that call tracker.models.make_daily_report function every 2 minutes
 * Setup the Celery task that is provided in `tracker.tasks`.

It also mean that you need to use memcache or at least the locmem cache backend (only if you have 1 server).
It might work with a database cache but it will not be the best configuration.

Installation
============

    # python setup.py install # as root



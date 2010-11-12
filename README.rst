===========================================
Django tracker - Track users actions
===========================================

:Version: 0.0.1

Introduction
============

This package is gonna give you an easy tool to track anonymous user
actions on your website. You choose a label for an action and everytime
a user do this action you call the backend tracking method::

    from tracker.models import Tracker
    tracker = Tracker()
    tracker.incr_labels("user_connected|user_clicked_button")

This action will increment the counter for the "user_connected" and the "user_clicked_button" label.
You can also call the tracker from javascript if you install the tracker view::

    from tracker.views import track, report

    urlpatterns = patterns('',
        ...
        (r'^track/', track),
    )

And then you can visit the `/track/?labels=user_connected|user_clicked_button` and it will have the same effect. e.g. with jQuery::

    function track(labels) {
        $.ajax({
            url: '/track/?labels='+labels,
            dataType: 'text',
            type: "GET",
            error:function (xhr) {
            }
        });
    }

    track('user_connected|user_clicked_button')

You can also specify 2 extra informations separated by a colon::

    track('user_connected:category:domId')

The category will help in the admin interface to filter your statistics. The dom id
can be used on a page to create a heat map. Here is an example of how to use the data::

    <div id="tracked-links">
    <a href="#1" id="link1">Test link 1</a>
    <a href="#2" id="link2">Test link 2</a>
    <a href="#3" id="link3">Test link 3</a>
    <a href="#4" id="link4">Test link 4</a>
    </div>

    <p><a href="/report/">Report the clicks in the database</a></p>
    <p><a href="#" id="get-stats">Get the statistics</a></p>

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script>
        $('#tracked-links a').click(function(e) {
            track('tracked-links-'+this.id+':links:'+this.id);
        })

        $('#get-stats').click(function(){
            var dom_ids = "";
            $.each($('#tracked-links a'), function(index, value) {
                dom_ids += value.id + '|';
            });
            $.ajax({
                url: '/get_stats/?dom_ids='+dom_ids,
                dataType: 'json',
                type: "GET",
                error:function (xhr) {
                },
                success: function(data, textStatus, XMLHttpRequest) {
                    for(stat in data) {
                        var id = data[stat][0];
                        var counter = data[stat][1];
                        var label = data[stat][2];
                        $('#'+id).text('clicked '+counter+ ' time.')
                    }
                }
            });

        });

    </script>

This little script gather the id in the "tracked-links" div make a request to the server to get the
statistics about them. The counter is then displayed inside the links. Take a look at the testproj
for an example.


How does it work?
==================

Django tracker is easy on the database and is architectured to use memcache to count every action. To collect the
memcache informations you will need to do one of these::

 * Setup and call the `report` view every 2 minutes
 * Setup a cron that call tracker.models.make_daily_report function every 2 minutes
 * Setup the Celery task that is provided in `tracker.tasks`.

It also mean that you need to use memcache or at least the locmem cache backend (only if you have 1 server).
It might work with a database cache but it will not be the best configuration.

All the informations are stored in daily Statistic models (1 record by label and by day). Those models can be used directly in the admin interface
to examine interesting metrics of your website.

Installation
============

    # python setup.py install # as root



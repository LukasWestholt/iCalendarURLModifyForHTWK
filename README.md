# iCalendarURLModify for HTWK

This app is modifying the HTWK calendar by [`htwk-stundenplan.de`](http://www.htwk-stundenplan.de/de/) on-the-fly.

Feel free to use :)

# HOWTO

start flask server and go to /calendar/modify/<prof_schwarz_group>/?id=<id>

## Info
You can [check](https://icalendar.org/validator.html) the validity of icalendar files.
You can [compare](/diff_tester.py) icalendar files.
# Credits

Credits go to [htwk-stundenplan.de](http://www.htwk-stundenplan.de/de/). See on [GitHub](https://github.com/LeEnno/htwk2ical).

For the `icalendar` lib in python I used a script by [adamgreig](https://gist.github.com/adamgreig/a5eada2934d19189c0f6).
You can find it also [here](/template/icalcombine.py).

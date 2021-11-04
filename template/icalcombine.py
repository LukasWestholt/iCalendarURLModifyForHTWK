#!/usr/bin/env python
"""
iCal Combine

./icalcombine.py <input URLs file> <output filename>

Read ICS (iCAL) URLs, one per line, from the <input URLs files>, then combine
into a single iCal which is written to <output filename>.
"""
import sys
import datetime

import pytz
import requests
from icalendar import Calendar, Event

now = datetime.datetime.utcnow()
now.replace(tzinfo=pytz.utc)

today = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).date()

if len(sys.argv) != 3:
    print("Usage: {} <iCal URL file> <output filename>"
          .format(sys.argv[0]))
    sys.exit(1)

urls = [url.strip() for url in open(sys.argv[1]).readlines()]

combined_cal = Calendar()
combined_cal.add('prodid', '-//icalcombine//NONSGML//EN')
combined_cal.add('version', '2.0')
combined_cal.add('x-wr-calname', "Adam's Combined Calendar")

for url in urls:
    req = requests.get(url)
    if req.status_code != 200:
        print("Error {} fetching {}: {}"
              .format(url, req.status_code, req.text))
        continue

    cal = Calendar.from_ical(req.text)
    for event in cal.walk("VEVENT"):
        end = event.get('dtend')
        if end:
            if hasattr(end.dt, 'date'):
                date = end.dt.date()
            else:
                date = end.dt
            if date >= today or 'RRULE' in event:
                copied_event = Event()
                for attr in event:
                    if type(event[attr]) is list:
                        for element in event[attr]:
                            copied_event.add(attr, element)
                    else:
                        copied_event.add(attr, event[attr])
                combined_cal.add_component(copied_event)

with open(sys.argv[2], "wb") as f:
    f.write(combined_cal.to_ical())
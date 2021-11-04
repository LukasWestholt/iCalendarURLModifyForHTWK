#!/usr/bin/env python
"""
./iCalendarURL.py <input URL> <output filename>

Read ICS (iCAL) URL, then modify. Write ICS result to <output filename>.
"""

import sys
import requests
import icalendar
import re
import datetime


def modify(calendar_id, prof_schwarz_group):
    url = "http://www.htwk-stundenplan.de/" + calendar_id + "/"
    req = requests.get(url)
    if req.status_code != 200:
        print("Error {} fetching {}: {}"
              .format(url, req.status_code, req.text))
        return False

    new_cal = icalendar.Calendar()
    cal = icalendar.Calendar.from_ical(req.text)

    for event in cal.walk("VEVENT"):
        desc = event.get('DESCRIPTION')
        if desc and re.search(r"\s*SCHWARZ.*Gr.\s*([" +
                              "".join([str(y) if y != prof_schwarz_group else "" for y in range(1, 4)]) +
                              r"]).*", desc):
            pass
        else:
            copied_event = icalendar.Event()
            for attr in event:
                if type(event[attr]) is list:
                    for element in event[attr]:
                        copied_event.add(attr, element)
                else:
                    copied_event.add(attr, event[attr])
            new_cal.add_component(copied_event)

    new_cal.add_component(icalendar_timezone())
    new_cal.add('X-WR-CALDESC', calendar_id)
    new_cal.add('X-WR-CALNAME', calendar_id)
    new_cal.add('X-WR-TIMEZONE', 'Europe/Berlin')
    new_cal.add('PRODID', '-//htwk-stundenplan.de//ENNOCAL 2.1//DE')
    new_cal.add('CALSCALE', 'GREGORIAN')
    new_cal.add('VERSION', '2.0')

    return new_cal.to_ical()


def icalendar_timezone():
    tzc = icalendar.Timezone()
    tzc.add('tzid', 'Europe/Berlin')
    tzc.add('x-lic-location', 'Europe/Berlin')
    tzs = icalendar.TimezoneStandard()
    tzs.add('tzname', 'CET')
    tzs.add('dtstart', datetime.datetime(1970, 10, 25, 3, 0, 0))
    tzs.add('rrule', {'freq': 'yearly', 'bymonth': 10, 'byday': '-1su'})
    tzs.add('TZOFFSETFROM', datetime.timedelta(hours=2))
    tzs.add('TZOFFSETTO', datetime.timedelta(hours=1))
    tzd = icalendar.TimezoneDaylight()
    tzd.add('tzname', 'CEST')
    tzd.add('dtstart', datetime.datetime(1970, 3, 29, 2, 0, 0))
    tzs.add('rrule', {'freq': 'yearly', 'bymonth': 3, 'byday': '-1su'})
    tzd.add('TZOFFSETFROM', datetime.timedelta(hours=1))
    tzd.add('TZOFFSETTO', datetime.timedelta(hours=2))

    tzc.add_component(tzs)
    tzc.add_component(tzd)
    return tzc


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: {} <ICS URL> <output filename>"
              .format(sys.argv[0]))
        sys.exit(1)

    with open(sys.argv[2], "wb") as file:
        file.write(modify(sys.argv[1].strip(), 1))

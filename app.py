# app.py
from flask import Flask, make_response, request
import iCalendarURL
import consts

app = Flask(__name__)


@app.get("/calendar/modify/")
@app.get("/calendar/modify/<prof_schwarz_group>/")
def calendar_modify(prof_schwarz_group=None):

    prof_schwarz_group = prof_schwarz_group or request.args.get('prof_schwarz_group')
    if not prof_schwarz_group:
        return "prof_schwarz_group not found", consts.HTTP_400_BAD_REQUEST
    try:
        prof_schwarz_group = int(prof_schwarz_group)
    except TypeError:
        return "prof_schwarz_group is no integer", consts.HTTP_400_BAD_REQUEST
    if prof_schwarz_group > 3 or prof_schwarz_group < 1:
        return "prof_schwarz_group must be 1, 2 or 3", consts.HTTP_400_BAD_REQUEST

    calendar_id = request.args.get('id')
    if not calendar_id:
        return "id not found", consts.HTTP_400_BAD_REQUEST
    try:
        calendar_id = str(calendar_id)
    except TypeError:
        return "id is no string", consts.HTTP_400_BAD_REQUEST

    calendar = iCalendarURL.modify(calendar_id, prof_schwarz_group)
    response = make_response(calendar)
    response.headers["Content-Type"] = "text/calendar"
    response.headers["Content-Disposition"] = "attachment; filename=ModifiedHTWK2iCal.ics"
    return response

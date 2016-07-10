"""
Provides functionality for sending reminder email to user to book a cab based on user's given preferences
"""
from __future__ import print_function

import sys
from datetime import timedelta
from math import ceil
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler

from app import input_validator, web_service, email_util
from app.uber_request import UberRequest


def set_uber_reminder(request_info, socketio):
    """
    Checks for a valid request from user and schedules the reminder
    :param request_info: dict containing user input parameters
    :param socketio: flask socketio object
    :return: dict with status of processed request
    """
    print("request received from client", file=sys.stderr)
    is_valid, errors = input_validator.InputValidator.validate_inputs(request_info)
    if not is_valid:
        yield {"valid": is_valid, "errors": errors}
    else:
        req_obj = UberRequest(request_info)
        if req_obj.time.now() > req_obj.arrival_time:
            errors.append("Arrival time has already passed.")
            yield {"valid": False, "errors": errors}
        else:
            uber_time, google_time = get_uber_and_google_times(req_obj, socketio)
            total_commute_time = ceil(uber_time + google_time)
            if total_commute_time <= 0:
                errors.append("Cab not available at this location")
                yield {"valid": False, "errors": errors}
            elif total_commute_time > req_obj.time.difference(req_obj.time.now(), req_obj.arrival_time):
                errors.append("Not a valid request. You cannot reach on time")
                yield {"valid": False, "errors": errors}
            else:
                yield {"valid": is_valid, "errors": errors}
                print("after yield", file=sys.stderr)
                scheduler = BackgroundScheduler()
                estimated_time_to_schedule = req_obj.arrival_time - timedelta(minutes=int(total_commute_time) + 60)
                current_time = req_obj.time.now()
                if current_time > estimated_time_to_schedule:
                    print("Reminder check scheduled for ", current_time, file=sys.stderr)
                    scheduler.add_job(remind_user_with_email, 'date',
                                      next_run_time=current_time + timedelta(seconds=10),
                                      args=[req_obj, socketio, uber_time, google_time])
                else:
                    print("Reminder check scheduled for ", estimated_time_to_schedule, file=sys.stderr)
                    scheduler.add_job(remind_user_with_email, 'date', next_run_time=estimated_time_to_schedule, args=[req_obj, socketio])
                scheduler.start()


def remind_user_with_email(cab_request, socketio, uber_time=None, google_time=None):
    """
    Checks for most optimized time to remind user to book the cab
    :param cab_request: dict containing user input parameters
    :param socketio: flask socketio object
    :param uber_time: datetime object
    :param google_time: datetime object
    """
    if not uber_time and not google_time:
        uber_time, google_time = get_uber_and_google_times(cab_request, socketio)
    print("uber ", uber_time, " map ", google_time, file=sys.stderr)
    total_commute_time = int(ceil(google_time + uber_time))
    cab_request.departure_time = cab_request.arrival_time - timedelta(minutes=total_commute_time)
    time_left_to_send_mail = cab_request.time.difference(cab_request.time.now(), cab_request.departure_time)
    while time_left_to_send_mail >= uber_time:
        wait_time = 10 if time_left_to_send_mail > 35 else 5
        sleep_time = max(min(time_left_to_send_mail, wait_time), uber_time)
        print("Checking for status again in", sleep_time, "minutes. Current time:: ", cab_request.time.now(),
              cab_request.recipient, file=sys.stderr)
        sleep(sleep_time * 60)
        uber_time, google_time = get_uber_and_google_times(cab_request, socketio)
        total_commute_time = int(ceil(google_time + uber_time))
        cab_request.departure_time = cab_request.arrival_time - timedelta(minutes=total_commute_time)
        time_left_to_send_mail = cab_request.time.difference(cab_request.time.now(), cab_request.departure_time)
    print("Sending email to " + cab_request.recipient, file=sys.stderr)
    email_util.send_email([cab_request.recipient])


def get_uber_and_google_times(cab_request, socktio):
    """
    Checks for maps api and uber api to fetch the required details
    :param cab_request: dict containing user input parameters
    :param socketio: flask socketio object
    :return: eta for uber and transit time using google maps
    """
    uber_time = web_service.get_cab_eta(cab_request, socktio)
    google_time = web_service.get_google_transit_estimation(cab_request, socktio)
    return uber_time, google_time

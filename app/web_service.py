"""
Provides API client for different services
"""
from __future__ import print_function

import requests

from app.app_util import ConfigurationParser

TIME_FORMAT = "%I:%M %p"
CONFIG_HEADER = "api.settings"


def get_cab_eta(uber_request, socketio, cab_type="uberGO"):
    """
    Fetches ETA for a uber cab in a given location
    :param uber_request: uber request object
    :param cab_type: string type of uber cab for which ETA is needed
    :param socketio: flask socketio object
    :return: float estimated arrival time in minutes
    """
    socketio.emit("api_logs",
                  "[{0}] Called Uber api for email {1}".format(uber_request.time.now().strftime(TIME_FORMAT),
                                                               uber_request.recipient), broadcast=True)
    config = ConfigurationParser.get_config_object()
    url = 'https://api.uber.com/v1/estimates/time'
    parameters = {
        'server_token': config.get(CONFIG_HEADER, "UBER_API_KEY"),
        'start_latitude': uber_request.source_lat,
        'start_longitude': uber_request.source_long,
    }
    response = requests.get(url, params=parameters)
    cab_eta = -99999  # Negative value to signify cab isn't avaialble at the given location
    data = response.json().get("times")
    for cabs in data:
        if cabs.get("display_name") == cab_type:
            cab_eta = float(cabs.get("estimate")) / 60
    return cab_eta


def get_google_transit_estimation(uber_request, socketio):
    """
    Fetches estimated time to reach from one geographical coordinate to another using Google's services
    :param uber_request: uber request object
    :param socketio: flask socketio object
    :return: float time to travel between two places in minutes
    """
    socketio.emit("api_logs",
                  "[{0}] Called Google api for email {1}".format(uber_request.time.now().strftime(TIME_FORMAT),
                                                                 uber_request.recipient), broadcast=True)
    orig_coord = "{0},{1}".format(uber_request.source_lat, uber_request.source_long)
    dest_coord = "{0},{1}".format(uber_request.dest_lat, uber_request.dest_long)
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(
        orig_coord, dest_coord)
    transit_response = requests.get(url)
    transit_details = transit_response.json()
    transit_time = float(transit_details.get("rows")[0].get("elements")[0].get("duration").get("value")) / 60
    return transit_time

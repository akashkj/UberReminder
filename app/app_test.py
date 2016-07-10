from app.uber_request import UberRequest
from app import uber_reminder


if __name__ == '__main__':
    req = {"source_lat": "12.927880", "source_long": "77.627600",
           "dest_lat": "13.035542", "dest_long": "77.597100",
           "recipient": "akashjain1708@gmail.com",
           "arrival_time": "23:58"}
    print "req ", req
    for entry in uber_reminder.set_uber_reminder(req):
        print "entry", entry
    print "out"


from app.app_time import Time


class UberRequest(object):
    def __init__(self, request_dict):
        """
        :param request_dict: dict containing request from the user
        """
        self.source_lat = float(request_dict.get("source_lat", ""))
        self.source_long = float(request_dict.get("source_long", ""))
        self.dest_lat = float(request_dict.get("dest_lat", ""))
        self.dest_long = float(request_dict.get("dest_long", ""))
        self.recipient = request_dict.get("recipient", "")
        self.time = Time(request_dict.get("timezone", "Asia/Kolkata"))
        self.arrival_time = self.time.string_to_time(request_dict.get("arrival_time", ""))
        self.departure_time = None

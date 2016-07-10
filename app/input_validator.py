"""
Validates input parameters received from the user
"""


class InputValidator(object):
    """
    Validator class
    """

    @staticmethod
    def validate_inputs(request_info):
        """
        Control class to validate different types of inputs and returns validation result
        :param request_info: dict user preferences
        :return: boolean and list of strings
        """
        is_valid = True
        validation_errors = []
        src_lat = InputValidator._validate_latitude(request_info.get("source_lat"), "Source latitude",
                                                    validation_errors)
        src_long = InputValidator._validate_latitude(request_info.get("source_long"), "Source longitude",
                                                     validation_errors)
        dest_lat = InputValidator._validate_longitude(request_info.get("dest_lat"), "Destination latitude",
                                                      validation_errors)
        dest_long = InputValidator._validate_longitude(request_info.get("dest_long"), "Destination longitude",
                                                       validation_errors)
        time = InputValidator._validate_time(request_info.get("arrival_time"), "Time", validation_errors)
        email = InputValidator._validate_email(request_info.get("recipient"), "Time", validation_errors)
        if all([src_lat, src_long, dest_lat, dest_long, time, email]):
            return True, validation_errors
        return False, validation_errors

    @staticmethod
    def _validate_latitude(input_lat, field_name, validation_errors):
        """
        Validates latitude
        :param input_lat: string latitude
        :param field_name: string input name
        :param validation_errors: list of strings
        :return: boolean for valid latitude
        """
        try:
            input_float = float(input_lat)
            if -90.0 <= input_float <= 90.0:
                return True
            validation_errors.append("{} is not in the allowed range".format(field_name))
            return False
        except ValueError:
            validation_errors.append("{} is invalid latitude format".format(field_name))
            return False

    @staticmethod
    def _validate_longitude(input_long, field_name, validation_errors):
        """
        Validates longitude
        :param input_longt: string longitude
        :param field_name: string input name
        :param validation_errors: list of strings
        :return: boolean for valid longitude
        """
        try:
            input_float = float(input_long)
            if -180.0 <= input_float <= 180.0:
                return True
            validation_errors.append("{} is not in the allowed range".format(field_name))
            return False
        except ValueError:
            validation_errors.append("{} is invalid longitude format".format(field_name))
            return False

    @staticmethod
    def _validate_time(input_time, field_name, validation_errors):
        """
        Validates time
        :param input_lat: string time
        :param field_name: string input name
        :param validation_errors: list of strings
        :return: boolean for valid time
        """
        try:
            hours, minutes = map(int, input_time.split(":"))
            if 0 <= hours <= 23 and 0 <= minutes <= 59:
                return True
            validation_errors.append("{} is not in the allowed range".format(field_name))
            return False
        except (ValueError, AttributeError):
            validation_errors.append("{} is invalid HH:MM format".format(field_name))
            return False

    @staticmethod
    def _validate_email(input_email, field_name, validation_errors):
        """
        Validates email
        :param input_lat: string email
        :param field_name: string input name
        :param validation_errors: list of strings
        :return: boolean for valid email
        """
        if not len(input_email):
            validation_errors.append("Invalid email")
            return False
        split_1 = input_email.split("@")
        if len(split_1) != 2:
            validation_errors.append("Invalid email")
            return False
        split_2 = split_1[1].split(".")
        if len(split_2) != 2:
            validation_errors.append("Invalid email")
            return False
        if len(split_1[0]) < 3 or len(split_2[0]) < 3 or len(split_2[1]) < 3:
            validation_errors.append("Invalid email")
            return False
        return True

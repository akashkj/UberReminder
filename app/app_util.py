"""
Utility configuration parser object provider
"""
import ConfigParser
import logging


class ConfigurationParser(object):
    """
    Utility class for configuration parser object provider
    """

    CONFIG_OBJECT = None

    @classmethod
    def get_config_object(cls):
        """
        :return: configuration file reader object
        """
        if not cls.CONFIG_OBJECT:
            config = ConfigParser.ConfigParser()
            try:
                config.read("app_config.properties")
            except (IOError, ConfigParser.NoSectionError, ConfigParser.NoOptionError) as err:
                logging.error("Error in reading configuration file %s" % err)
                return
            cls.CONFIG_OBJECT = config
        return cls.CONFIG_OBJECT

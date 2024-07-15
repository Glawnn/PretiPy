""" Alert class for creating alert messages """

from typing import Union

from prettypi.pretty_print.emojis import Emoji


class Alert:
    """Alert class for creating alert messages
    * Use static methods to create different types of alerts (info, warning, error, success)
    * Use Alert class to create custom alerts with custom emojis
    * You can custom your messages with other elements present in the pretty_print module
    * You can also surround your prefix with :
        surround_prefix="left,right" to add more style to your alert

    :param message: The message to display in the alert
    :type message: str

    :param prefix: The emoji to display before the message
    :type prefix: Union[Emoji | str]

    :param surround_prefix: The string to surround the prefix with,
                            surround_prefix="left,right", default is " ,"
    :type surround_prefix: str

    :Example:
    >>> from pretty_print import Alert

    >>> alert = Alert.info("This is an information alert")
    >>> print(alert)
    ⚠️ This is an information alert

    >>> custom_alert = Alert("This is a warning alert", prefix="+", surround_prefix=" [,]")
    >>> print(custom_alert)
    [+] This is a warning alert
    """

    def __init__(
        self,
        message: str = "",
        prefix: Union[Emoji | str] = Emoji.INFORMATION,
        surround_prefix: str = " ,",
    ):
        self.surround_prefix = surround_prefix
        self.message = message
        self.prefix = prefix
        self._check_surround_prefix()

    def _check_surround_prefix(self):
        """Check if the surround_prefix is valid"""
        if (
            not self.surround_prefix
            or "," not in self.surround_prefix
            or self.surround_prefix.count(",") > 1
        ):
            raise ValueError("surround_prefix must be of the form 'left,right'")

    def __str__(self):
        left, right = self.surround_prefix.split(",")
        return f"{left}{self.prefix}{right} {self.message}"

    @staticmethod
    def info(message: str = "", surround_prefix: str = " ,"):
        """Create an information alert

        :param message: The message to display in the alert
        :type message: str
        :param surround_prefix: The string to surround the prefix with,
                                surround_prefix="left,right", default is " ,"

        :return: An information alert
        :rtype: Alert
        """
        return Alert(message, Emoji.INFORMATION, surround_prefix)

    @staticmethod
    def warning(message: str = "", surround_prefix: str = " ,"):
        """Create a warning alert

        :param message: The message to display in the alert
        :type message: str
        :param surround_prefix: The string to surround the prefix with,
                                surround_prefix="left,right", default is " ,"

        :return: An information alert
        :rtype: Alert
        """
        return Alert(message, Emoji.WARNING, surround_prefix)

    @staticmethod
    def error(message: str = "", surround_prefix: str = " ,"):
        """Create an error alert

        :param message: The message to display in the alert
        :type message: str
        :param surround_prefix: The string to surround the prefix with,
                                surround_prefix="left,right", default is " ,"

        :return: An information alert
        :rtype: Alert
        """
        return Alert(message, Emoji.CROSS, surround_prefix)

    @staticmethod
    def success(message: str = "", surround_prefix: str = " ,"):
        """Create a success alert

        :param message: The message to display in the alert
        :type message: str
        :param surround_prefix: The string to surround the prefix with,
                                surround_prefix="left,right", default is " ,"

        :return: An information alert
        :rtype: Alert
        """
        return Alert(message, Emoji.CHECK, surround_prefix)

from incoming import datatypes, PayloadValidator


class EventValidator(PayloadValidator):
    action = datatypes.String()
    input = datatypes.JSON(dict)

# encoding: utf-8
from rangersdk.dslclient.json_formatter import JSONFormatter


class Condition(JSONFormatter):
    def __init__(self, value_type, name, operation, values, type_):
        self.property_value_type = value_type
        self.property_name = name
        self.property_operation = operation
        self.property_values = []
        if isinstance(values,list):
            self.property_values.extend(values)
        else:
            self.property_values.append(values)
        self.property_type = type_


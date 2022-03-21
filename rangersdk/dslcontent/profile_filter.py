# encoding: utf-8
from __future__ import annotations
from rangersdk.dslclient.json_formatter import JSONFormatter
from rangersdk.dslcontent.condition import Condition


class Filter(JSONFormatter):
    def __init__(self):
        self.show_name = None
        self.show_label = None
        self.expression = dict(logic=None, conditions=[])

    @staticmethod
    def builder() -> _FilterBuilder:
        return _FilterBuilder(Filter())


class _FilterBuilder(object):
    def __init__(self, profile_filter):
        self.profile_filter = profile_filter

    def set_show_name(self, show_name) -> _FilterBuilder:
        self.profile_filter.show_name = show_name
        return self

    def set_show_label(self, show_label) -> _FilterBuilder:
        self.profile_filter.show_label = show_label
        return self

    def set_show(self, show_label, show_name) -> _FilterBuilder:
        return self.set_show_label(show_label).set_show_name(show_name)

    def set_logic(self, logic) -> _FilterBuilder:
        self.profile_filter.expression['logic'] = logic
        return self

    def set_conditions(self, conditions) -> _FilterBuilder:
        if isinstance(conditions, list):
            self.profile_filter.expression['conditions'].extend(conditions)
        else:
            self.profile_filter.expression['conditions'].append(conditions)
        return self

    def set_string_expr(self, name, operation, values, type_='profile') -> _FilterBuilder:
        return self.set_conditions(Condition('string', name, operation, values, type_))

    def set_int_expr(self, name, operation, values, type_='profile') -> _FilterBuilder:
        return self.set_conditions(Condition('int', name, operation, values, type_))

    def build(self) -> Filter:
        return self.profile_filter

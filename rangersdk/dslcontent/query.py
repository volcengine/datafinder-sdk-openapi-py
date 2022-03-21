# encoding: utf-8
from __future__ import annotations

from rangersdk.dslclient.json_formatter import JSONFormatter


class _QueryBuilder(object):
    def __init__(self, query: Query):
        self.query = query

    def set_sample(self, sample_percent=100) -> _QueryBuilder:
        self.query.sample_percent = sample_percent
        return self

    def set_show_name(self, show_name) -> _QueryBuilder:
        self.query.show_name = show_name
        return self

    def set_show_label(self, show_label) -> _QueryBuilder:
        self.query.show_label = show_label
        return self

    def set_event(self, event_type, event_name, event_indicator=None, event_id=None) -> _QueryBuilder:
        self.query.event_id = event_id
        self.query.event_type = event_type
        self.query.event_name = event_name
        self.query.event_indicator = event_indicator
        return self

    def set_measure_info(self, measure_type, property_name, measure_value) -> _QueryBuilder:
        self.query.measure_info = dict(measure_type=measure_type,
                                       property_name=property_name,
                                       measure_value=measure_value)
        return self

    def set_and_filter(self, exp_builder) -> _QueryBuilder:
        self.query.filters.append(exp_builder.set_logic('and').build())
        return self

    def set_or_filter(self, exp_builder) -> _QueryBuilder:
        self.query.filters.append(exp_builder.set_logic('or').build())
        return self

    def set_group(self, group) -> _QueryBuilder:
        if isinstance(group, list):
            self.query.groups.extend(group)
        else:
            self.query.groups.append(group)
        return self

    def set_group_common_param(self, group) -> _QueryBuilder:
        return self.__set_group_v2(group, "common_param")

    def set_group_event_param(self, group) -> _QueryBuilder:
        return self.__set_group_v2(group, "event_param")

    def __set_group_v2(self, group, property_type: str) -> _QueryBuilder:
        if isinstance(group, list):
            self.query.groups_v2.extend([
                {"property_name": k,
                 "property_type": property_type} for k in group])
        else:
            self.query.groups_v2.append(
                {"property_name": group,
                 "property_type": property_type})
        return self

        return self

    def build(self) -> Query:
        return self.query


class Query(JSONFormatter):
    def __init__(self):
        self.sample_percent = None
        self.show_name = None
        self.show_label = None
        self.event_id = None
        self.event_type = None
        self.event_name = None
        self.event_indicator = None
        self.measure_info = {}
        self.filters = []
        self.groups = []
        self.groups_v2 = []

    @staticmethod
    def builder() -> _QueryBuilder:
        return _QueryBuilder(Query())

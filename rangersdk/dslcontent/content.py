# encoding: utf-8
from __future__ import annotations
from rangersdk.dslclient.json_formatter import JSONFormatter


class Content(JSONFormatter):
    def __init__(self):
        self.query_type = None
        self.profile_filters = []
        self.profile_groups = []
        self.profile_groups_v2 = []
        self.orders = []
        self.page = {}
        self.option = {}
        self.show_option = {}
        self.queries = []

    @staticmethod
    def builder() -> _ContentBuilder:
        return _ContentBuilder(Content())


class _ContentBuilder(object):
    def __init__(self, content):
        self.content = content

    def set_query_type(self, query_type) -> _ContentBuilder:
        self.content.query_type = query_type
        return self

    def set_profile_filter(self, profile_filter) -> _ContentBuilder:
        self.content.profile_filters.append(profile_filter)
        return self

    def set_profile_groups(self, profile_groups) -> _ContentBuilder:
        if isinstance(profile_groups, list):
            self.content.profile_groups.extend(profile_groups)
        else:
            self.content.profile_groups.append(profile_groups)
        return self

    def set_profile_groups_v2(self, profile_groups) -> _ContentBuilder:
        if isinstance(profile_groups, list):
            self.content.profile_groups_v2.extend(profile_groups)
        else:
            self.content.profile_groups_v2.append(profile_groups)
        return self

    def set_orders(self, orders) -> _ContentBuilder:
        if isinstance(orders, list):
            for order in orders:
                if isinstance(order, str):
                    self.content.orders.append({'field': order, 'direction': 'asc'})
                if isinstance(order, dict):
                    self.content.orders.append(order)
                if isinstance(order, tuple):
                    field = order[0]
                    if len(order) == 1:
                        direction = 'asc'
                    else:
                        direction = order[1]
                    self.content.orders.append({'field': field, 'direction': direction})
        else:
            self.content.orders.append(orders)
        return self

    def set_page(self, limit, offset) -> _ContentBuilder:
        self.content.page['limit'] = limit
        self.content.page['offset'] = offset
        return self

    def set_limit(self, limit) -> _ContentBuilder:
        self.content.page['limit'] = limit
        return self

    def set_offset(self, offset) -> _ContentBuilder:
        self.content.page['offset'] = offset
        return self

    def set_option(self, key, value) -> _ContentBuilder:
        self.content.option[key] = value
        return self

    def set_show_option(self, key, value) -> _ContentBuilder:
        self.content.show_option[key] = value
        return self

    def set_query(self, query) -> _ContentBuilder:
        self.content.queries.append(query)
        return self

    def build(self) -> Content:
        return self.content

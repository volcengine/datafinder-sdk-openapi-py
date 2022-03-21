# encoding: utf-8
from __future__ import annotations
import copy
from rangersdk.dslclient.json_formatter import JSONFormatter
from rangersdk.dslcontent.content import Content, _ContentBuilder
from rangersdk.dslcontent.profile_filter import Filter
from rangersdk.dslcontent.condition import Condition
from rangersdk.dslcontent.query import Query


class DSL(JSONFormatter):

    def __init__(self):
        self.version = 3.0
        self.use_app_cloud_id = True
        self.app_ids = []
        self.periods = []
        self.content = {}

        self.content_builder = Content.builder()

    @staticmethod
    def builder(query_type=None) -> _DSLBuilder:
        return _DSLBuilder(DSL(), query_type)

    @staticmethod
    def event_builder() -> _DSLBuilder:
        return DSL.builder('event')

    @staticmethod
    def funnel_builder() -> _DSLBuilder:
        return DSL.builder('funnel')

    @staticmethod
    def lifecycle_builder() -> _DSLBuilder:
        return DSL.builder('life_cycle')

    @staticmethod
    def pathfind_builder() -> _DSLBuilder:
        return DSL.builder('path_find')

    @staticmethod
    def retention_builder() -> _DSLBuilder:
        return DSL.builder('retention')

    @staticmethod
    def web_builder() -> _DSLBuilder:
        return DSL.builder('web_session')

    @staticmethod
    def confidence_builder() -> _DSLBuilder:
        return DSL.builder('confidence')

    @staticmethod
    def topk_builder() -> _DSLBuilder:
        return DSL.builder('event_topk')

    @staticmethod
    def advertise_builder() -> _DSLBuilder:
        return DSL.builder('advertise')

    def get_content_builder(self) -> _ContentBuilder:
        return self.content_builder

    def add_appid(self, app_id):
        self.app_ids.extend(app_id)


def string_expr(name, operation, values, type_='profile'):
    return _expr('string', name, operation, values, type_)


def int_expr(name, operation, values, type_='profile'):
    return _expr('int', name, operation, values, type_)


def empty_expr():
    return Filter.builder()


def _expr(value_type, name, operation, values, type_='profile'):
    return Filter.builder() \
        .set_conditions(Condition(value_type, name, operation, values, type_))


def show(label, name):
    return Query.builder().set_show_label(label).set_show_name(name)


def merge(params, *dsls):
    merge_dsl = None
    for dsl in dsls:
        if not merge_dsl:
            merge_dsl = copy.deepcopy(dsl)
            setattr(merge_dsl, 'contents', [])
            merge_dsl.contents.append(dsl.content)
            delattr(merge_dsl, '_content')
            continue
        merge_dsl.contents.append(dsl.content)
    if params and isinstance(params, dict):
        setattr(merge_dsl, 'option', params)
    return merge_dsl


def blend(base, *dsls):
    merge_dsl = merge(dict(blend=dict(status=True, base=base)), *dsls)
    return merge_dsl


class _DSLBuilder(object):
    def __init__(self, dsl, query_type=None):
        self.dsl = dsl
        self.query_type = query_type
        self.set_query_type(query_type)

    def set_app_id(self, *app_id) -> _DSLBuilder:
        self.dsl.app_ids.extend(app_id)
        return self

    def set_query_type(self, query_type) -> _DSLBuilder:
        self.dsl.get_content_builder().set_query_type(query_type)
        # self.query_type = query_type
        # 留存的optmized 是true
        if 'funnel' == query_type:
            self.set_optmized(True)
        if 'path_find' == query_type:
            self.set_optmized(False)
        return self

    def set_range_period(self, granularity, start, end, real_time=False) -> _DSLBuilder:
        period = {'type': 'range', 'granularity': granularity, 'range': [start, end]}
        if real_time:
            period['real_time'] = True
        self.dsl.periods.append(period)
        return self

    def set_last_period(self, granularity, amount, unit, real_time=False) -> _DSLBuilder:
        period = {'type': 'last', 'granularity': granularity, 'last': {'amount': amount, 'unit': unit}}
        if real_time:
            period['real_time'] = True
        self.dsl.periods.append(period)
        return self

    def set_today_period(self, granularity, real_time=False) -> _DSLBuilder:
        period = {'type': 'today', 'granularity': granularity}
        if real_time:
            period['real_time'] = True
        self.dsl.periods.append(period)
        return self

    def set_group(self, group) -> _DSLBuilder:
        self.dsl.get_content_builder().set_profile_groups(group)
        return self

    # def set_group_common_param(self, group) -> _DSLBuilder:
    #     return self.__set_group_v2(group, "common_param")

    def set_group_user_profile(self, group) -> _DSLBuilder:
        return self.__set_group_v2(group, "user_profile")

    def __set_group_v2(self, group, property_type: str) -> _DSLBuilder:
        if isinstance(group, list):
            self.dsl.get_content_builder().set_profile_groups_v2([
                {"property_name": k,
                 "property_type": property_type} for k in group])
        else:
            self.dsl.get_content_builder().set_profile_groups_v2(
                {"property_name": group,
                 "property_type": property_type})
        return self

        return self

    def set_order(self, order, direction='asc') -> _DSLBuilder:
        if isinstance(order, list):
            self.dsl.get_content_builder().set_orders(order)
        else:
            self.dsl.get_content_builder().set_orders({'field': order, 'direction': direction})
        return self

    def set_page(self, limit, offset) -> _DSLBuilder:
        self.dsl.get_content_builder().set_page(limit, offset)
        return self

    def set_limit(self, limit) -> _DSLBuilder:
        self.dsl.get_content_builder().set_limit(limit)
        return self

    def set_offset(self, offset) -> _DSLBuilder:
        self.dsl.get_content_builder().set_offset(offset)
        return self

    def set_skip_cache(self, skip_cache) -> _DSLBuilder:
        self.dsl.get_content_builder().set_option('skip_cache', skip_cache)
        return self

    def set_is_stack(self, is_stack) -> _DSLBuilder:
        self.dsl.get_content_builder().set_option('is_stack', is_stack)
        return self

    def set_optmized(self, optimized) -> _DSLBuilder:
        self.dsl.get_content_builder().set_option('optimized', True if optimized else False)
        return self

    def set_window(self, granularity, interval) -> _DSLBuilder:
        if 'life_cycle' == self.query_type:
            self.set_lifecycle(granularity, interval)
        elif 'retention' == self.query_type:
            self.set_retention(granularity, interval)
        else:
            self.dsl.get_content_builder().set_option('window_period_type', granularity)
            self.dsl.get_content_builder().set_option('window_period', interval)
        return self

    def set_lifecycle(self, granularity, interval, type_='stickiness') -> _DSLBuilder:
        self.dsl.get_content_builder().set_option('lifecycle_query_type', type_)
        self.dsl.get_content_builder().set_option('lifecycle_period',
                                                  dict(granularity=granularity,
                                                       period=interval))
        return self

    def set_retention(self, granularity, interval) -> _DSLBuilder:
        self.dsl.get_content_builder().set_option('retention_type', granularity)
        self.dsl.get_content_builder().set_option('retention_n_days', interval)
        return self

    def set_web(self, type_, timeout) -> _DSLBuilder:
        self.dsl.get_content_builder().set_option('web_session_params',
                                                  dict(session_params_type=type_,
                                                       session_timeout=timeout))
        return self

    def set_product(self, product) -> _DSLBuilder:
        self.dsl.get_content_builder().set_option('product', product)
        return self

    def set_advertise(self, advertise_params) -> _DSLBuilder:
        # type: (dict) -> _DSLBuilder
        for k, v in advertise_params.items():
            self.dsl.get_content_builder().set_option(k, v)
        return self

    def set_option(self, option) -> _DSLBuilder:
        for k, v in option.items():
            self.dsl.get_content_builder().set_option(k, v)
        return self

    def set_tag(self, tags) -> _DSLBuilder:
        for k, v in tags.items():
            self.dsl.get_content_builder().set_show_option(k, v)
        return self

    def set_and_profile_filter(self, exp_builder) -> _DSLBuilder:
        self.dsl.get_content_builder().set_profile_filter(exp_builder.set_logic('and').build())
        return self

    def set_or_profile_filter(self, exp_builder) -> _DSLBuilder:
        self.dsl.get_content_builder().set_profile_filter(exp_builder.set_logic('or').build())
        return self

    def set_query(self, query_builders) -> _DSLBuilder:
        query = []
        for query_builder in query_builders:
            query.append(query_builder.build())
        self.dsl.get_content_builder().set_query(query)
        return self

    def set_periods(self, periods) -> _DSLBuilder:
        self.dsl.periods = periods
        return self

    def build(self) -> DSL:
        self.dsl.content = self.dsl.get_content_builder().build()
        del self.dsl.content_builder
        return self.dsl

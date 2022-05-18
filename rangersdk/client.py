# encoding: utf-8
import json

import requests
from rangersdk.dslclient.dsl_sign import sign


class RangerClient(object):
    def __init__(self, org, ak, sk, expiration=None, url=None):
        if url:
            self.__url = url
        else:
            self.__url = "https://analytics.volcengineapi.com"
        self.__ak = ak
        self.__sk = sk
        if expiration:
            self.__expiration = expiration
        else:
            self.__expiration = 1800
        self.__org = org
        self.__services = {
            'data_finder': '/datafinder',
            'data_tracer': '/datatracer',
            'data_tester': '/datatester',
            'data_analyzer': '/dataanalyzer',
            'data_rangers': '/datarangers',
            'data_profile': '/dataprofile',
        }

    def _request_service(self, service, method, path, headers, params, body):
        service_path = self.__services.get(service)
        if not service_path:
            raise ClientException('service: {} not exist'.format(service))

        service_url = service_path + path
        return self._request(method, service_url, headers, params, body)

    @staticmethod
    def parse_params(params):
        kvs = []
        for k, v in params.items():
            kvs.append('{}={}'.format(k, v))
        return '&'.join(kvs)

    @staticmethod
    def _parse_method(**kwargs):
        method = kwargs.get('method')
        if not method:
            if kwargs.get('body'):
                method = 'POST'
            else:
                method = 'GET'
        return method

    def _request(self, method, service_url, headers, params, body):
        if body is not None:
            if hasattr(body, "toJSON"):
                body = body.toJSON()
            if isinstance(body, dict):
                body = json.dumps(body)
            elif isinstance(body, str):
                pass
            else:
                raise ClientException('body must have toJSON or be dict or be str')
        method = method.upper()
        if method not in ["POST", "GET", "DELETE", "PUT", "PATCH"]:
            raise ClientException('unSupport method: {}'.format(method))
        if 'POST' == method:
            if body is None:
                raise ClientException('post must have body')

        authorization = sign(self.__ak, self.__sk, self.__expiration, method, service_url, params, body)
        r_headers = {'Authorization': authorization}
        if headers:
            r_headers.update(headers)
        elif 'POST' == method:
            r_headers['Content-Type'] = 'application/json'
        url = self.__url + service_url + ("?{}".format(RangersClient.parse_params(params)) if params else "")
        return requests.request(method=method, url=url, data=body, headers=r_headers)

    def request(self, service_url, **kwargs):
        return self._request(RangersClient._parse_method(**kwargs), service_url, kwargs.get('headers'),
                                     kwargs.get('params'), kwargs.get('body'))

    def data_finder(self, path, **kwargs):
        return self._request_service('data_finder', RangersClient._parse_method(**kwargs), path, kwargs.get('headers'),
                                     kwargs.get('params'), kwargs.get('body'))

    def data_tracer(self, path, **kwargs):
        return self._request_service('data_tracer', RangersClient._parse_method(**kwargs), path, kwargs.get('headers'),
                                     kwargs.get('params'), kwargs.get('body'))

    def data_tester(self, path, **kwargs):
        return self._request_service('data_tester', RangersClient._parse_method(**kwargs), path, kwargs.get('headers'),
                                     kwargs.get('params'), kwargs.get('body'))

    def data_analyzer(self, path, **kwargs):
        return self._request_service('data_analyzer', RangersClient._parse_method(**kwargs), path, kwargs.get('headers'),
                                     kwargs.get('params'), kwargs.get('body'))

    def data_rangers(self, path, **kwargs):
        return self._request_service('data_rangers', RangersClient._parse_method(**kwargs), path, kwargs.get('headers'),
                                     kwargs.get('params'), kwargs.get('body'))

    def data_profile(self, path, **kwargs):
        return self._request_service('data_profile', RangersClient._parse_method(**kwargs), path, kwargs.get('headers'),
                                     kwargs.get('params'), kwargs.get('body'))

    def rangers(self, path, **kwargs):
        return self._request_service('data_rangers', RangersClient._parse_method(**kwargs), path, kwargs.get('headers'),
                                     kwargs.get('params'), kwargs.get('body'))


class ClientException(Exception):
    def __init__(self, message):  # real signature unknown
        super(Exception, self).__init__(message)


class RangersClient(RangerClient):
    def __init__(self, ak, sk, expiration=None, url=None):
        RangerClient.__init__(self, '', ak, sk, expiration, url)

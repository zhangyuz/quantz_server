'''
QuantZ 数据接口，处理所有
'''

import base64
import functools
import json

from flask import jsonify, Response
from mongoengine import Document
from quantz_repo import *

_params = '''
{
	"filters":["ts_code=000001.SH"],
	"order_by": ["-trade_date"],
	"page": 1,
	"per_page": 100
}
'''


def _query(doc: Document, filters: tuple = None, page: int = 1, per_page: int = 100, order_by: str = None) -> str:
    """数据库查询函数

    :param doc: Document的子类型，从哪个collection 中获取数据
    :type doc: Document
    :param filters: QuerySet 的 filter 参数, defaults to None
    :type filters: tuple, optional
    :param page: 数据分页，此处表示页码, defaults to 1
    :type page: int, optional
    :param per_page: 每页文档个数, defaults to 100
    :type per_page: int, optional
    :param order_by: QuerySet 的 order_by, defaults to None
    :type order_by: str, optional
    :return: collection 的 JSON 串
    :rtype: str
    """
    print('\nQuery params:\n')
    print('filters:%s\norder_by:%s\npage:%d per_page:%d' %
          (filters, order_by, page, per_page))
    objects = None
    if filters:
        objects = doc.objects(**filters)
    else:
        objects = doc.objects()
    if per_page > 0 and per_page > 0:
        objects = objects.limit(per_page).skip((page - 1) * per_page)
    if order_by is not None:
        objects = objects.order_by(*order_by)
    if objects is not None and objects.count() > 0:
        return objects.to_json()
    print('Failed to get data from db\n')
    return None


def _base64_filters_to_dict(filters: str) -> dict:
    '''
    将Base64的查询参数转换成dict
    '''
    try:
        return json.loads(base64.urlsafe_b64decode(filters))
    except Exception as e:
        print('Failed to decode filters(%s)\n%s\n' % filters, e)
        return None


def _handle_query_prarams(query_params: str = None) -> dict:
    """ 解析查询参数，返回参数字典

    :param query_params: Base64 websafe的参数编码, defaults to None
    :type query_params: str, optional
    :return: 返回参数字典，如解析失败或参数中无预定的参数，返回 None
    :rtype: dict
    """
    if query_params:
        local = {}
        params_dict = _base64_filters_to_dict(query_params)
        if not params_dict:
            print('Failed to decode query params(%s)\n' % query_params)
            return None
        if 'filters' in params_dict:
            filters_str = 'filters = {'
            for f in params_dict['filters']:
                f_list = f.split('=')
                filters_str += '"%s":"%s",' % (f_list[0], f_list[1])
            filters_str = filters_str[:len(filters_str) - 1] + '}'
            print('\nfilters_str=%s\n' % filters_str)
            exec(filters_str, {}, local)
            print('\nfilters = %s\n' % local['filters'])
        if 'order_by' in params_dict:
            order_by_str = 'order_by = ['
            for o in params_dict['order_by']:
                order_by_str += '"%s",' % o
            order_by_str = order_by_str[:len(order_by_str) - 1] + ']'
            print('order_by_str:%s\n' % order_by_str)
            exec(order_by_str, {}, local)
            print('order_by:%s' % type(local['order_by']))
        if 'page' in params_dict:
            exec('page = %d' % params_dict['page'], {}, local)
        if 'per_page' in params_dict:
            exec('per_page = %d' % params_dict['per_page'], {}, local)
        if len(local) == 0:
            print('No param found:%s\n' % params_dict)
            return None
        return local
    else:
        return None


class QuantZ():
    DFT_TABLE = 'IndexDaily'
    DFT_QUERY_PARAMS = base64.urlsafe_b64encode(str.encode(_params))
    _TABLE_MAP = {'IndexDaily', 'IndexDailyItem'}

    def index(self):
        return jsonify('Welcome to QuantZ!')

    def data(self, table: str, query_params: str):
        if table in QuantZ._TABLE_MAP:
            params = _handle_query_prarams(query_params)
            query_func = functools.partial(
                _query, doc=eval('IndexDailyItem'))
            collection = query_func(filters=params.get('filters'), order_by=params.get('order_by'),
                                    page=params.get('page'), per_page=params.get('per_page'))
            if collection is not None:
                return Response(collection, mimetype='application/json')
            else:
                return 'Failed to get data from DB!'
        else:
            print('Invalide table:%s\n' % table)
            return jsonify('Invalide table %s!!!' % table)

    def post(self):
        pass

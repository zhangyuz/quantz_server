import json
from unittest import TestCase

import pandas as pd
import requests
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from quantz_server.schema import schema

# 以3个引号定义的字符串表示多行内容，这样就不用自己写换行符了。
query = """
{
  indexDaily(tsCode: "000001.SH", first: 2, after: "YXJyYXljb25uZWN0aW9uOjc=") {
    edges {
      node {
        tsCode
        close
        tradeDate
      }
      cursor
    }
    pageInfo {
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
    }
  }
}
"""

url = 'http://localhost:8080/graphql'


def hello_dict_args(arg1='o1', arg2='02', **args):
    print('\narg1=%s arg2=%s args=%s\n' % (arg1, arg2, args))


class AppTest(TestCase):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_graphql_request(self):
        resp = requests.post(url, json={'query': query})
        print(resp.status_code)
        print(resp.json()['data']['indexDaily']['edges'])

    def test_graphql_gql(self):
        gql_client = Client(
            transport=RequestsHTTPTransport(url=url), schema=schema)
        gql_query = gql(query)
        resp = gql_client.execute(gql_query)
        print(resp)

    def test_dict_args(self):
        test_args = dict({'arg1': '111', 'arg2': '2222', 'arg3': '3333'})
        hello_dict_args(**test_args)

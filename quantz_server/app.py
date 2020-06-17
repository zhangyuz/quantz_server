from flask import Flask, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
from mongoengine import connect

from .schema import schema

from .resources.quantz import QuantZ

connect('quant_test')

app = Flask(__name__)
app.debug = True


CORS(app, resources={r'/*': {'origins': '*'}})


quantz_resource = QuantZ()

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify(a='pong!')


@app.route('/quantz', methods=['GET', 'POST'])
def quantz():
    return quantz_resource.index()


# 默认返回上证最近100个交易日日线数据
@app.route('/quantz/', defaults={'table': QuantZ.DFT_TABLE, 'query_params': QuantZ.DFT_QUERY_PARAMS})
# 默认 返回最近100个交易日日线数据
@app.route('/quantz/<string:table>', defaults={'query_params': QuantZ.DFT_QUERY_PARAMS})
# 用户指定返回的数据
@app.route('/quantz/<string:table>/<string:query_params>')
def quantz_data(table, query_params):
    return quantz_resource.data(table, query_params)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

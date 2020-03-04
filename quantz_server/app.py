from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from mongoengine import connect

from schema import schema

connect('quant_test')

app = Flask(__name__)
app.debug = True

CORS(app, resources={r'/*': {'origins': '*'}})

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(host='localhost', debug=True)
    # app.run(host='localhost', debug=True)

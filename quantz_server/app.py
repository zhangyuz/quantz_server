from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

from mongoengine import connect
connect('quant_test')

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)

# from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def hello():
#     return 'My First API !!'

# from api import app, db
# from api import models

# from ariadne import load_schema_from_path, make_executable_schema, \
#     graphql_sync, snake_case_fallback_resolvers, ObjectType
# from ariadne.constants import PLAYGROUND_HTML       
# from flask import request, jsonify

# type_defs = load_schema_from_path("schema.graphql")
# schema = make_executable_schema(
#     type_defs,
#     snake_case_fallback_resolvers,
# )
# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     return PLAYGROUND_HTML, 200
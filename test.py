from flask import Flask, request, jsonify
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerPlayground
from ariadne import QueryType

# Create Flask app
app = Flask(__name__)

# Define type definitions (GraphQL schema)
type_defs = """
    type Query {
        hello: String!
    }
"""

# Define resolvers
query = QueryType()

@query.field("hello")
def resolve_hello(_, info):
    return "Hello from Ariadne with Flask!"

# Create schema
schema = make_executable_schema(type_defs, query)

# Enable Playground (GraphQL UI)
playground = ExplorerPlayground()

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return playground.html(), 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "No valid GraphQL query provided"}), 400

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug  # helps with Flask debugger
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)

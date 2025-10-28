from flask import Flask, request, jsonify
from ariadne import QueryType, make_executable_schema, graphql_sync
from ariadne.explorer import ExplorerPlayground 

# Define schema
type_defs = """
    type Query {
        hello(name: String): String!
    }
"""

query = QueryType()

@query.field("hello")
def resolve_hello(_, info, name="World"):
    return f"Good Morning, {name}!"

# Create executable schema
schema = make_executable_schema(type_defs, query)

app = Flask(__name__)

# Initialize new Ariadne Playground
playground = ExplorerPlayground() 

# GraphQL Playground route
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    print("Playground accessed", playground)
    return playground.html(None), 200

############################ GraphQL POST route #########################
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "No valid GraphQL query provided"}), 400

    success, result = graphql_sync(schema, data, context_value=request)
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)

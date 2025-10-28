from flask import Flask, request, jsonify
from ariadne import gql, QueryType, MutationType, make_executable_schema, graphql_sync
from ariadne.explorer import ExplorerPlayground

# --------------------------
# Mock Database
# --------------------------
users = [
    {
        "id": 1,
        "name": "Vaishnavi",
        "email": "vaishnavi@example.com",
        "posts": [
            {
                "id": 101,
                "content": "Just cloned the Prime Video website using HTML & CSS!",
                "reactions": [
                    {"type": "LIKE", "user": "Anirudh"},
                    {"type": "LOVE", "user": "Nikhil"}
                ]
            },
            {
                "id": 102,
                "content": "Working on GraphQL Flask integration today 🚀",
                "reactions": [{"type": "LIKE", "user": "Praven"}]
            }
        ],
        "photos": [
            {"url": "https://example.com/photo1.jpg", "caption": "UI Design Work"},
            {"url": "https://example.com/photo2.jpg", "caption": "Dashboard Testing"}
        ]
    }
]

# --------------------------
# GraphQL Schema
# --------------------------
type_defs = gql("""
    type Query {
        user(id: ID!): User
        users: [User!]!
    }

    type Mutation {
        updatePost(userId: ID!, postId: ID!, newContent: String!): Post
        deletePost(userId: ID!, postId: ID!): String
    }

    type User {
        id: ID!
        name: String!
        email: String!
        posts: [Post!]!
        photos: [Photo!]!
    }

    type Post {
        id: ID!
        content: String!
        reactions: [Reaction!]!
    }

    type Reaction {
        type: String!
        user: String!
    }

    type Photo {
        url: String!
        caption: String!
    }
""")

# --------------------------
# Query Resolvers
# --------------------------
query = QueryType()

@query.field("users")
def resolve_users(_, info):
    return users

@query.field("user")
def resolve_user(_, info, id):
    return next((user for user in users if user["id"] == int(id)), None)

# --------------------------
# Mutation Resolvers
# --------------------------
mutation = MutationType()

@mutation.field("updatePost")
def resolve_update_post(_, info, userId, postId, newContent):
    for user in users:
        if user["id"] == int(userId):
            for post in user["posts"]:
                if post["id"] == int(postId):
                    post["content"] = newContent
                    return post
    return None

@mutation.field("deletePost")
def resolve_delete_post(_, info, userId, postId):
    for user in users:
        if user["id"] == int(userId):
            before_count = len(user["posts"])
            user["posts"] = [p for p in user["posts"] if p["id"] != int(postId)]
            after_count = len(user["posts"])
            if before_count != after_count:
                return f"Post {postId} deleted successfully."
            else:
                return f"Post {postId} not found."
    return "User not found."

# --------------------------
# Build Schema & Flask App
# --------------------------
schema = make_executable_schema(type_defs, query, mutation)
app = Flask(__name__)
playground = ExplorerPlayground()

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return playground.html(None), 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request)
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)

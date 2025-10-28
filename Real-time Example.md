⚙️ Real Meta/Facebook Analogy

In the actual Meta backend:
Every profile, post, or reaction is part of a graph.
Updates and deletions are handled via GraphQL mutations (not REST).
This helps the mobile app sync instantly (no extra API calls).

Server Side:
GraphQL Endpoint:
http://127.0.0.1:5000/graphql
 
1. Fetch user data with posts:
query {
  user(id: 1) {
    name
    posts {
      id
      content
    }
  }
}

2. Update Post Example:
mutation {
  updatePost(userId: 1, postId: 101, newContent: "Updated content") {
    id
    content
  }
}
3. Delete Post Example:
mutation {
  deletePost(userId: 1, postId: 101)
}

4.post
query {
  user(id: 1) {
    name
    email
    posts {
      content
      reactions {
        type
        user
      }
    }
    photos {
      url
      caption
    }
  }
}

`Feature Comparison`

| Action      | REST API Equivalent         | GraphQL Mutation                         |
| ----------- | --------------------------- | ---------------------------------------- |
| Update post | `PUT /users/1/posts/102`    | `updatePost(userId, postId, newContent)` |
| Delete post | `DELETE /users/1/posts/101` | `deletePost(userId, postId)`             |
| Benefit     | Multiple endpoints          | Unified endpoint `/graphql`              |

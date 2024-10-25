
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__) 

#created at SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
#defined api from flask restful api
api = Api(app)

class UserModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self): 
        return f"User(name = {self.name}, email = {self.email})"


# Define expected parameters and Create a RequestParser instance

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")


#decorated with marshal with serializing data with using data
userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}

class Users(Resource):
    #shape the data with http  request using post and get function
    @marshal_with(userFields)
    #Requesting data from a specified resource
    def get(self):
        #retrive data in database
        users = UserModel.query.all() 
        #empty array as output
        return users 
    
    @marshal_with(userFields)
    def post(self):
        #define name with used argumnet wih
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user) 
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

class User(Resource):
    #get the data with id parameter 
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            #aborted if no user is found
            abort(404, message="User not found")
        return user
    
    @marshal_with(userFields)
    # the retrieval, validation, updating, and response formatting in a systematic way.
    def patch(self, id):
        # Parse the incoming arguments
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="user not found")
        user.name =args["name"]
        user.email= args["email"]
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self, id):
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
            db.session.delete(user)
            db.session.commit()
            users=UserModel.query.all()
            return users

# Add a resource for all users
api.add_resource(Users, '/api/users/')

#add paramerater, Add a resource for a single user, with an ID parameter
api.add_resource(User, '/api/user/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True) 

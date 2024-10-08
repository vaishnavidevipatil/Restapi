from flask import Flask
from flask_restful import Api, Resource

app= Flask(__name__)
api=Api(app)

class HelloWorld(Resource):
    def get(self, name, test):
        return {
         "name": name,
         "test": test  
         #json object
        }


api.add_resource(HelloWorld, '/helloworld/<string:name>/<int:test>')

if __name__ == "__main__":
      app.run(debug=True,  port=5000)



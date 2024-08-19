from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app= Flask(__name__)
api=Api(app)



video_put_arugs= reqparse.RequestParser()
video_put_arugs.add_argument("name", type=str, help="Names of the video", required=True)
video_put_arugs.add_argument("views", type=str, help="Views of the video", required=True )
video_put_arugs.add_argument("likes", type=str, help="Likes of the videos", required=True)

videos= {}

def abort_if_video_id_doesnt_exit(video_id):
      if video_id not in videos:
            abort(404, message="Could nt find video...")


def abort_if_video_exists(video_id):
    if video_id in videos:  
       abort(409,message="Video already exists with that ID...")

class Video(Resource):
      def get(self, video_id):
            abort_if_video_id_doesnt_exit(video_id)
            return videos[video_id]
      
      def put(self, video_id):
            args= video_put_arugs.parse_args()
            videos[video_id]= args
            return videos[video_id], 201
      
      def delete(self, video_id):
           abort_if_video_id_doesnt_exit(video_id)
           del videos[video_id]
           return '', 204
      

api.add_resource(Video, '/video/<int:video_id>')

if __name__ == "__main__":
      app.run(debug=True,  port=5000)



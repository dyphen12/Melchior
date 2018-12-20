from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

from core import Melicon

app = Flask(__name__)
api = Api(app)
CORS = (app)

refactorParser = reqparse.RequestParser()
refactorParser.add_argument('user_id')
refactorParser.add_argument('access_token')
refactorParser.add_argument('percent')



current_accesstoken = 'APP_USR-280693783442951-121921-e0b96d75d2a10b602cf954a3d23a0436-76816874'

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class userid(Resource):
    def get(self, access_token):
        x = Melicon.get_userID(access_token)
        payload = {"user-id":x}
        return payload

class refactor_all(Resource):
    def post(self):
        args = refactorParser.parse_args()
        UID = args['user_id']
        current_at = args['access_token']
        percent = int(args['percent'])
        x = Melicon.PercentRefactor_allitems(UID,percent,current_at)
        return 200


api.add_resource(HelloWorld, '/')
api.add_resource(userid, '/user_id/<string:access_token>')
api.add_resource(refactor_all, '/refactor_all')


if __name__ == '__main__':
    app.run(debug=True)
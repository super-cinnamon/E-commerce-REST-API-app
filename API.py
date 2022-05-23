from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import json

app = Flask(__name__)
api = Api(app)

#database
db = open("data.json", "r+")
database = json.load(db)

#parsers
item_put_args = reqparse.RequestParser()
item_put_args.add_argument("owner", type=str, help="Name of the winning bidder")
item_put_args.add_argument("prix_achat", type=int, help="Price item was bought for")

class Auction(Resource):
        def get(self, ID):
                if ID > 0:
                        #check if exists
                        idObj = f'{ID}'
                        if database[idObj]:
                                object = {}                        
                                object[idObj] = database[idObj]
                                return object, 200
                        else: abort(404, message="Could not find item with that id")
                if ID == 0:
                        keys={key:"0"for key in database.keys()}
                        return keys, 200
                else:
                        abort(406, message = "ID invalid")
                

        def put(self, ID):
                args = item_put_args.parse_args()
                if ID in database.keys():
                        #we update the boys
                        idObj = f'{ID}'
                        object = database[idObj]
                        object["Acheteur"] = args["owner"]
                        object["Prix d'achat"] = args["prix_achat"]
                        updt = json.dumps(database, indent=4)
                        db.write(updt)
                        
                else: abort(404, message="Could not find item with that id")
                

api.add_resource(Auction, "/auction/<int:ID>")

if __name__ == "__main__":
        ### open the db file?
        app.run(debug=True)

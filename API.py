from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import json

from numpy import unicode_

app = Flask(__name__)
api = Api(app)



#parsers
item_put_args = reqparse.RequestParser()
item_put_args.add_argument("owner", type=str, help="Name of the winning bidder", location='form')
item_put_args.add_argument("prix_achat", type=int, help="Price item was bought for", location='form')

class Auction(Resource):
        def get(self, ID):
                #database
                with open("data.json", "r+",encoding="utf-8") as db : 
                       database = json.load(db)
                
                if ID > 0:
                        #check if exists
                        idObj = f'{ID}'
                        if idObj in database.keys():
                                object = {}                        
                                object[idObj] = database[idObj]
                                return object, 200
                        else: abort(404, message="Could not find item with that id")
                if ID == 0:
                        keys={key:"0"for key in database.keys()}
                        return keys, 200
                

        def put(self, ID):
                #database
                with open("data.json", "r+",encoding="utf-8") as db : 
                       database = json.load(db)
                args = item_put_args.parse_args()
                idObj = f'{ID}'
                if idObj in database.keys():
                        #we update the boys
                        object = database[idObj]
                        object["Acheteur"] = args["owner"]
                        object["Prix d'achat"] = args["prix_achat"]
                        #database
                        db.close()
                        with open("data.json", "r+",encoding="utf-8") as db : 
                                updt = json.dumps(database, indent=4, ensure_ascii=False)
                                db.seek(0)
                                db.write(updt)
                                db.truncate()
                        
                        
                else: abort(404, message="Could not find item with that id")
                

api.add_resource(Auction, "/auction/<int:ID>")

if __name__ == "__main__":
        ### open the db file?
        app.run(debug=True)

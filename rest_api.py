from flask import Flask, jsonify, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

stored_transactions = []

class add(Resource):
    def post(self):
       added_points = request.get_json()
       stored_transactions.append(added_points)

       if "payer" not in added_points or "points" not in added_points or "timestamp" not in added_points:
           return '', 400

       return '', 200
    
class spend(Resource):
    def post(self):
        spent_points = request.get_json()
        stored_transactions.append(spent_points)
        result = []

        if "points" not in spent_points:
            return '', 400
        
        sorted_transactions = sorted(stored_transactions, key=lambda k : k["timestamp"])
        points = spent_points["points"]
        for transaction in sorted_transactions:
            if transaction["points"] <= points:
                points -= transaction["points"]
                transaction["points"] = 0
                result.append({transaction["payer"]: -transaction["points"]})
            else:
                transaction["points"] -= points
                result.append({transaction["payer"]: -points})
                points = 0
        
        if points != 0:
            return 'Not Enough Points!', 400

        return jsonify(result), 200

class balance(Resource):
    def get(self):
        result = {}
        for transaction in stored_transactions:
            if transaction["payer"] not in result:
                result[transaction["payer"]] = 0
            result[transaction["payer"]] += transaction["points"]
        return jsonify(result), 200      

api.add_resource(add, '/add')
api.add_resource(spend, '/spend')
api.add_resource(balance, '/balance')

if __name__ == '__main__':
    app.run(host='localhost', port = 8000, debug=True)
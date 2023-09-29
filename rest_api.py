from flask import Flask, jsonify, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

stored_transactions = []

class add(Resource):
    """
    adds a valid transaction to the stored_transactions list

    args: JSON in format
        {
            "payer": "company_name",
            "points": point_value,
            "timestamp": "timestamp_date"
        }

    returns: 200 if successful, 400 if not
    """
    def post(self):
       added_points = request.get_json()
       stored_transactions.append(added_points)

       if "payer" not in added_points or "points" not in added_points or "timestamp" not in added_points:
           return '', 400

       return '', 200
    
class spend(Resource):
    """
    updates the stored_transactions list to reflect the spent points

    args: JSON in format
        {
            "points": point_value
        }

    returns: 200 if successful and the amount of points that each payer spend on the transaction, 400 if not
    """
    def post(self):
        spent_points = request.get_json()
        result = []
        result_dict = {}

        if "points" not in spent_points:
            return '', 400
        
        sorted_transactions = sorted(stored_transactions, key=lambda k : k["timestamp"])
        points = spent_points["points"]
        for transaction in sorted_transactions:
            if transaction["points"] < points:
                points -= transaction["points"]
                transaction["points"] = 0
                if transaction["payer"] not in result_dict:
                    result_dict[transaction["payer"]] = 0
                result_dict[transaction["payer"]] += -transaction["points"]
            else:
                transaction["points"] -= points
                if transaction["payer"] not in result_dict:
                    result_dict[transaction["payer"]] = 0
                result_dict[transaction["payer"]] += -points
                points = 0
        
        if points != 0:
            return 'Not Enough Points!', 400

        result.append(result_dict)

        return result, 200

class balance(Resource):
    """
    returns the current balance of each payer

    returns: 200 if successful and the current balance of each payer
    """
    def get(self):
        result = {}

        for transaction in stored_transactions:
            if "payer" in transaction and "points" in transaction:
                payer = transaction["payer"]
                points = transaction["points"]
                
                if payer not in result:
                    result[payer] = 0
                result[payer] += points

        return result, 200

api.add_resource(add, '/add')
api.add_resource(spend, '/spend')
api.add_resource(balance, '/balance')

if __name__ == '__main__':
    app.run(host='localhost', port = 8000, debug=True)
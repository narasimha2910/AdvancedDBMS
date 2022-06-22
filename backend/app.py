from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from py2neo import Graph
g = Graph("neo4j+s://88430ba4.databases.neo4j.io", auth=("neo4j", "Q6aHR0gm2yFXyz2tndqEPOFLsi9JwHGfNYww3zZ1ySQ"))

app = Flask(__name__)
CORS(app=app)
def errorMessage(error):
    res = {}
    res["error"] = error
    res["status"] = False
    res["code"] = 401
    return jsonify(res)

@app.route("/predict", methods=["POST"])
@cross_origin()
def crop_recommender():
    data = request.get_json()
    if not data:
        return errorMessage("Bad Request")
    if "season" in data.keys():
        season = data["season"]
    else:
        season=""
    if "location" in data.keys():
        location = data["location"]
    else:
        location=""
    if not location:
        q = "MATCH (c:Crop {{ season: '{0}'}}) Match(f:Farmer)-[r:GREW]->(c) RETURN c, f".format(season)
    elif not season:
        q = "MATCH (c:Crop {{location: '{0}' }}) Match(f:Farmer)-[r:GREW]->(c) RETURN c, f".format(location)
    else:
        q = "MATCH (c:Crop {{ season: '{0}', location: '{1}' }}) Match(f:Farmer)-[r:GREW]->(c) RETURN c, f".format(season, location)
    resp =  g.run(q).data()
    res = {}
    crop_list = []
    for crop in resp:
        crop_list.append(crop)
    res["crop_list"] = crop_list
    res["status"] = True
    res["code"] = 200
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

            

if __name__ == '__main__':
    app.run(debug=True, port=5001)

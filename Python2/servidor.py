from flask import Flask, request, jsonify
import json
import logging
import os
import atexit
from ModeloTrafico import TraficModel

app = Flask(__name__, static_url_path='')
model = TraficModel(14, 2, 55, 55)


def positionsToJSON(ps):
    posDict = []
    for p in ps:
        pos = {
            "x": p[0],
            "z": p[1],
            "y": p[2],
        }
        posDict.append(pos)
    return json.dumps(posDict)


def colorsToJSON(colors):
    colorsDict = []
    for color in colors:
        colorsDict.append(color)
    return json.dumps(colorsDict)


def directionsToJSON(directions):
    directionsDict = []
    for direction in directions:
        directionsDict.append(direction)
    return json.dumps(directionsDict)


port = int(os.getenv('PORT', 8585))


@app.route('/')
def root():
    return jsonify([{"message": "Hello World from IBM Cloud"}])


@app.route('/multiagentes', methods=['POST', 'GET'])
def multiagentes():
    positions = model.step()
    return positionsToJSON(positions)


@app.route('/semaforos', methods=['POST', 'GET'])
def semaforos():
    colors = model.getColors()
    return colorsToJSON(colors)


@ app.route('/direcciones', methods=['POST', 'GET'])
def directions():
    directions = model.getFront()
    return directionsToJSON(directions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

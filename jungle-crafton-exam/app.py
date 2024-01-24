from bson import ObjectId
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider

import json
import sys


app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbjungle

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)

app.json = CustomJSONProvider(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/list', methods=['GET'])
def show_movies_list():
    sortMode = request.args.get('sortMode', 'likes')

    if sortMode == 'likes':
        movies = list(db.movies.find({'trashed': False}, {}).sort("likes", -1))
    elif sortMode == 'viewers':
        movies = list(db.movies.find({'trashed': False}, {}).sort("viewers", -1))
    elif sortMode == 'date':
        movies = list(db.movies.find({'trashed': False}, {}).sort([('open_year', -1), ('open_month', -1), ('open_day', -1)]))
    else:
        return jsonify({'result': 'failure'})

    return jsonify({'result': 'success', 'movies_list': movies})

@app.route('/api/list/trash', methods=['GET'])
def show_movies_list_trash():
    sortMode = request.args.get('sortMode', 'likes')

    if sortMode == 'likes':
        movies = list(db.movies.find({'trashed': True}, {}).sort("likes", -1))
    elif sortMode == 'viewers':
        movies = list(db.movies.find({'trashed': True}, {}).sort("viewers", -1))
    elif sortMode == 'date':
        movies = list(db.movies.find({'trashed': True}, {}).sort([('open_year', -1), ('open_month', -1), ('open_day', -1)]))
    else:
        return jsonify({'result': 'failure'})

    return jsonify({'result': 'success', 'movies_list': movies})

@app.route('/api/like', methods=['POST'])
def like_movie():
    id = request.form['_id']
    movie = db.movies.find_one({"_id" : ObjectId(id)})
    new_likes = movie['likes'] + 1
    result = db.movies.update_one({"_id" : ObjectId(id)}, {'$set': {'likes': new_likes}})

    if result.modified_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})

@app.route('/api/trash', methods=['POST'])
def trash_movie():
    id = request.form['_id']
    result = db.movies.update_one({"_id" : ObjectId(id)}, {'$set': {'trashed': True}})

    if result.modified_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})

@app.route('/api/restore', methods=['POST'])
def restore_movie():
    id = request.form['_id']
    result = db.movies.update_one({"_id" : ObjectId(id)}, {'$set': {'trashed': False}})

    if result.modified_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})

@app.route('/api/delete', methods=['POST'])
def delete_movie():
    id = request.form['_id']
    result = db.movies.delete_one({"_id" : ObjectId(id)})

    if result.deleted_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})


if __name__ == '__main__':
    print(sys.executable)
    app.run('0.0.0.0', port=5000, debug=True)
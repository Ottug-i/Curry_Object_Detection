from flask import Flask, json, request
from py.bookmark_recommend import recommend_with_bookmark
from py.rating_recommend import find_user_ratings
from py.rating_recommend import update_or_append_user_ratings
from py.rating_recommend import delete_user_rating
from py.rating_recommend import find_favorite_genre_with_bookmark
from py.rating_recommend import recommend_with_ratings

app = Flask(__name__)

@app.route("/hello", methods=['GET'])
def hello():
    return "hello world"

@app.route('/bookmark/recommend', methods=['GET'])
def get_bookmark_recommend():
    try:
        recipe_id = int(request.args.get('recipe_id'))
        page = int(request.args.get('page', 1))
    except (TypeError, ValueError):
        return json.dumps({"error": "Invalid parameters"}), 400

    try:
        result = recommend_with_bookmark(recipe_id, page)
    except KeyError as e:
        return json.dumps({"error": "Recipe ID not found"}), 404

    if result is None:
        return json.dumps({"error": "No recommendations found"}), 404
        
    return json.dumps(result), 200

@app.route('/rating/user_ratings', methods=['GET'])
def get_user_ratings():
    try:
        user_id = int(request.args.get('user_id'))
        recipe_id = int(request.args.get('recipe_id'))
    except (TypeError, ValueError):
        return json.dumps({"error": "Invalid parameters"}), 400

    try:
        result = find_user_ratings(user_id, recipe_id)
    except KeyError as e:
        return json.dumps({"error": "User rating not found for the given user_id and recipeId."}), 404

    return json.dumps(result), 200

@app.route('/rating/user_ratings', methods=['POST'])
def update_user_ratings():
    try:
        user_id = int(request.json.get('user_id'))
        new_user_ratings_dic = request.json.get('new_user_ratings_dic')
    except (TypeError, ValueError):
        return json.dumps({"error": "Invalid parameters"}), 400

    try:
        update_or_append_user_ratings(user_id, new_user_ratings_dic)
        return json.dumps({"message": "User ratings updated successfully."}), 200
    except Exception as e:
        return json.dumps({"error": str(e)}), 500
    
@app.route('/rating/user_ratings', methods=['DELETE'])
def remove_user_ratings():
    try:
        user_id = int(request.args.get('user_id'))
        recipe_id = int(request.args.get('recipe_id'))
    except (TypeError, ValueError):
        return json.dumps({"error": "Invalid parameters"}), 400

    try:
        delete_user_rating(user_id, recipe_id)
        return json.dumps({"message": "User ratings deleted successfully."}), 200
    except Exception as e:
        return json.dumps({"error": str(e)}), 500

@app.route('/rating/recommend', methods=['GET'])
def get_rating_recommend():
    try:
        user_id = int(request.args.get('user_id'))
        page = int(request.args.get('page', 1))
        bookmark_list = request.args.getlist('bookmark_list', type=int)
    except (TypeError, ValueError):
        return json.dumps({"error": "Invalid parameters"}), 400

    try:
        user_id, favorite_genre = find_favorite_genre_with_bookmark(user_id, bookmark_list)
        result = favorite_genre, recommend_with_ratings(user_id, favorite_genre, page)
        return json.dumps(result), 200
    except Exception as e:
        return json.dumps({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
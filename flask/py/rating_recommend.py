import pandas as pd
import csv
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso

def find_favorite_genre_with_bookmark(user_id, bookmark_list):
    
    if not bookmark_list:
        return user_id, None
    
    curry_recipes = pd.read_csv('./csv/curry_recipe_with_genres.csv', index_col='id')

    genre_count = {}
    for recipe_id in bookmark_list:
        genres = curry_recipes.loc[recipe_id, 'genres'].split('|')
        for genre in genres:
            genre_count[genre] = genre_count.get(genre, 0) + 1

    favorite_genre = max(genre_count, key=genre_count.get)
    return user_id, favorite_genre

def find_user_ratings(user_id, recipe_id):

    curry_recipes = pd.read_csv('./csv/curry_recipe_with_genres.csv', index_col='id')

    curry_ratings = pd.read_csv('./csv/user_ratings.csv', index_col = 'id')

    user_ratings = curry_ratings[curry_ratings['userId'] == user_id]

    if recipe_id in user_ratings.index:
        return [recipe_id] + [user_id] + user_ratings.loc[recipe_id, ['rating']].tolist()
    elif recipe_id not in user_ratings.index and recipe_id in curry_recipes.index:
        return None
    else:
        return False

def update_or_append_user_ratings(user_id, new_user_ratings_dic):

    curry_recipes = pd.read_csv('./csv/curry_recipe_with_genres.csv', index_col='id')

    file_path = './csv/user_ratings.csv'

    file_exists = os.path.exists(file_path)

    existing_ratings = []
    if file_exists:
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            existing_ratings = [row for row in csv_reader]

        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['id', 'userId', 'rating']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()

            updated = False

            for rating in existing_ratings:
                if (rating['userId'] == str(user_id)) and (rating['id']) in new_user_ratings_dic:
                    rating['rating'] = new_user_ratings_dic[rating['id']]
                    updated = True

                csv_writer.writerow(rating)   

            for key, val in new_user_ratings_dic.items():
                if (key in curry_recipes.index) and not any(rating['userId'] == str(user_id) and rating['id'] == key for rating in existing_ratings):
                    csv_writer.writerow({'id': key, 'userId': str(user_id), 'rating': val})
                    updated = True
            
            return updated
        
def delete_user_rating(user_id, recipe_id):
    
    file_path = './csv/user_ratings.csv'
    file_exists = os.path.exists(file_path)
    
    if file_exists:
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            existing_ratings = [row for row in csv_reader]
        
        filtered_ratings = [row for row in existing_ratings if row['userId'] != str(user_id) or row['id'] != str(recipe_id)]
        
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = existing_ratings[0].keys()
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(filtered_ratings)
        
        if len(existing_ratings) == len(filtered_ratings):
            return False
        else:
            return True
    return False

def recommend_with_ratings(user_id, favorite_genre, page):

    user_ratings = pd.read_csv('./csv/user_ratings.csv')

    curry_genres = pd.read_csv('./csv/genres.csv')

    user_ratings = user_ratings.merge(curry_genres, left_on='id', right_on='id')

    user_profile = user_ratings[user_ratings['userId'] == user_id]

    X_train, X_test, y_train, y_test = train_test_split(user_profile[curry_genres.columns], user_profile['rating'], random_state=42, test_size=0.1)

    lasso = Lasso(alpha=0.005)

    lasso.fit(X_train, y_train)

    predictions = lasso.predict(curry_genres)
    curry_genres['predict'] = predictions

    if favorite_genre is None:
        sorted_user_predict = curry_genres.sort_values(by='predict', ascending=False)
    else:
        sorted_user_predict = curry_genres.sort_values(by=['predict', favorite_genre], ascending=[False, False])

    user_predict_ids = sorted_user_predict.id.tolist()

    start_idx = (page - 1) * 10
    end_idx = start_idx + 10

    if start_idx >= len(user_predict_ids):
        return None

    return user_predict_ids[start_idx:end_idx]
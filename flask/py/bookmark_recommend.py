import pandas as pd

def recommend_with_bookmark(recipe_id, page):

    curry_genres = pd.read_csv('./csv/genres.csv', index_col = 'id')
    genres = curry_genres.loc[recipe_id, 'ing1':'ing25']
    selected_genres = genres[genres == 1].index

    genre_scores = {}
    for idx, row in curry_genres.iterrows():
      if all(row[genre] == 1 for genre in selected_genres):
        genre_score = sum(row[genre] == 1 for genre in genres.index if genres[genre] == 1)
        genre_score += sum(row[genre] == 0 for genre in genres.index if genres[genre] == 0)
        genre_scores[idx] = genre_score

    sorted_genre_scores = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)

    similar_recipe_ids = [recipe_id for recipe_id, similarity_score in sorted_genre_scores]
    similar_recipe_ids = [id for id in similar_recipe_ids if id != recipe_id]

    start_idx = (page - 1) * 5
    end_idx = start_idx + 5

    if start_idx >= len(similar_recipe_ids):
        return None

    return similar_recipe_ids[start_idx:end_idx]
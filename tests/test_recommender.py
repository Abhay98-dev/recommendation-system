import unittest
import pandas as pd
from src.recommender import recommend

def frame():
    return pd.DataFrame([
        {"movie_id":"1","title":"Action One","genres":"Action|Thriller","release_year":2018,"language":"Hindi","rating":8.0,"duration":110,"mood":"Exciting","themes":"space|family","audience":"Adult","popularity":80,"description":"An action story about space travel","poster_color":"#123456"},
        {"movie_id":"2","title":"Quiet Two","genres":"Drama","release_year":2005,"language":"English","rating":7.0,"duration":85,"mood":"Relaxing","themes":"garden|friendship","audience":"Family","popularity":50,"description":"A calm garden tale","poster_color":"#123456"},
        {"movie_id":"3","title":"Low Three","genres":"Action","release_year":2022,"language":"Hindi","rating":4.0,"duration":130,"mood":"Exciting","themes":"space","audience":"Adult","popularity":90,"description":"Space action","poster_color":"#123456"},
    ])

class RecommenderTests(unittest.TestCase):
    def test_genre_language_mood_and_keyword_affect_scores(self):
        movies=frame()
        base=recommend(movies, min_rating=1)
        targeted=recommend(movies, ["Action"], "Hindi", "Exciting", 1, keyword="space")
        self.assertGreater(targeted.loc[targeted.movie_id=="1","score"].iloc[0], base.loc[base.movie_id=="1","score"].iloc[0])
        self.assertIn("Hindi", targeted.loc[targeted.movie_id=="1","explanation"].iloc[0])
        self.assertIn("Exciting", targeted.loc[targeted.movie_id=="1","explanation"].iloc[0])
        self.assertIn("space", targeted.loc[targeted.movie_id=="1","explanation"].iloc[0])
    def test_mandatory_filters(self):
        out=recommend(frame(), min_rating=6, release_period="2020 onward", duration="Under 90 minutes")
        self.assertTrue(out.empty)
        out=recommend(frame(), min_rating=6, release_period="2000–2009", duration="Under 90 minutes")
        self.assertEqual(out.movie_id.tolist(), ["2"])
    def test_sorted_deterministic_unique_and_bounded(self):
        a=recommend(frame(), ["Action"], min_rating=1)
        b=recommend(frame(), ["Action"], min_rating=1)
        self.assertEqual(a.movie_id.tolist(), b.movie_id.tolist())
        self.assertEqual(a.score.tolist(), b.score.tolist())
        self.assertEqual(a.score.tolist(), sorted(a.score.tolist(), reverse=True))
        self.assertTrue(a.movie_id.is_unique)
        self.assertTrue(a.score.between(0,100).all())
    def test_empty_and_any_preferences(self):
        self.assertTrue(recommend(frame(), min_rating=10).empty)
        out=recommend(frame(), language="Any", mood="Any", min_rating=1)
        self.assertEqual(len(out), 3)
        self.assertTrue(out.explanation.str.len().gt(0).all())

if __name__ == "__main__": unittest.main()

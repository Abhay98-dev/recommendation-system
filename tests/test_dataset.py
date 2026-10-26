import unittest
import pandas as pd
from src.data_loader import load_movies
from src.validators import validate_movies

class DatasetTests(unittest.TestCase):
    def test_bundled_dataset(self):
        data=load_movies()
        self.assertGreaterEqual(len(data),150)
        self.assertTrue(data.movie_id.is_unique)
        self.assertTrue(data.title.str.casefold().is_unique)
        self.assertTrue(data.rating.between(1,10).all())
        self.assertEqual(validate_movies(data), [])
    def test_invalid_values_detected(self):
        data=load_movies().head(2).copy()
        data.loc[data.index[1],"movie_id"] = data.iloc[0].movie_id
        data.loc[data.index[1],"rating"] = 11
        data.loc[data.index[0],"description"] = ""
        errors=validate_movies(data)
        self.assertTrue(any("unique" in error for error in errors))
        self.assertTrue(any("rating" in error for error in errors))
        self.assertTrue(any("description" in error for error in errors))
    def test_missing_column_detected(self):
        self.assertTrue(any("Missing required columns" in e for e in validate_movies(pd.DataFrame({"title": ["x"]}))))

if __name__ == "__main__": unittest.main()

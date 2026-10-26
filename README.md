# CineSuggest — Smart Movie Recommendations

## Abstract

CineSuggest is a local movie discovery application built with Python, Pandas, and Streamlit. It uses a deterministic rule-based inference process to filter and rank films against explicit preferences. It does not train or use a machine learning model.

## Problem statement and objectives

Finding a film that fits a viewer's genre, language, mood, rating, release period, and runtime preferences can be time-consuming. This mini project demonstrates how an explainable knowledge base and IF/THEN rules can make that selection more relevant. Objectives are to collect preferences, enforce hard constraints, rank matching films, and explain the resulting scores.

## Scope and technologies

The application runs offline from a bundled CSV and has no API, database, account, or network dependency. Python 3.10+, Streamlit, Pandas, CSV, and the standard library are used. The bundled ratings and popularity values are illustrative academic demo values, not verified current statistics.

## Architecture

`data/movies.csv` is the knowledge base. `src/data_loader.py` loads it and `src/validators.py` checks required attributes and value ranges. `src/recommender.py` applies mandatory filters and scoring rules. `app.py` presents the preferences, recommendations, browse view, session favorites, statistics, and a rule explanation. `scripts/generate_dataset.py` reproducibly regenerates the local data.

## Dataset

The CSV contains 168 unique movies and 13 fields: `movie_id`, `title`, `genres`, `release_year`, `language`, `rating`, `duration`, `mood`, `themes`, `audience`, `popularity`, `description`, and `poster_color`. Multi-valued genres and themes use `|`. The catalog contains recognizable films and clearly fictional entries prefixed `Demo:`. Fictional descriptions are demo examples, not claims about real films.

## Rule-based recommendation methodology

The engine first excludes records below the minimum rating or outside the chosen release-year and duration ranges. It then computes a deterministic preference score:

| Rule | Maximum |
|---|---:|
| Genre overlap | 40 |
| Selected language | 15 |
| Selected mood | 20 |
| Keyword matches in title, themes, genres, or description | 10 |
| Rating quality | 10 |
| Popularity bonus | 5 |

The score is the sum of these components, capped at 100. Genre points are proportional to the number of chosen genres matched. Keyword points are proportional to matched search terms. Rating bonus scales linearly from zero at 5/10 to ten at 10/10. Popularity contributes at most five points. `Any` language or mood contributes zero and creates no penalty. Results sort by score descending, rating descending, and title ascending, with movie ID duplicates removed. The default limit is ten.

Explanations are built from each movie's actual matched conditions. A movie below the user's minimum rating, outside a selected year range, or outside a runtime range cannot appear.

### Example inference rules

- IF the user selects Action AND a movie contains Action, THEN add genre points.
- IF the user selects Hindi AND the movie language is Hindi, THEN add language points.
- IF movie rating is below the minimum, THEN exclude the movie.
- IF movie year or duration violates the selected range, THEN exclude the movie.

## Example workflow

Choose Action and Hindi, select an Exciting mood, set a 6.5 minimum rating, and enter `family`. The engine removes films that fail the rating/year/runtime constraints, scores the remaining catalog on matching rules, and returns the top ten with scores and explanations. Repeating the same inputs against the same CSV returns the same results.

## Project structure

```text
app.py
requirements.txt
README.md
data/movies.csv
src/{__init__.py,data_loader.py,recommender.py,validators.py}
scripts/generate_dataset.py
tests/{test_dataset.py,test_recommender.py}
assets/styles.css (reserved for optional custom styles)
```

## Installation and use

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_dataset.py
streamlit run app.py
```

The generated CSV is committed as a project file, so generation is optional unless you want to recreate it. Run the automated checks with:

```bash
python -m unittest discover -s tests -v
```

## Advantages

- Explicit rules are easy to inspect, explain, and adjust.
- No internet, external service, user account, or training data is needed.
- Filtering protects hard user constraints, and explanations show why a result ranked.
- Dataset generation is reproducible.

## Limitations and assumptions

- Ratings and popularity are illustrative rather than verified.
- Movie attributes and the catalog are finite and manually curated/generated; quality depends on their completeness.
- Keyword matching is literal substring matching and does not understand synonyms or context.
- Favorites last only for the current browser session.
- This system does not learn from viewing history and is not collaborative filtering or machine learning.

## Future enhancements

Possible extensions include a larger licensed dataset, editable rule weights, CSV export, persistent local favorites, multilingual keyword normalization, and an examiner-facing evaluation of precision on a hand-labeled sample.

## Conclusion

CineSuggest demonstrates a complete rule-based recommendation pipeline: a structured knowledge base, preference facts, hard constraint filters, transparent inference scores, ranked output, and dynamic explanations. Its behavior is deterministic and suitable for an AI mini-project demonstration.

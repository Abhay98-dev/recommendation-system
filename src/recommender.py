"""Transparent, deterministic movie filtering and rule-based scoring."""
from __future__ import annotations
import re
import pandas as pd

GENRE_WEIGHT = 40
LANGUAGE_WEIGHT = 15
MOOD_WEIGHT = 20
KEYWORD_WEIGHT = 10
RATING_WEIGHT = 10
POPULARITY_WEIGHT = 5
SCORING_WEIGHTS = {"Genre match": GENRE_WEIGHT, "Language match": LANGUAGE_WEIGHT, "Mood match": MOOD_WEIGHT, "Theme/keyword match": KEYWORD_WEIGHT, "Rating bonus": RATING_WEIGHT, "Popularity bonus": POPULARITY_WEIGHT}
PERIODS = {"Any year": (None, None), "Before 2000": (None, 1999), "2000–2009": (2000, 2009), "2010–2019": (2010, 2019), "2020 onward": (2020, None)}
DURATIONS = {"Any duration": (None, None), "Under 90 minutes": (None, 89), "90–120 minutes": (90, 120), "Over 120 minutes": (121, None)}


def _parts(value: str) -> set[str]:
    return {item.strip().casefold() for item in str(value).split("|") if item.strip()}


def recommend(movies: pd.DataFrame, genres: list[str] | None = None, language: str = "Any", mood: str = "Any", min_rating: float = 0.0, release_period: str = "Any year", duration: str = "Any duration", keyword: str = "", limit: int = 10) -> pd.DataFrame:
    """Filter mandatory constraints, then rank on a 100 point preference score."""
    genres = genres or []
    if release_period not in PERIODS or duration not in DURATIONS:
        raise ValueError("Unknown release period or duration preference.")
    start, end = PERIODS[release_period]
    dmin, dmax = DURATIONS[duration]
    keep = pd.Series(True, index=movies.index)
    keep &= pd.to_numeric(movies.rating, errors="coerce").ge(float(min_rating))
    if start is not None: keep &= movies.release_year.ge(start)
    if end is not None: keep &= movies.release_year.le(end)
    if dmin is not None: keep &= movies.duration.ge(dmin)
    if dmax is not None: keep &= movies.duration.le(dmax)
    result = movies.loc[keep].copy()
    wanted = {g.casefold() for g in genres}
    words = [w.casefold() for w in re.findall(r"[\w'-]+", keyword) if len(w) > 1]
    scores, reasons = [], []
    for _, movie in result.iterrows():
        why: list[str] = []
        movie_genres = _parts(movie.genres)
        matches = wanted & movie_genres
        genre_score = round(GENRE_WEIGHT * len(matches) / len(wanted)) if wanted else 0
        if matches: why.append("Matches your " + ", ".join(sorted((g.title() for g in matches))) + " genre preference" + ("s" if len(matches) > 1 else ""))
        language_score = LANGUAGE_WEIGHT if language != "Any" and str(movie.language).casefold() == language.casefold() else 0
        if language_score: why.append(f"Matches your selected language: {movie.language}")
        mood_score = MOOD_WEIGHT if mood != "Any" and str(movie.mood).casefold() == mood.casefold() else 0
        if mood_score: why.append(f"Matches your preferred mood: {movie.mood}")
        searchable = " ".join(str(movie[c]) for c in ("themes", "description", "title", "genres")).casefold()
        hits = [w for w in words if w in searchable]
        keyword_score = min(KEYWORD_WEIGHT, KEYWORD_WEIGHT * len(hits) / len(words)) if words else 0
        if hits: why.append("Matches your keyword: " + ", ".join(hits))
        rating_score = RATING_WEIGHT * max(0, min(1, (float(movie.rating) - 5) / 5))
        if float(movie.rating) >= float(min_rating): why.append("Meets your minimum rating requirement")
        popularity_score = POPULARITY_WEIGHT * float(movie.popularity) / 100
        scores.append(round(min(100, genre_score + language_score + mood_score + keyword_score + rating_score + popularity_score), 1))
        if not why: why.append("Meets your filters; rating and popularity provide the ranking score")
        reasons.append(" · ".join(why))
    result["score"] = scores
    result["explanation"] = reasons
    return result.sort_values(["score", "rating", "title"], ascending=[False, False, True], kind="stable").drop_duplicates("movie_id").head(max(0, int(limit))).reset_index(drop=True)

"""Validation helpers for the local movie knowledge base."""
from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = ["movie_id", "title", "genres", "release_year", "language", "rating", "duration", "mood", "themes", "audience", "popularity", "description", "poster_color"]


def validate_movies(data: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        return [f"Missing required columns: {', '.join(missing)}"]
    if data[REQUIRED_COLUMNS].isna().any().any():
        errors.append("Required fields contain missing values.")
    if data.movie_id.duplicated().any():
        errors.append("Movie IDs must be unique.")
    if data.title.astype(str).str.strip().str.casefold().duplicated().any():
        errors.append("Movie titles must be unique.")
    for column, low, high in (("rating", 1, 10), ("popularity", 1, 100), ("release_year", 1990, 2026), ("duration", 1, 500)):
        values = pd.to_numeric(data[column], errors="coerce")
        if values.isna().any() or not values.between(low, high).all():
            errors.append(f"{column} values must be numeric and between {low} and {high}.")
    for column in ("genres", "language", "mood", "themes", "audience", "description", "poster_color"):
        if data[column].astype(str).str.strip().eq("").any():
            errors.append(f"{column} cannot be blank.")
    return errors

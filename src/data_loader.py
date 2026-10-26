"""Load and validate the bundled CSV dataset."""
from pathlib import Path
import pandas as pd
from .validators import validate_movies

ROOT = Path(__file__).resolve().parents[1]


def load_movies(path: str | Path | None = None) -> pd.DataFrame:
    source = Path(path) if path else ROOT / "data" / "movies.csv"
    if not source.exists():
        raise FileNotFoundError(f"Movie dataset not found: {source}. Run python scripts/generate_dataset.py")
    try:
        movies = pd.read_csv(source)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise ValueError(f"Could not read movie dataset {source}: {exc}") from exc
    errors = validate_movies(movies)
    if errors:
        raise ValueError("Invalid movie dataset: " + " ".join(errors))
    movies["release_year"] = movies.release_year.astype(int)
    movies["duration"] = movies.duration.astype(int)
    movies["rating"] = movies.rating.astype(float)
    movies["popularity"] = movies.popularity.astype(int)
    return movies

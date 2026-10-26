"""CineSuggest: local, explainable, rule-based movie discovery."""
from pathlib import Path
import streamlit as st
import pandas as pd
from src.data_loader import load_movies
from src.recommender import recommend, SCORING_WEIGHTS

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="CineSuggest", page_icon="🎬", layout="wide")

st.markdown("""
<style>
.stApp {background: radial-gradient(ellipse at 15% 0%, #252047 0, #11121b 44%, #0b0c12 100%); color:#f4f2ff}
[data-testid="stSidebar"] {background:#12131d; border-right:1px solid #292a3b}
.hero {padding:2.1rem 2.3rem; border:1px solid #38344f; border-radius:24px; background:linear-gradient(120deg,#292044,#171a2a 65%,#172c38); margin:.7rem 0 1.5rem}
.hero h1 {font-size:2.7rem; margin:0; color:#fff}
.hero p {color:#c3bfd4; font-size:1.07rem; margin:.6rem 0 0}
.movie {height:100%; border:1px solid #303144; border-radius:18px; background:#171823; overflow:hidden; margin-bottom:1rem}
.poster {height:94px; padding:16px 18px; display:flex; align-items:end; color:white; font-weight:800; font-size:1.1rem; text-shadow:0 2px 8px #0008}
.moviebody {padding:14px 16px 17px}.muted {color:#aaa9bd;font-size:.88rem}.score {color:#a78bfa;font-weight:800}
.tag {display:inline-block;background:#29283b;border-radius:14px;padding:3px 9px;margin:2px;font-size:.77rem;color:#d2c9ff}
</style>""", unsafe_allow_html=True)

try:
    movies = load_movies()
except (FileNotFoundError, ValueError) as error:
    st.error(str(error)); st.stop()

genres = sorted({g.strip() for values in movies.genres for g in values.split("|")})
languages = sorted(movies.language.unique())
moods = sorted(movies.mood.unique())
with st.sidebar:
    st.markdown("## 🎬 CineSuggest")
    st.caption("A movie discovery studio powered by transparent rules")
    st.divider()
    chosen_genres = st.multiselect("Genres", genres, default=["Science Fiction"] if "Science Fiction" in genres else [], key="pref_genres")
    language = st.selectbox("Language", ["Any", *languages], key="pref_language")
    mood = st.selectbox("Mood", ["Any", *moods], key="pref_mood")
    min_rating = st.slider("Minimum rating", 1.0, 10.0, 6.5, 0.5, key="pref_rating")
    period = st.selectbox("Release period", ["Any year", "Before 2000", "2000–2009", "2010–2019", "2020 onward"], key="pref_period")
    duration = st.selectbox("Maximum duration / runtime", ["Any duration", "Under 90 minutes", "90–120 minutes", "Over 120 minutes"], key="pref_duration")
    keyword = st.text_input("Theme or keyword", placeholder="e.g. family, friendship", key="pref_keyword")
    submitted = st.button("✨ Find my movies", type="primary", use_container_width=True)
    if st.button("Reset preferences", use_container_width=True):
        for key in ("pref_genres", "pref_language", "pref_mood", "pref_rating", "pref_period", "pref_duration", "pref_keyword", "results"):
            st.session_state.pop(key, None)
        st.rerun()

if "favorites" not in st.session_state: st.session_state.favorites = []
if submitted:
    st.session_state.results = recommend(movies, chosen_genres, language, mood, min_rating, period, duration, keyword)
    st.session_state.last_filters = {"genres": chosen_genres, "language": language, "mood": mood, "rating": min_rating, "period": period, "duration": duration, "keyword": keyword}
results = st.session_state.get("results", recommend(movies, chosen_genres, language, mood, min_rating, period, duration, keyword))

st.markdown('<div class="hero"><h1>Find a film that feels like yours.</h1><p>Discover your next favorite movie through intelligent, preference-based recommendations.</p></div>', unsafe_allow_html=True)
st.write("CineSuggest compares your preferences with a local movie knowledge base. Every result is filtered and scored by explicit rules, so recommendations are relevant, repeatable, and easy to explain.")
tabs = st.tabs(["✨ Recommendations", "🔎 Browse all", "💜 Favorites", "📊 Insights", "🧠 How it works"])

def movie_card(movie, show_score=True):
    title = str(movie.title)
    st.markdown(f'''<div class="movie"><div class="poster" style="background:linear-gradient(0deg,#111a 0%,transparent 100%),{movie.poster_color}">{title}</div><div class="moviebody"><div class="muted">{int(movie.release_year)} · {movie.language} · {int(movie.duration)} min · ⭐ {movie.rating:.1f}/10</div><div>{''.join(f'<span class="tag">{g.strip()}</span>' for g in str(movie.genres).split('|'))}</div><p>{movie.description}</p>{f'<div class="score">Match score {movie.score:.1f}/100</div><div class="muted">{movie.explanation}</div>' if show_score else ''}</div></div>''', unsafe_allow_html=True)
    label = "♥ Saved" if title in st.session_state.favorites else "♡ Save"
    if st.button(label, key=f"fav_{movie.movie_id}"):
        if title in st.session_state.favorites: st.session_state.favorites.remove(title)
        else: st.session_state.favorites.append(title)
        st.rerun()

with tabs[0]:
    st.subheader("Your recommendations")
    st.caption("Adjust preferences in the sidebar and select Find my movies to refresh.")
    if results.empty: st.info("No movies meet every selected requirement. Try lowering the rating or widening the release and duration filters.")
    else:
        cols = st.columns(2)
        for i, movie in results.iterrows():
            with cols[i % 2]: movie_card(movie)
with tabs[1]:
    st.subheader("Browse the collection")
    q = st.text_input("Search title, theme, description, or genre", key="browse_search")
    bg = st.multiselect("Filter genres", genres, key="browse_genres")
    view = movies.copy()
    if q:
        mask = view[["title", "themes", "description", "genres"]].astype(str).agg(" ".join, axis=1).str.contains(q, case=False, regex=False)
        view = view[mask]
    if bg: view = view[view.genres.apply(lambda x: bool(set(bg) & set(x.split("|"))))]
    st.caption(f"Showing {len(view)} of {len(movies)} movies")
    for start in range(0, len(view), 3):
        cols = st.columns(3)
        for col, (_, movie) in zip(cols, view.iloc[start:start+3].iterrows()):
            with col: movie_card(movie, show_score=False)
with tabs[2]:
    st.subheader("Your saved movies")
    saved = movies[movies.title.isin(st.session_state.favorites)]
    if saved.empty: st.info("Save a movie from recommendations or Browse to keep it here for this session.")
    for _, movie in saved.iterrows(): movie_card(movie, show_score=False)
with tabs[3]:
    st.subheader("Collection insights")
    a, b, c = st.columns(3)
    a.metric("Movies in collection", len(movies))
    b.metric("Highest-rated in results", f"{results.rating.max():.1f}/10" if not results.empty else "—")
    common = results.genres.str.split("|").explode().str.strip().value_counts().index[0] if not results.empty else "—"
    c.metric("Most common result genre", common)
    st.markdown("#### Collection by language")
    st.bar_chart(movies.language.value_counts())
    if not results.empty:
        st.markdown("#### Your result genres")
        st.bar_chart(results.genres.str.split("|").explode().str.strip().value_counts())
with tabs[4]:
    st.subheader("How the Recommendation Engine Works")
    st.write("A rule-based system applies human-written IF/THEN rules to a knowledge base. Here, movie attributes form the knowledge base, your selections are the input facts, and filtering plus scoring infer a ranked recommendation list.")
    st.markdown("**Example rules**\n\n- IF you select Action AND a movie has the Action genre, THEN increase its genre score.\n- IF you select Hindi AND a movie is in Hindi, THEN add language points.\n- IF a movie rating is below your minimum, THEN exclude it.\n- IF its year or runtime violates your selected range, THEN exclude it.")
    st.markdown("**Scoring weights**")
    st.dataframe(pd.DataFrame([{"Rule": k, "Maximum points": v} for k, v in SCORING_WEIGHTS.items()]), hide_index=True, use_container_width=True)
    st.write("Genre points are proportional to selected genres matched (up to 40). Language adds 15, mood 20, matching keywords up to 10, rating quality up to 10, and popularity at most 5. The maximum is capped at 100. Unselected language and mood do not penalize a movie. Mandatory filters run first; remaining movies sort by score, then rating, then title.")
    st.write("The system is deterministic: identical data and preferences always produce the same ordering. Unlike a machine learning recommender, it does not train on user behavior or infer hidden patterns; its rules are visible and adjustable.")
    st.caption("Demo ratings and popularity are illustrative values for this academic project, not verified current statistics. Fictional records are labeled Demo:.")

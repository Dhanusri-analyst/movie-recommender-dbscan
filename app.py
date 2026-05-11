import streamlit as st
import pandas as pd
import pickle
import random
import numpy as np

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="ReelMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    background-color: #0a0a0f;
    color: #e8e8e8;
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1100px; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem 0;
    position: relative;
}
.hero-tag {
    display: inline-block;
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #e5383b;
    border: 1px solid #e5383b44;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 8vw, 6.5rem);
    letter-spacing: 0.06em;
    line-height: 1;
    color: #ffffff;
    margin: 0;
}
.hero-title span { color: #e5383b; }
.hero-sub {
    font-size: 1rem;
    color: #888;
    margin-top: 0.8rem;
    font-weight: 300;
    letter-spacing: 0.03em;
}
.hero-line {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, #e5383b, transparent);
    margin: 1.5rem auto 0 auto;
}

/* ── Search box ── */
.stTextInput > div > div > input {
    background: #13131a !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1.2rem !important;
    transition: border-color 0.3s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #e5383b !important;
    box-shadow: 0 0 0 3px #e5383b22 !important;
}
.stTextInput > div > div > input::placeholder { color: #555 !important; }
.stTextInput label {
    color: #aaa !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
.stButton > button {
    background: #e5383b !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 0.65rem 2.2rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    background: #c1121f !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px #e5383b44 !important;
}

/* ── Movie card ── */
.movie-card {
    background: #13131a;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.25s, transform 0.25s;
    position: relative;
    overflow: hidden;
}
.movie-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: #e5383b;
    border-radius: 3px 0 0 3px;
    opacity: 0;
    transition: opacity 0.25s;
}
.movie-card:hover {
    border-color: #e5383b44;
    transform: translateX(4px);
}
.movie-card:hover::before { opacity: 1; }
.card-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #2a2a3a;
    min-width: 2.5rem;
    line-height: 1;
}
.card-body { flex: 1; }
.card-title {
    font-size: 1rem;
    font-weight: 500;
    color: #f0f0f0;
    margin-bottom: 0.3rem;
}
.card-meta {
    font-size: 0.8rem;
    color: #666;
    display: flex;
    gap: 1rem;
}
.card-badge {
    background: #1e1e2e;
    border: 1px solid #2a2a3a;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.75rem;
    color: #e5383b;
    font-weight: 500;
}
.imdb-score {
    background: #f5c518;
    color: #000;
    border-radius: 5px;
    padding: 2px 8px;
    font-size: 0.75rem;
    font-weight: 700;
}

/* ── Found movie banner ── */
.found-banner {
    background: linear-gradient(135deg, #13131a 0%, #1a0a0a 100%);
    border: 1px solid #e5383b33;
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.found-icon { font-size: 2rem; }
.found-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.15em; color: #e5383b; margin-bottom: 3px; }
.found-title { font-size: 1.1rem; font-weight: 500; color: #fff; }
.found-cluster { font-size: 0.8rem; color: #666; margin-top: 2px; }

/* ── Section heading ── */
.section-heading {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.1em;
    color: #fff;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #2a2a3a, transparent);
}

/* ── Error / warning ── */
.err-box {
    background: #1a0a0a;
    border: 1px solid #e5383b55;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    color: #e5383b;
    font-size: 0.9rem;
}
.noise-box {
    background: #13130a;
    border: 1px solid #f5c51855;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    color: #f5c518;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

/* ── Stats strip ── */
.stats-strip {
    display: flex;
    gap: 1.5rem;
    margin: 2rem 0 1rem 0;
    flex-wrap: wrap;
}
.stat-box {
    background: #13131a;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    flex: 1;
    min-width: 130px;
    text-align: center;
}
.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #e5383b;
    line-height: 1;
}
.stat-label { font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }

/* ── Divider ── */
.divider { height: 1px; background: #1e1e2e; margin: 2rem 0; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: #333;
    font-size: 0.78rem;
    margin-top: 4rem;
    letter-spacing: 0.05em;
}
.footer span { color: #e5383b; }
</style>
""", unsafe_allow_html=True)


# ── Load assets ──────────────────────────────────────────────
@st.cache_resource
def load_assets():
    with open('dbscan_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('pca_model.pkl', 'rb') as f:
        pca = pickle.load(f)
    df = pd.read_csv('movies_cleaned.csv', index_col='title')
    return model, scaler, pca, df

try:
    dbscan_model, scaler, pca, df_movies = load_assets()
    assets_loaded = True
except Exception as e:
    assets_loaded = False
    load_error = str(e)


# ── Recommendation function ───────────────────────────────────
def recommend(movie_name, n=6):
    name_lower = movie_name.strip().lower()
    df_movies['_lower'] = df_movies.index.str.lower()
    matches = df_movies[df_movies['_lower'].str.contains(name_lower, na=False)]
    df_movies.drop('_lower', axis=1, inplace=True, errors='ignore')

    if matches.empty:
        return None, None, None, "not_found"

    movie_row   = matches.iloc[0]
    actual_title = matches.index[0]
    cluster      = movie_row.get('dbscan_clusters', -1)
    is_noise     = (cluster == -1)

    if is_noise:
        cluster = df_movies[df_movies['dbscan_clusters'] != -1]['dbscan_clusters'].value_counts().idxmax()

    pool = df_movies[
        (df_movies['dbscan_clusters'] == cluster) &
        (df_movies.index != actual_title)
    ]

    if pool.empty:
        return actual_title, cluster, [], "empty_cluster"

    sample_size  = min(n, len(pool))
    recommended  = pool.sample(sample_size)
    return actual_title, cluster, recommended, "noise" if is_noise else "ok"


# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">DBSCAN Clustering · AI Powered</div>
    <h1 class="hero-title">REEL<span>MATCH</span></h1>
    <p class="hero-sub">Discover movies that truly match your taste — powered by density-based clustering</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Stats strip ───────────────────────────────────────────────
if assets_loaded:
    total_movies  = len(df_movies)
    total_clusters = df_movies['dbscan_clusters'].nunique() - (1 if -1 in df_movies['dbscan_clusters'].values else 0)
    noise_pct     = round((df_movies['dbscan_clusters'] == -1).sum() / total_movies * 100, 1)

    st.markdown(f"""
    <div class="stats-strip">
        <div class="stat-box">
            <div class="stat-num">{total_movies:,}</div>
            <div class="stat-label">Total Movies</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{total_clusters}</div>
            <div class="stat-label">Clusters Found</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">3</div>
            <div class="stat-label">Platforms</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">DBSCAN</div>
            <div class="stat-label">Algorithm</div>
        </div>
    </div>
    <div class="divider"></div>
    """, unsafe_allow_html=True)

# ── Search UI ─────────────────────────────────────────────────
if not assets_loaded:
    st.markdown(f'<div class="err-box">⚠️ Could not load model files: {load_error}</div>', unsafe_allow_html=True)
else:
    col1, col2 = st.columns([4, 1], gap="medium")
    with col1:
        movie_input = st.text_input(
            "Movie Name",
            placeholder="e.g.  Inception,  Parasite,  The Dark Knight ...",
            label_visibility="visible"
        )
    with col2:
        st.markdown("<div style='height:1.95rem'></div>", unsafe_allow_html=True)
        search_clicked = st.button("Find Matches →")

    # ── Results ───────────────────────────────────────────────
    if search_clicked and movie_input.strip():
        title, cluster, results, status = recommend(movie_input.strip())

        if status == "not_found":
            st.markdown(f'<div class="err-box">🎬 Could not find <strong>"{movie_input}"</strong> in our database. Try a different title or check the spelling.</div>', unsafe_allow_html=True)

        else:
            # Found movie banner
            imdb_val = df_movies.loc[title, 'imdb_score'] if 'imdb_score' in df_movies.columns else 'N/A'
            imdb_str = f"{imdb_val:.1f}" if isinstance(imdb_val, float) else str(imdb_val)

            st.markdown(f"""
            <div class="found-banner">
                <div class="found-icon">🎬</div>
                <div>
                    <div class="found-label">Now matching based on</div>
                    <div class="found-title">{title}</div>
                    <div class="found-cluster">Cluster #{cluster} &nbsp;·&nbsp; IMDb {imdb_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if status == "noise":
                st.markdown('<div class="noise-box">⚡ This title sits outside main clusters (noise point). Showing recommendations from the closest cluster.</div>', unsafe_allow_html=True)

            if status == "empty_cluster" or (results is not None and len(results) == 0):
                st.markdown('<div class="err-box">No similar movies found in this cluster. Try another title!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="section-heading">Recommended For You</div>', unsafe_allow_html=True)

                for i, (rec_title, row) in enumerate(results.iterrows(), 1):
                    imdb  = row.get('imdb_score', None)
                    genre = row.get('main_genre', '')
                    yr    = row.get('release_year', '')
                    mtype = row.get('type', '')

                    imdb_html = f'<span class="imdb-score">⭐ {imdb:.1f}</span>' if isinstance(imdb, float) else ''
                    genre_html = f'<span class="card-badge">{genre}</span>' if genre else ''

                    st.markdown(f"""
                    <div class="movie-card">
                        <div class="card-num">0{i}</div>
                        <div class="card-body">
                            <div class="card-title">{rec_title}</div>
                            <div class="card-meta">
                                {imdb_html}
                                {genre_html}
                                <span style="color:#555">{yr} &nbsp; {mtype}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    elif search_clicked and not movie_input.strip():
        st.markdown('<div class="err-box">Please enter a movie name to search.</div>', unsafe_allow_html=True)

    # ── Divider + How it works ────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">How ReelMatch Works</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="large")
    for col, icon, title_t, desc in [
        (c1, "🗂️", "Data Clustering", "DBSCAN groups thousands of movies by genre, IMDb score, popularity and runtime — without needing a fixed number of clusters."),
        (c2, "🔍", "Smart Matching",  "When you search, ReelMatch finds which cluster your movie belongs to and picks the most similar titles from that group."),
        (c3, "🎯", "Noise Handling",  "Unlike KMeans, DBSCAN gracefully handles outlier movies — unique titles that don't fit neatly into any cluster."),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-box" style="text-align:left; padding:1.3rem 1.5rem">
                <div style="font-size:1.6rem; margin-bottom:0.6rem">{icon}</div>
                <div style="font-weight:500; color:#f0f0f0; margin-bottom:0.4rem">{title_t}</div>
                <div style="font-size:0.82rem; color:#666; line-height:1.6">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with <span>♥</span> using Python · DBSCAN · Streamlit &nbsp;·&nbsp; Team 11
</div>
""", unsafe_allow_html=True)

   

import streamlit as st
import joblib
import requests
import pandas as pd # <-- NEW: For TV Shows Dataframe
from textblob import TextBlob
import base64 # <-- NEW: Local background image ko parhne ke liye

# 1. UPGRADED: API Fetcher for Poster + Movie Details (Rating, Year, Cast & Story)
def fetch_details(item_id, media_type="movie"): # <-- ADDED media_type to support TV
    api_key = "API_KEY" # <--- 1. APNI API KEY YAHAN DALO
    # Modified URL to use media_type dynamically
    url = f"https://api.themoviedb.org/3/{media_type}/{item_id}?api_key={api_key}&language=en-US&append_to_response=credits"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # Poster logic
        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            poster = "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            poster = "https://www.prokerala.com/movies/assets/img/no-poster-available.jpg"
            
        # Rating & Year logic
        rating = round(data.get('vote_average', 0), 1) 
        # TV shows use 'first_air_date', Movies use 'release_date'
        date = data.get('release_date', data.get('first_air_date', 'N/A')) 
        year = date.split('-')[0] if date != 'N/A' else 'N/A' 
        
        # Story & Cast logic
        overview = data.get('overview', 'No story available.')
        cast_data = data.get('credits', {}).get('cast', [])
        cast_names = [actor['name'] for actor in cast_data[:3]] 
        cast = ", ".join(cast_names) if cast_names else "Unknown"
        
        return poster, rating, year, overview, cast
    except:
        return "https://www.prokerala.com/movies/assets/img/no-poster-available.jpg", 0, "N/A", "N/A", "N/A"

# 2. API Fetcher for YouTube Trailer
def fetch_trailer(item_id, media_type="movie"): # <-- ADDED media_type
    api_key = "API_KEY" # <--- 2. APNI API KEY YAHAN BHI DALO
    url = f"https://api.themoviedb.org/3/{media_type}/{item_id}/videos?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        for video in data.get('results', []):
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                return f"https://www.youtube.com/watch?v={video['key']}"
        return "https://www.youtube.com/results?search_query=movie+trailer"
    except:
        return "https://www.youtube.com/results?search_query=movie+trailer"

# 3. AI Sentiment Analysis Fetcher
def analyze_sentiment(item_id, media_type="movie"): # <-- ADDED media_type
    api_key = "API_KEY" # <--- 3. APNI API KEY YAHAN BHI DALO
    url = f"https://api.themoviedb.org/3/{media_type}/{item_id}/reviews?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        reviews = data.get('results', [])
        
        if not reviews:
            return "⭐ No Reviews Yet"
            
        positive_count = 0
        total_reviews = min(len(reviews), 5)
        
        for r in reviews[:total_reviews]:
            analysis = TextBlob(r['content'])
            if analysis.sentiment.polarity > 0: 
                positive_count += 1
                
        score = int((positive_count / total_reviews) * 100)
        
        if score >= 60:
            return f"🔥 {score}% Positive Reviews"
        elif score >= 40:
            return f"😐 {score}% Mixed Reviews"
        else:
            return f"🤢 {score}% Negative Reviews"
    except:
        return "⭐ Rating Not Available"

# 4. Page Styling & VIP Netflix CSS
st.set_page_config(page_title="AI Movie Expert", page_icon="🎬", layout="wide")

# --- 🔥 NEW: FUNCTION TO LOAD LOCAL IMAGE FOR BACKGROUND ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# Read the local Netflix logo from your folder
bg_image_base64 = get_base64_of_bin_file('netflix_logo.png')

# Inject local image into Background CSS directly
if bg_image_base64:
    # 🔥 FIX: Lightened the gradient (0.65) and increased size to 50vw so logo pops out!
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: #000000 !important;
            background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.95)), url("data:image/png;base64,{bg_image_base64}") !important;
            background-size: 140vw !important; 
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
    </style>
    """, unsafe_allow_html=True)
else:
    # Fallback to dark theme if image not found
    st.markdown("<style>.stApp { background-color: #000000; }</style>", unsafe_allow_html=True)

# Rest of your standard CSS 
st.markdown("""
<style>
    /* Main Title */
    h1 {
        color: #e50914 !important;
        text-align: center;
        text-shadow: 0px 5px 15px rgba(229, 9, 20, 0.6);
        font-size: 3.2rem !important;
        font-weight: 900 !important;
    }

    /* Subtitle */
    p {
        color: #b3b3b3 !important;
        text-align: center;
        font-size: 1.2rem !important;
        letter-spacing: 1px;
    }

    /* Search Bar Label */
    div[data-testid="stSelectbox"] label p, div[data-testid="stTextInput"] label p {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.4);
        text-align: left;
    }

    /* URNE WALA SEARCH BAR EFFECT */
    div[data-testid="stSelectbox"], div[data-testid="stTextInput"] {
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        padding: 5px;
    }
    div[data-testid="stSelectbox"]:hover, div[data-testid="stTextInput"]:hover {
        transform: translateY(-8px) scale(1.01); 
        box-shadow: 0 15px 30px rgba(229, 9, 20, 0.3); 
        border-radius: 10px;
    }

    @keyframes pulse-border {
        0% { border-color: #b20710; box-shadow: 0 0 5px #b20710; }
        50% { border-color: #e50914; box-shadow: 0 0 15px #e50914, 0 0 25px #e50914; }
        100% { border-color: #b20710; box-shadow: 0 0 5px #b20710; }
    }

    .movie-title { 
        color: #ffffff !important; 
        font-weight: bold; 
        font-size: 16px; 
        text-align: center; 
        height: 40px; 
        text-shadow: 0px 0px 10px #e50914; 
        margin-bottom: 0px;
    }

    /* --- NEW: Movie Rating & Year CSS --- */
    .movie-info {
        color: #f5c518 !important; /* IMDb Yellow */
        font-size: 13px !important;
        font-weight: bold;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }

    div[data-testid="stImage"] img {
        border-radius: 10px; 
        border: 2px solid #b20710;
        animation: pulse-border 2s infinite; 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
        cursor: pointer;
    }

    div[data-testid="stImage"] img:hover {
        transform: translateY(-15px) scale(1.08); 
        border: 2px solid #ffffff;
        box-shadow: 0 20px 40px rgba(229, 9, 20, 0.9), 0 0 20px rgba(255, 255, 255, 0.6);
        animation: none; 
        z-index: 10;
    }

    /* Netflix Style Generate Button */
    div.stButton > button:first-child {
        background-color: #e50914;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #b20710;
        transform: translateY(-3px) scale(1.02); 
        box-shadow: 0 10px 20px rgba(229, 9, 20, 0.7);
        color: white;
    }

    /* Trailer Button CSS */
    .trailer-btn {
        display: block;
        text-align: center;
        background-color: rgba(0, 0, 0, 0.6);
        color: white !important;
        border: 1px solid #e50914;
        padding: 8px;
        margin-top: 15px;
        border-radius: 5px;
        text-decoration: none;
        font-size: 14px;
        font-weight: bold;
        transition: 0.3s;
    }
    .trailer-btn:hover {
        background-color: #e50914;
        color: white !important;
        text-decoration: none;
        transform: scale(1.05);
        box-shadow: 0 0 15px #e50914;
    }

    /* Sentiment Badge CSS */
    .sentiment-badge {
        text-align: center;
        color: #00ff88;
        font-size: 13px;
        font-weight: bold;
        margin-top: 10px;
        background-color: rgba(0,255,136, 0.1);
        padding: 5px;
        border-radius: 5px;
        border: 1px solid rgba(0,255,136, 0.3);
    }
    
    /* Fix for Expander text color */
    .streamlit-expanderContent p { color: #ffffff !important; font-size: 13px; }

    /* ========================================== */
    /* 🔥 NEW: CSS FOR RADIO TABS (MOVIES VS WEB SERIES) */
    /* ========================================== */
    div.stRadio > div[role="radiogroup"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    
    /* 🔥 HOVER WALA URNE KA EFFECT AB INDIVIDUAL BOXES PAR LAGAYA HAI */
    div.stRadio > div[role="radiogroup"] > label {
        background-color: rgba(20, 20, 20, 0.9) !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        border: 1px solid #e50914 !important;
        box-shadow: 0 0 10px rgba(229, 9, 20, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; 
        color: white !important;
        font-weight: bold !important;
        cursor: pointer !important;
        margin-right: 15px !important;
    }
    
    div.stRadio > div[role="radiogroup"] > label:hover {
        transform: translateY(-8px) scale(1.05) !important; 
        box-shadow: 0 15px 30px rgba(229, 9, 20, 0.7) !important; 
        border-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🚀 NEW: SIDEBAR SMART FILTERS
# ==========================================
# NEW: 100% Unblockable CSS Text Logo
st.sidebar.markdown("""
<div style="margin-bottom: 20px;">
    <h1 style="color: #e50914; font-family: 'Arial Black', sans-serif; font-size: 42px; font-weight: 900; letter-spacing: -3px; margin: 0; text-shadow: 0px 0px 15px rgba(229, 9, 20, 0.6);">
        NETFLIX
    </h1>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='color: #e50914;'>🔍 Smart Filters</h2>", unsafe_allow_html=True)

# Sidebar Radio Button for Category
filter_type = st.sidebar.radio("Category:", ["🎬 Movies", "📺 Web Series"], horizontal=True)

media_val = "movie" if "Movies" in filter_type else "tv"

# 🔥 FIX: Sidebar Genre Logic Update
if media_val == "movie":
    genre_dict = {"Action": 28, "Comedy": 35, "Sci-Fi": 878, "Horror": 27, "Romance": 10749, "Animation": 16}
else:
    genre_dict = {"Action": 10759, "Comedy": 35, "Sci-Fi": 10765, "Horror": 9648, "Romance": 10749, "Animation": 16}

selected_genre = st.sidebar.selectbox("Select Genre", list(genre_dict.keys()))
selected_year = st.sidebar.slider("Release Year After", 1990, 2024, 2020)

if st.sidebar.button("Discover Movies 🚀"):
    st.title(f"🍿 Top {selected_genre} {filter_type.split()[1]} after {selected_year}")
    api_key = "API_KEY" # <--- 4. APNI API KEY YAHAN BHI DALO 
    
    date_param = "primary_release_date.gte" if media_val == "movie" else "first_air_date.gte"
    
    discover_url = f"https://api.themoviedb.org/3/discover/{media_val}?api_key={api_key}&with_genres={genre_dict[selected_genre]}&{date_param}={selected_year}-01-01&sort_by=popularity.desc"
    
    try:
        disc_res = requests.get(discover_url).json()
        disc_movies = disc_res.get('results', [])[:5]
        
        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i < len(disc_movies):
                with col:
                    m_id = disc_movies[i]['id']
                    # TV shows have 'name', Movies have 'title'
                    m_title = disc_movies[i].get('title', disc_movies[i].get('name'))
                    
                    poster_url, rating, year, overview, cast = fetch_details(m_id, media_val)
                    trailer_url = fetch_trailer(m_id, media_val)
                    
                    st.markdown(f'<p class="movie-title">{m_title}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="movie-info">⭐ {rating}/10 | 📅 {year}</p>', unsafe_allow_html=True)
                    st.image(poster_url)
                    st.markdown(f'<a href="{trailer_url}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>', unsafe_allow_html=True)
                    with st.expander("📝 Story & Cast"):
                        st.markdown(f"**🎭 Cast:** {cast}")
                        st.caption(f"{overview[:120]}...")
    except:
        st.error("Network issue. Please check API Key.")
    
    st.markdown("---")


# ==========================================
# 🎬 MAIN APP (DOUBLE BRAIN AI RECOMMENDATION)
# ==========================================
st.title('🎬 AI Recommendation System')
st.markdown("<p>Find your next favorite Movie or Web Series.</p>", unsafe_allow_html=True)

# 🚀 TABS UPDATED: Ab dono AI Recommended hain
search_mode = st.radio("What do you want to search?", ["🎬 Movies (AI Recommended)", "📺 Web Series (AI Recommended)"], horizontal=True)

if "Movies" in search_mode:
    # --- BRAIN 1: MOVIES ---
    movies = joblib.load('movie_list.pkl')
    similarity = joblib.load('similarity.pkl')

    selected_movie = st.selectbox(
        'Type or select a movie you liked:',
        movies['title'].values
    )

    if st.button('GENERATE RECOMMENDATIONS'):
        movie_index = movies[movies['title'] == selected_movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                m_title = movies.iloc[movies_list[i][0]].title
                m_id = movies.iloc[movies_list[i][0]].movie_id
                
                poster_url, rating, year, overview, cast = fetch_details(m_id, "movie") 
                trailer_url = fetch_trailer(m_id, "movie")
                sentiment_score = analyze_sentiment(m_id, "movie")
                
                st.markdown(f'<p class="movie-title">{m_title}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="movie-info">⭐ {rating}/10 | 📅 {year}</p>', unsafe_allow_html=True)
                st.image(poster_url)
                st.markdown(f'<div class="sentiment-badge">{sentiment_score}</div>', unsafe_allow_html=True)
                st.markdown(f'<a href="{trailer_url}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>', unsafe_allow_html=True)
                with st.expander("📝 Story & Cast"):
                    st.markdown(f"**🎭 Cast:** {cast}")
                    st.caption(f"{overview[:120]}...") 

else:
    # --- BRAIN 2: TV SHOWS (NEW ML LOGIC) ---
    tv_dict = joblib.load('tv_list.pkl')
    tv_shows = pd.DataFrame(tv_dict)
    tv_similarity = joblib.load('tv_similarity.pkl')

    selected_tv = st.selectbox('Type or select a Web Series you liked:', tv_shows['name'].values)
    
    if st.button('GENERATE RECOMMENDATIONS'):
        tv_index = tv_shows[tv_shows['name'] == selected_tv].index[0]
        distances = tv_similarity[tv_index]
        tv_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                t_title = tv_shows.iloc[tv_list[i][0]]['name']
                t_id = tv_shows.iloc[tv_list[i][0]]['id']
                
                poster_url, rating, year, overview, cast = fetch_details(t_id, "tv") 
                trailer_url = fetch_trailer(t_id, "tv")
                sentiment_score = analyze_sentiment(t_id, "tv")
                
                st.markdown(f'<p class="movie-title">{t_title}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="movie-info">⭐ {rating}/10 | 📅 {year}</p>', unsafe_allow_html=True)
                st.image(poster_url)
                st.markdown(f'<div class="sentiment-badge">{sentiment_score}</div>', unsafe_allow_html=True)
                st.markdown(f'<a href="{trailer_url}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>', unsafe_allow_html=True)
                with st.expander("📝 Story & Cast"):
                    st.markdown(f"**🎭 Cast:** {cast}")
                    st.caption(f"{overview[:120]}...")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Built with ❤️ by Muhammad Bin Nadeem | BSAI Student</p>", unsafe_allow_html=True)
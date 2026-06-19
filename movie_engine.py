import pandas as pd
import ast
import nltk
from nltk.stem.porter import PorterStemmer # Naya Add kiya
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Stemmer initialize kar rahe hain
ps = PorterStemmer()

# Helper function words ko stem karne ke liye (e.g. loved -> love)
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

# 1. Load the real datasets (Make sure files are in the same folder!)
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# 2. Merge on title
movies = movies.merge(credits, on='title')

# 3. Select important columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

# --- CLEANING FUNCTIONS ---
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name']) 
    return L

def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter < 3:
            L.append(i['name'])
            counter += 1
    return L

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

# Applying functions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)

# Overview ko list mein badalna taake tags mein merge ho sakay
movies['overview'] = movies['overview'].apply(lambda x:x.split())

# Spaces khatam karna
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

# 4. 🔥 CREATING THE "TAGS" COLUMN
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Wapas String mein convert karna
new_df = movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

# 🔥 STEMMING APPLY KAR RAHE HAIN (Words ko root form mein lana)
new_df['tags'] = new_df['tags'].apply(stem)

print("✅ Step 1: Data Cleaning & Stemming Complete!")
print(new_df.head())

# --- STEP 2: VECTORIZATION & SIMILARITY ---

# 1. Text ko Vectors mein badalna (5000 movies, 5000 words)
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# 2. Similarity Matrix banana (Har movie ka har movie ke sath muqabla)
similarity = cosine_similarity(vectors)

# 3. 🎬 THE RECOMMENDATION FUNCTION
def recommend(movie):
    try:
        # Movie ka index nikalna
        movie_index = new_df[new_df['title'] == movie].index[0]
        # Similarity score nikal kar sort karna (Top 5)
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        print(f"\n🍿 If you liked '{movie}', you should watch:")
        for i in movies_list:
            print(f"- {new_df.iloc[i[0]].title}")
    except:
        print("\n❌ Movie not found in database! Check spelling.")

# --- TEST KARO ---
recommend('Avatar')
recommend('The Dark Knight Rises')

# --- STEP 3: SAVING THE BRAIN ---
print("\n💾 Saving the model...")
joblib.dump(new_df, 'movie_list.pkl')
joblib.dump(similarity, 'similarity.pkl')
print("✅ Everything Saved!")
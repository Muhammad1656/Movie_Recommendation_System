import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import pickle

print("🚀 TV Engine Started: Loading Dataset...")
# 1. Load Dataset (YAHAN APNI CSV FILE KA ASLI NAAM DALNA)
tv = pd.read_csv('TMDB_tv_dataset_v3.csv') 

# 🔥 THE MEMORY FIX: Prevent 30GB RAM Explosion!
print(f"📊 Total shows found: {tv.shape[0]}. Cutting down to top 5000 for PC safety...")
if 'popularity' in tv.columns:
    tv = tv.sort_values(by='popularity', ascending=False).head(5000)
elif 'vote_count' in tv.columns:
    tv = tv.sort_values(by='vote_count', ascending=False).head(5000)
else:
    tv = tv.head(5000)

# 2. Keep Only Required Columns
tv = tv[['id', 'name', 'overview', 'genres']] 

# Drop missing values
tv.dropna(inplace=True)

print("🧹 Cleaning Data & Building Tags...")

def convert_genres(text):
    L = []
    try:
        for i in ast.literal_eval(text):
            L.append(i['name'])
        return L
    except:
        return str(text).split(',')

tv['genres'] = tv['genres'].apply(convert_genres)
tv['overview'] = tv['overview'].apply(lambda x: str(x).split())
tv['genres'] = tv['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
tv['tags'] = tv['overview'] + tv['genres']

# 🔥 WARNING FIX: Added .copy() to stop pandas from crying
new_df = tv[['id', 'name', 'tags']].copy()
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

print("🧠 Training the Machine Learning Model...")

ps = PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

print("⚙️ Calculating Cosine Similarity (Almost Done)...")
similarity = cosine_similarity(vectors)

print("💾 Saving the New Brain to .pkl files...")

pickle.dump(new_df.to_dict(), open('tv_list.pkl', 'wb'))
pickle.dump(similarity, open('tv_similarity.pkl', 'wb'))

print("✅ Success! 'tv_list.pkl' and 'tv_similarity.pkl' are ready!")
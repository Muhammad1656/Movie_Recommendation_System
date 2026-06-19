# 🎬 AI Movie Recommendation Engine

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg)
![TMDB API](https://img.shields.io/badge/API-TMDB-green.svg)

An advanced, Machine Learning-powered web application that recommends movies based on user preferences. By leveraging content-based filtering algorithms and the TMDB API, this system not only suggests highly accurate movie matches but also fetches real-time official movie posters to create a premium, Netflix-like user experience.

---

## ✨ VIP Features
* **🧠 Smart AI Engine:** Uses mathematical vectorization (Cosine Similarity) to analyze movie metadata (genres, cast, crew, keywords) and find the perfect match.
* **🌍 Real-Time API Integration:** Connected directly to the TMDB (The Movie Database) API to fetch high-quality, up-to-date movie posters.
* **💻 Sleek Dashboard UI:** Built entirely on Streamlit with a highly interactive, responsive, and aesthetically pleasing dark-mode interface.
* **⚡ Lightning Fast:** Optimized matrix calculations ensure that recommendations and image fetching happen in milliseconds.

---

## 🛠️ Tech Stack & Architecture
| Component | Technology Used |
| :--- | :--- |
| **Programming Language** | Python |
| **Frontend UI** | Streamlit |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy |
| **Data Source** | TMDB 5000 Movies Dataset (Kaggle) |
| **Live API** | TMDB (The Movie Database) API |

---

## 🚀 How to Run Locally

Follow these steps to deploy the AI engine on your local machine:

**1. Clone the Repository**
```bash
git clone [https://github.com/Muhammad1656/Movie_Recommendation_System](https://github.com/Muhammad1656/Movie_Recommendation_System.git)
cd Movie_Recommendation_System

2. Install Dependencies
Ensure you have Python installed, then run:

Bash
pip install -r requirements.txt

3. TMDB API Key Setup

Create an account on TMDB.

Generate your free API key from the settings menu.

Open app.py and replace the placeholder API key with your actual key.

4. Launch the App
Fire up the Streamlit server:

Bash
streamlit run app.py
💡 How It Works (Under the Hood)
Data Preprocessing: The engine cleans and merges datasets, combining overviews, genres, cast, and directors into a single "tags" column.

Text Vectorization: Natural Language Processing (NLP) converts these text tags into mathematical vectors.

Distance Calculation: The AI calculates the cosine distance between the user's selected movie vector and all other movie vectors in the database.

Output: The top 5 closest vectors are identified, their IDs are sent to the TMDB API, and the results are rendered on the screen.

👨‍💻 Developer
Muhammad Bin Nadeem BSAI Data Science & ML Developer Passionate about building hybrid AI systems, deploying scalable ML models, and pushing the boundaries of artificial intelligence.

If you like this project, don't forget to star ⭐ the repository!

"""
TrendPredict – Twitter/X Topic Modeling (TF-IDF)
Author: Chaimaa Nairi
Description:
Extracts dominant discussion keywords from Twitter/X tweets
using TF-IDF to explain WHY trends are emerging.
Outputs topic keywords per hashtag for Tableau storytelling.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# -------------------------
# Configuration
# -------------------------
CSV_INPUT = "../data/twitter_trends.csv"
CSV_OUTPUT = "../data/twitter_trends_topics.csv"

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(CSV_INPUT)

# -------------------------
# Keyword extraction function
# -------------------------
def extract_keywords(texts, top_n=3):
    if len(texts) == 0:
        return ""

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=1000
    )

    X = vectorizer.fit_transform(texts)
    words = vectorizer.get_feature_names_out()
    scores = X.mean(axis=0).A1

    top_words = sorted(
        zip(words, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ", ".join([w for w, _ in top_words[:top_n]])

# -------------------------
# Extract topics per hashtag
# -------------------------
topics = []

for hashtag, group in df.groupby("hashtag"):
    keywords = extract_keywords(group["text"].astype(str))
    topics.append({
        "hashtag": hashtag,
        "topic_keywords": keywords
    })

topics_df = pd.DataFrame(topics)

# -------------------------
# Merge back into main df
# -------------------------
df = df.merge(topics_df, on="hashtag", how="left")

# -------------------------
# Save output
# -------------------------
df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
print(f"✅ Topic-enhanced CSV saved → {CSV_OUTPUT} ({len(df)} rows)")

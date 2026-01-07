import pandas as pd

data = {
    "created_at": pd.date_range(start="2025-01-01", periods=10, freq="H"),
    "text": ["Sample tweet"] * 10,
    "sentiment": [0.2, -0.1, 0.5, 0.3, -0.4, 0.1, 0.6, -0.2, 0.4, 0.0],
    "likes": [5, 10, 3, 8, 1, 4, 12, 6, 9, 2],
    "retweets": [1, 3, 0, 2, 0, 1, 4, 1, 2, 0]
}

df = pd.DataFrame(data)
df.to_csv("../data/twitter_trends.csv", index=False)

print("✅ Sample data created")

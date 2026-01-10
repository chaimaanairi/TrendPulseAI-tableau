# TrendPulse AI – Real-Time Social Media Trend Intelligence

AI-powered Tableau dashboard for tracking sentiment, momentum, and actionable insights from trending topics on Twitter/X.

**TrendPulse AI** transforms Twitter/X trends into actionable, explainable insights by combining NLP, predictive analytics, and AI-driven recommendations. Designed for marketers, analysts, and decision-makers, it answers:

- **What’s trending?**  
- **Why?**  
- **What should I do next?**  

All in near real-time.

## Key Capabilities

- **Dual Sentiment Analysis**: Uses TextBlob and VADER for nuanced sentiment scoring and cross-validation.
- **Trend Momentum Scoring**: Custom algorithm combining engagement (likes + retweets) and sentiment weighting to classify trends: **Stable**, **Emerging**, **Exploding**.
- **Trending Topics Analysis (Explainability Layer)**: Uses TF-IDF to surface top keywords, explaining why trends emerge.
- **AI-Powered Recommendations**: Converts analytics into actionable decisions:  
  🔥 Launch campaign now | 🚀 Monitor trend closely | ⚠️ Investigate reputation risk | ⏳ No action needed
- **Simulated Near-Real-Time Streaming**: Micro-batch updates for fresh insights without heavy streaming infrastructure.
- **Hyper API (Optional)**: Enables external systems to query trends, momentum, sentiment, and AI recommendations.

## Project Structure
- `data/`: Raw and processed data files
- `scripts/`: Python scripts for data ingestion, analysis, NLP, and AI recommendations
- `tableau/`: Tableau workbook for visualization
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not included for security)
- `.gitignore`: Files to ignore in Git


## Installation & Setup

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Set Twitter/X API token**:
```bash
export BEARER_TOKEN="YOUR_TWITTER_API_BEARER_TOKEN"
```
3. **Run Data Pipeline**:
```bash
python scripts/fetch_twitter_data.py
python scripts/json_to_csv.py
python scripts/feature_engineering.py
python scripts/nlp_vader.py
python scripts/nlp_topics.py
python scripts/ai_recommendations.py
python scripts/micro_batch_streaming.py

```
4. **Start Hyper API (Optional)**:
```bash
uvicorn hyper_api:app --reload
```

## Tableau Dashboard Overview

Open `tableau/TrendPulse.twbx` in Tableau Cloud to explore interactive, storytelling dashboards with deep insights.
**Note:** Every visualization includes rich **hover tooltips** that provide deeper context.

### Hover Tooltips Include:
- Exact sentiment scores (TextBlob & VADER)  
- Engagement metrics (likes, retweets, momentum)  
- Top keywords driving trends  
- AI-generated recommendations  
- Timestamp and hashtag context  

### Tableau Sheets Description

**KPI – Trend Momentum**  
- Shows momentum scores and trend status per hashtag  
- Displays average VADER sentiment  
- Highlights AI recommendations count  
- Hover reveals sentiment breakdown & engagement metrics  

**TextBlob & VADER Sentiment Sheets**  
- Line/bar charts of sentiment over time  
- Color-coded: Positive / Neutral / Negative  
- Hover shows exact scores & tweet volumes  

**Trending Topics – Behind the Trend**  
- Table of top 3 keywords per hashtag (TF-IDF)  
- Explains why trends are emerging  

**AI Recommendations**  
- 🔥 Launch campaign now  
- 🚀 Monitor closely  
- ⚠️ Investigate reputation risk  
- ⏳ No action needed  
- Shows which hashtags require action  

**Engagement Over Time**  
- Line chart tracking engagement (likes + retweets) per hashtag  

**Top Tweets by Engagement**  
- Table of most engaging tweets  
- Includes text, sentiment, and momentum  

**Trend Forecast**  
- Projected momentum & engagement trends  
- Helps predict potential viral hashtags  

**Actionable Insights**  
- Dashboard cards summarizing key insights  
- Combines momentum, sentiment, trending topics, and AI recommendations  

**Map Visualization**  
- Displays tweets by user location (Asia, Europe, USA)  
- Highlights regional engagement patterns  

**Storytelling Dashboard**  
- Combines all sheets into a single interactive story layout  
- Explore:  
  - Momentum vs Sentiment vs Topics  
  - AI Recommendations & Actionable Insights  
  - Regional Trends on the Map  

**Impact:**  
Provides a holistic view of trending hashtags, sentiment, momentum, and AI-driven recommendations, enabling marketers to make informed decisions in near real-time.


# TrendPulse AI – Real-Time Social Media Trend Intelligence

**AI-powered Tableau dashboard for tracking sentiment, momentum, and actionable insights from trending topics on Twitter/X**

**TrendPulse AI** transforms Twitter/X trends into actionable insights by combining **NLP, predictive analytics, and AI-driven recommendations**. It’s designed to help businesses, marketers, and analysts understand **what’s trending, why, and what actions to take** — all in near real-time. 

**Key Capabilities:**

- **Dual Sentiment Analysis:** Uses **TextBlob** and **VADER** to assess sentiment and validate results for higher analytical confidence.
- **Trend Momentum Scoring:** Custom scoring algorithm combines engagement (likes + retweets) and sentiment weighting to classify trends: **Stable, Emerging, Exploding.**  
- **Trending Topics Analysis (Explainability Layer):** Extracts top discussion keywords per hashtag using **TF-IDF** to explain *why trends are emerging*.
- **AI-Powered Recommendations:** Converts analytics into actionable decisions: **Launch campaign now**, **Monitor trend closely**, **Investigate reputation risk**, **No action needed**.
- **Simulated Near-Real-Time Streaming:** Micro-batch updates to reflect fresh data without heavy streaming infrastructure.
- **Hyper API:** Exposes trend metrics and AI recommendations for integration into dashboards or apps.

## Project Structure
- `data/`: Raw and processed data files
- `scripts/`: Python scripts for data processing and analysis
- `tableau/`: Tableau workbook for visualization
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not included for security)
- `.gitignore`: Git ignore file


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
Open `tableau/TrendPulse.twbx` in Tableau to visualize the processed data.

**Note:** Every visualization includes rich **hover tooltips** that provide deeper context without cluttering the dashboard.
On hover, users can view:
- Exact sentiment scores (TextBlob & VADER)
- Engagement metrics (likes, retweets, momentum)
- Top keywords driving each trend
- AI-generated recommendations
- Timestamp and hashtag context

### Tableau Sheets Description
**KPI - Trend Momentum**
- Shows overall momentum scores and statuses per hashtag  
- Displays **average VADER sentiment**  
- Highlights **AI recommendations count**  
- Hover reveals **sentiment breakdown and engagement metrics**

**TextBlob Sentiment Sheet**
- Line/bar charts showing sentiment over time using **TextBlob**  
- Color-coded for **Positive / Neutral / Negative** sentiment  
- Hover displays **exact sentiment score and tweet volume**

**VADER Sentiment Sheet**
- Line/bar charts showing sentiment over time using **VADER**  
- Color-coded for **Positive / Neutral / Negative** sentiment  

**Trending Topics Behind the Trend**
- Table showing **top 3 keywords per hashtag** via **TF-IDF**  
- Explains **why trends are emerging**  

**AI Recommendations**
- Color-coded recommendations:  
  - 🔥 **Launch marketing campaign now**  
  - 🚀 **Monitor closely – trend emerging**  
  - ⚠️ **Reputation risk – investigate**  
  - ⏳ **No action needed**  
- Shows which **hashtags require action**  

**Engagement Over Time**
- Line chart tracking **engagement (likes + retweets) per hashtag**  

**Top Tweets by Engagement**
- Table showing **tweets with highest engagement metrics**  
- Includes **text, sentiment, and momentum**  

**Trend Forecast**
- Projected **momentum and engagement trends**  
- Helps predict **potential viral hashtags**  

**Actionable Insights**
- Dashboard cards summarizing **key insights**  
- Combines **momentum, sentiment, trending topics, and AI recommendations**  

**Map Visualization**
- Shows tweets by **user location**  
- Highlights **regional engagement patterns**  

**Dashboard (Storytelling Layout)**
- Combines all sheets into an **interactive storytelling dashboard**  
- Allows exploration of:  
  - Momentum vs Sentiment vs Topics  
  - AI Recommendations and Actionable Insights  
  - Regional Trends on the Map  

This dashboard provides a **holistic view of trending hashtags**, combining sentiment analysis, momentum tracking, AI insights, and regional patterns to guide marketing or strategic decisions.




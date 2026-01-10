# TrendPredict – Twitter/X Trend Prediction & AI Recommendations

**TrendPredict** collects, processes, and visualizes Twitter/X trends in **near-real-time**.  
It combines **feature engineering, NLP, topic modeling, and AI-powered recommendations** to provide actionable insights for decision-makers.  

Key capabilities:

- **Sentiment Analysis**: TextBlob + VADER comparison for richer insights  
- **Trend Momentum**: Calculates momentum score and status for hashtags  
- **Topic Modeling**: Extracts top discussion keywords using TF-IDF  
- **AI Recommendations**: Suggests next actions based on momentum and sentiment  
- **Simulated Streaming**: Micro-batch updates to simulate near-real-time data  
- **Optional API**: Hyper API to query trends externally  


## Project Structure
- `data/`: Raw and processed data files
- `scripts/`: Python scripts for data processing and analysis
- `tableau/`: Tableau workbook for visualization
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation
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
3. **Run scripts in order**:
```bash
python scripts/fetch_twitter_data.py
python scripts/json_to_csv.py
python scripts/feature_engineering.py
python scripts/nlp_vader.py
python scripts/nlp_topics.py
python scripts/ai_recommendations.py
python scripts/micro_batch_streaming.py

```
4. **Start Hyper API**:
```bash
uvicorn hyper_api:app --reload
```

## Tableau Dashboard Overview
Open `tableau/TrendPredict.twbx` in Tableau to visualize the processed data.

**KPI - Trend Momentum**
- Shows overall momentum scores and statuses per hashtag  
- Displays **average VADER sentiment**  
- Highlights **AI recommendations count**  

**TextBlob Sentiment Sheet**
- Line/bar charts showing sentiment over time using **TextBlob**  
- Color-coded for **Positive / Neutral / Negative** sentiment  

**VADER Sentiment Sheet**
- Line/bar charts showing sentiment over time using **VADER**  
- Color-coded for **Positive / Neutral / Negative** sentiment  
- Comparison with TextBlob using **dual-axis charts**  

**Trending Topics Behind the Trend**
- Bar chart / table showing **top 3 keywords per hashtag** via **TF-IDF**  
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
- Helps judges see **trend spikes**  

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


## Outcome

**TrendPredict** allows judges and stakeholders to:

- Quickly assess **trending topics and sentiment**
- Compare **NLP models side-by-side** (TextBlob vs VADER)
- Understand **why trends are happening** via topic keywords
- See **AI-powered recommendations** for next actions
- Explore **regional trends** via map visualization
- Follow **near-real-time updates** using micro-batch streaming

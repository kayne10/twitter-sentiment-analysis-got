# twitter-sentiment-analysis-got
Data Streaming Pipeline on GoT tweets for Series Finale

This small project was meant to run sentiment analysis on Tweets just a week after the season finale of Game of Thrones.
There was a lot of negative feedback and so I wanted to stream a small percentage of tweets for just 15 minutes. Then
I took that dataset, cleaned it, and ran some very basic sentiment analysis.

### Setup

Pre-requisites
- Postgres installed and running in your env
- Python3
- Twitter Api Keys (available on Twitter's developer portal)

Create a virtual environment
```
python -m venv venv
pip install -r requirements.txt
```

Export Twitter keys and Postgres password as environment variables
```
export CONSUMER_KEY=<consumer_key>
export CONSUMER_SECRET=<secret_key>
export ACCESS_TOKEN=<access_token>
export ACCESS_TOKEN_SECRET=<access_token_secret>
export password=<postgres_password>
```

## Run scripts

The clean data is already available in the `data/` directory from when I streamed the tweets just a week after the season finale. If you were to run this now, the results would be substantially different since the series ended on May 19, 2019.

However, you can change the trace keywords to whatever you desire.

Once that has been decided, run the streaming script that ingests each tweet into your local Postgres database.
```python
python StreamSQL.py
```

To see the results of the sentiment analysis run
```python
python exploration.py
```

Then feel free to add any Data Visualizations you desire with the transformed data.

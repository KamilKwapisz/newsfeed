import requests
import json
from decouple import config

# News from TechCrunch... powered by NewsAPI


def techcrunch_scraper() -> list:

    url: str = "https://newsapi.org/v2/everything?language=en&sources=techcrunch&apiKey={}"\
        .format(config('NEWSAPI_KEY'))  # techcrunch

    # GET method request to API url
    r = requests.get(url, headers={'User-agent': 'NewsScraper'})

    # loading data in json format
    data: list = json.loads(r.content)['articles']

    for row in data:
        # changing names of keys
        row['selftext'] = row.pop('description')
        row['created'] = row.pop('publishedAt')[:10]
        row['origin_logo'] = "img/techcrunch.png"

    return data

import requests
import json
from typing import Dict
import datetime


def check_subreddits(subreddits: list) -> list:
    """

    :param subreddits: list of subreddits which user wants to subscribe
    :return: list of subreddits which user wants to subscribe and they exist
    """
    subreddits_exist = []
    for subreddit_name in subreddits:
        url: str = "http://www.reddit.com/r/{}/new.json?sort=new".format(subreddit_name)
        r = requests.get(url, headers={'User-agent': 'Scrapper'})
        if r.status_code == 200:
            data = json.loads(r.content)
            if data['data']['after']:
                subreddits_exist.append(subreddit_name)
        else:
            pass

    return subreddits_exist


def reddit_scraper(subreddits: list, posts_limit: int) -> list:
    interesting_stuff: list = ['title', 'selftext', 'score', 'num_comments', 'url', 'author', 'is_video', 'created']
    articles = []
    data = Dict[str, str]  # create a dict for collected data

    for subreddit_name in subreddits:
        url: str = "http://www.reddit.com/r/{}/new.json?sort=new&limit={}".format(subreddit_name, posts_limit)

        r = requests.get(url, headers={'User-agent': 'Scraper'})

        if r.status_code == 200:
            data = json.loads(r.content)  # load json data to a python dict
            # parsing data Dict into a list with more relevant info
            data: list = data['data']['children']
            for i in range(len(data)):
                data[i] = data[i]['data']

        elif r.status_code == 429:  # if code == 429 change scraper's name and then load data
            r = requests.get(url, headers={'User-agent': 'Scraper{}'.format(str(datetime.date.today()))})
            if r.status_code == 200:
                data = json.loads(r.content)
                data: list = data['data']['children']  # parsing data Dict into a list with more relevant info
                for i in range(len(data)):
                    data[i] = data[i]['data']

        elif str(r.status_code)[0] == '5':
            print("Reddit server is not responding!")

        else:
            print("Something went wrong")

        articles += data  # add articles from each subreddit to single list.

    for i in range(len(articles)):  # create list of new dicts with only specific keys
        articles[i] = dict((key, value) for key, value in articles[i].items() if key in interesting_stuff)
        articles[i]['photo'] = "img/reddit.jpg"
        articles[i]['origin'] = "reddit"
        articles[i]['origin_logo'] = "img/reddit.png"
        create_timestamp = int(articles[i]['created'])
        articles[i]['created'] = str(datetime.datetime.fromtimestamp(create_timestamp).strftime('%Y-%m-%d'))
    return articles


def main():
    articles = reddit_scraper(['python', 'movies'], 10)
    print(articles)



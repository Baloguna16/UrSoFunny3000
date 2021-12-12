import os
import tweepy

from .api import RobotStream
from .api.graph import WordGraph
from .api.const import TWITTER_BOT_HANDLE
from .api.scrapers import get_press_releases
from .api.markov import create_training_set, generate_tweet
from .api.markov import build_word_graph, build_two_word_graph

class Bot:

    _instance = None

    def __init__(self):
        if Bot._instance is None:
            self.CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
            self.CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")

            self.ACCESS_KEY = os.getenv("TWITTER_ACCESS_KEY")
            self.ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

            self.BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

            self._auth = tweepy.OAuthHandler(
                consumer_key=self.CONSUMER_KEY,
                consumer_secret=self.CONSUMER_SECRET
            )
            self._auth.set_access_token(
                key=self.ACCESS_KEY,
                secret=self.ACCESS_SECRET
            )

            self.client = tweepy.Client(
                bearer_token=self.BEARER_TOKEN,
                consumer_key=self.CONSUMER_KEY,
                consumer_secret=self.CONSUMER_SECRET,
                access_token=self.ACCESS_KEY,
                access_token_secret=self.ACCESS_SECRET,
                wait_on_rate_limit=True
            )

            self.word_graph = None

            Bot._instance = self
            return
        raise Exception("UrSoFunny3000 should only be created once.")


    @staticmethod
    def get_instance():
        if Bot._instance is None:
            Bot()
        return Bot._instance

    def ama(self):
        response = self.client.get_user(username=TWITTER_BOT_HANDLE)
        user = response.data

        response = self.client.get_users_followers(id=user['id'])
        followers = response.data

        robot_stream = RobotStream(
            consumer_key=self.CONSUMER_KEY,
            consumer_secret=self.CONSUMER_SECRET,
            access_token=self.ACCESS_KEY,
            access_token_secret=self.ACCESS_SECRET,
            current_client=self.client,
            daemon=True
        )

        robot_stream.filter(
            follow=[user['id'] for user in followers],
            languages=['en']
        )

    def scrape_twitter(self, target):
        response = self.client.get_user(username=target)
        user = response.data

        response = self.client.get_users_tweets(id=user['id'], max_results=100)
        tweets = response.data

        dir = 'data'
        for tweet in tweets:
            filename = f'{target}_{tweet["id"]}.txt'
            file = os.path.join(dir, filename)
            file = open(file, 'w+')
            file.write(tweet["text"])
            file.close()

    def scrape_html(self):
        get_press_releases()

    def train(self):
        training_set = create_training_set(dir='data')
        word_graph = build_word_graph(training_set)
        word_graph = build_two_word_graph(training_set)
        self.word_graph = word_graph

    def sample(self):
        if self.word_graph is None:
            word_graph = WordGraph.load()

        else: word_graph = self.word_graph
        sample_tweet = generate_tweet(word_graph, prompt='i')
        
        print("Sample tweet: ", sample_tweet)


def create_bot():
    bot = Bot.get_instance()
    return bot

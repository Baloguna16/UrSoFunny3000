import os
import tweepy

from .api import RobotStream

class Bot:

    _instance = None

    def __init__(self):
        if Bot._instance is None:
            self.CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
            self.CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")

            self.ACCESS_KEY = os.getenv("TWITTER_ACCESS_KEY")
            self.ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

            self._auth = tweepy.OAuthHandler(
                consumer_key=self.CONSUMER_KEY,
                consumer_secret=self.CONSUMER_SECRET
            )
            self._auth.set_access_token(
                key=self.ACCESS_KEY,
                secret=self.ACCESS_SECRET
            )

            self.api = tweepy.API(
                auth=self._auth,
                wait_on_rate_limit=True
            )

            Bot._instance = self
            return
        raise Exception("UrSoFunny3000 should only be created once.")


    @staticmethod
    def get_instance():
        if Bot._instance is None:
            Bot()
        return Bot._instance

    def run(self):
        user_to_follow = self.api.get_user(screen_name='Ade_in_myLife')

        robot_stream = RobotStream(
            consumer_key=self.CONSUMER_KEY,
            consumer_secret=self.CONSUMER_SECRET,
            access_token=self.ACCESS_KEY,
            access_token_secret=self.ACCESS_SECRET
        )

        robot_stream.set_api(self.api)

        robot_stream.filter(
            follow=[user_to_follow.id],
            languages=['en']
        )

def create_bot():
    bot = Bot.get_instance()
    return bot

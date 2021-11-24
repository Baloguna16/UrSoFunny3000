from tweepy import Stream, OAuthHandler

from .api import RobotListener

class Bot:

    _instance = None

    def __init__(self):
        if Bot._instance is None:
            self.CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
            self.CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")

            self.ACCESS_KEY = os.getenv("TWITTER_ACCESS_KEY")
            self.ACCESS_SECRET = os.getenv("TWITTER_ACCESS_KEY")

            self._auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            self._auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

            self.api = tweepy.API(
                self._auth,
                wait_on_rate_limit=True,
                wait_on_rate_limit_notify=True
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
        robot_stream_listener = RobotListener()

        stream = tweepy.Stream(
            auth=self.api.auth,
            listener=robot_stream_listener
        )
        
        stream.retweet()

def create_bot():
    bot = Bot.get_instance()
    return bot

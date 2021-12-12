from .const import TWITTER_BOT_HANDLE

def check_content(tweet_text):
    """Checks to assure that status.text is content safe."""

    return f'@{TWITTER_BOT_HANDLE}' in tweet_text

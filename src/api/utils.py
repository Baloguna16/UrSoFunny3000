from .const import TWITTER_BOT_HANDLE

def check_content(tweet_text):
    """Checks to assure that status.text is content safe."""

    return f'@{TWITTER_BOT_HANDLE}' in tweet_text

def load_stored_response(tweet_text):
    """Building custom responses based on stored content."""

    response = "I like cheese."
    return response

import os
import logging
from tweepy import Stream

from .utils import check_content
from .utils import load_stored_response
from .openai import make_openai_request

class RobotStream(Stream):

    def __init__(
        self,
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
        *,
        chunk_size=512,
        daemon=False,
        max_retries=float('inf'),
        proxy=None,
        verify=True,
        current_client=None
    ):
        super().__init__(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            chunk_size=chunk_size,
            daemon=daemon,
            max_retries=max_retries,
            proxy=proxy,
            verify=verify
        )

        self.client = current_client


    def on_status(self, tweet):
        if check_content(tweet.text):

            #response = make_openai_request(status)
            response_text = load_stored_response(tweet.text)

            self.client.create_tweet(
                text=response_text,
                quote_tweet_id=tweet.id
            )

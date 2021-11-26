import os
import tweepy
import logging

from .utils import check_content
from .utils import load_stored_resposne
from .openai import make_openai_request

class RobotStream(tweepy.Stream):

    def on_status(self, status):
        assert check_content(status)

        #response = make_openai_request(status)
        response = load_stored_resposne(status)

        assert check_content(response)

        self.api.update_status(response)

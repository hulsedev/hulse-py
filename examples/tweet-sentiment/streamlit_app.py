import json
from bs4 import BeautifulSoup

import hulse
import requests
import streamlit as st
import streamlit.components.v1 as components


class Tweet(object):
    """Embed tweet in the streamlit app."""

    def __init__(self, s, embed_str=False):
        if not embed_str:
            api = "https://publish.twitter.com/oembed?url={}&theme=dark".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
            self.tweet_text = BeautifulSoup(self.text, "html.parser").get_text()
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=600, width=400)


if "client" not in st.session_state and "api_key" in st.session_state:
    st.session_state.client = hulse.Hulse()


st.title("Tweet Sentiment Analysis")
st.markdown("Analyse your tweets and get sentiment analysis.")

api_key = st.text_input(
    "Enter your API key:",
    help="You can get your API key from https://dashboard.hulse.app/.",
)
if not api_key:
    st.info("Please enter your API key.")
else:
    st.session_state.api_key = api_key
    tweet_url = st.text_input(
        "Enter a tweet url:", help="Enter a tweet url to be analysed."
    )
    if tweet_url and "client" in st.session_state and "api_key" in st.session_state:
        # load tweet data
        try:
            tweet_object = Tweet(tweet_url)
        except Exception as e:
            st.error(f"Impossible to load tweet. {e}")
            
        # query your hulse cluster
        try:
            sentiment = st.session_state.client.query(
                task="text-classification",
                data=tweet_object.tweet_text,
                api_key=st.session_state.api_key,
            )
            sentiment["result"] = json.loads(sentiment.get("result"))
        except Exception as e:
            st.error("Impossible to analyse tweet.")

        # present the loaded text
        st.header("Your tweet's text:")
        st.write(tweet_object.tweet_text)

        # display the result
        st.header("Sentiment results:")
        col1, col2, col3 = st.columns(3)
        col1.metric("Cluster", sentiment.get("cluster"))
        col2.metric("Sentiment", sentiment.get("result").get("label"))
        col3.metric("Score", "{:.3f}".format(sentiment.get("result").get("score")))

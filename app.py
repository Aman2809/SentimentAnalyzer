# import streamlit as st
# import pickle
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from nltk.corpus import stopwords
# import nltk
# from ntscraper import Nitter
# import time
# import requests
# from urllib3.util.retry import Retry
# from requests.adapters import HTTPAdapter
#
#
# # Download stopwords once, using Streamlit's caching
# @st.cache_resource
# def load_stopwords():
#     nltk.download('stopwords')
#     return stopwords.words('english')
#
#
# # Load model and vectorizer once
# @st.cache_resource
# def load_model_and_vectorizer():
#     with open('model.pkl', 'rb') as model_file:
#         model = pickle.load(model_file)
#     with open('vectorizer.pkl', 'rb') as vectorizer_file:
#         vectorizer = pickle.load(vectorizer_file)
#     return model, vectorizer
#
#
# # Create a robust session for HTTP requests
# def create_robust_session():
#     session = requests.Session()
#     retry_strategy = Retry(
#         total=3,
#         backoff_factor=1,
#         status_forcelist=[429, 500, 502, 503, 504],
#     )
#     adapter = HTTPAdapter(max_retries=retry_strategy)
#     session.mount("http://", adapter)
#     session.mount("https://", adapter)
#     return session
#
#
# # Initialize Nitter scraper with expanded instance list
# @st.cache_resource
# def initialize_scraper():
#     # Expanded list of Nitter instances
#     instances = [
#         "nitter.net",
#         "nitter.cz",
#         "nitter.it",
#         "nitter.pw",
#         "nitter.poast.org",
#         "nitter.privacydev.net",
#         "nitter.projectsegfau.lt",
#         "nitter.foss.wtf",
#         "nitter.1d4.us",
#         "nitter.kavin.rocks",
#         "nitter.unixfox.eu",
#         "nitter.mint.lgbt",
#         "nitter.esmailelbob.xyz",
#         "nitter.platypush.tech",
#         "nitter.nl",
#         "nitter.tux.pizza",
#         "nitter.riverside.rocks"
#     ]
#
#     session = create_robust_session()
#
#     working_instances = []
#     for instance in instances:
#         try:
#             # Test instance availability
#             url = f"https://{instance}/Twitter"
#             response = session.get(url, timeout=5)
#             if response.status_code == 200:
#                 working_instances.append(instance)
#         except Exception:
#             continue
#
#     if not working_instances:
#         return None
#
#     # Try to initialize scraper with working instances
#     for instance in working_instances:
#         try:
#             scraper = Nitter(instance=instance, log_level=1)
#             test = scraper.get_tweets("Twitter", mode='user', number=1)
#             if test and 'tweets' in test:
#                 return scraper
#         except Exception:
#             continue
#
#     return None
#
#
# # Function to create a colored card (unchanged)
# def create_card(tweet_text, sentiment):
#     color_map = {
#         "Positive": "rgba(0, 128, 0, 0.7)",
#         "Negative": "rgba(255, 0, 0, 0.7)",
#         "Neutral": "rgba(128, 128, 128, 0.7)",
#         "Error": "rgba(255, 165, 0, 0.7)"
#     }
#
#     color = color_map.get(sentiment, "rgba(128, 128, 128, 0.7)")
#
#     card_html = f"""
#     <div style="background-color: {color}; padding: 15px; border-radius: 10px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
#         <h5 style="color: white; margin-bottom: 10px;">{sentiment} Sentiment</h5>
#         <p style="color: white; margin: 0; line-height: 1.5;">{tweet_text}</p>
#     </div>
#     """
#     return card_html
#
#
# # Enhanced tweet fetching with multiple retries and instances
# def fetch_tweets_with_retry(scraper, username, max_retries=3):
#     if not scraper:
#         return None
#
#     for attempt in range(max_retries):
#         try:
#             tweets_data = scraper.get_tweets(username, mode='user', number=5)
#             if tweets_data and 'tweets' in tweets_data:
#                 return tweets_data
#
#             # If no tweets found, try reinitializing scraper
#             if attempt < max_retries - 1:
#                 new_scraper = initialize_scraper()
#                 if new_scraper:
#                     scraper = new_scraper
#
#         except Exception as e:
#             if attempt == max_retries - 1:
#                 st.error(f"Failed to fetch tweets after {max_retries} attempts. Error: {str(e)}")
#                 return None
#             time.sleep(2)  # Increased wait time between retries
#     return None
#
#
# # Sentiment prediction function (unchanged)
# def predict_sentiment(text, model, vectorizer, stop_words):
#     try:
#         text = re.sub('[^a-zA-Z]', ' ', text)
#         text = text.lower()
#         text = text.split()
#         text = [word for word in text if word not in stop_words]
#         text = ' '.join(text)
#
#         if not text.strip():
#             return "Neutral"
#
#         text = [text]
#         text = vectorizer.transform(text)
#         sentiment = model.predict(text)
#         return "Negative" if sentiment == 0 else "Positive"
#     except Exception as e:
#         st.error(f"Error predicting sentiment: {str(e)}")
#         return "Error"
#
#
# # Main app logic
# def main():
#     st.title("Twitter Sentiment Analysis")
#
#     # Load resources with detailed error messages
#     with st.spinner("Loading resources..."):
#         try:
#             stop_words = load_stopwords()
#             model, vectorizer = load_model_and_vectorizer()
#         except Exception as e:
#             st.error(f"Error loading model resources: {str(e)}")
#             return
#
#         scraper = initialize_scraper()
#         if not scraper:
#             st.error("""Unable to connect to any Nitter instance. This might be due to:
#             1. Network connectivity issues
#             2. Nitter instances being blocked in your region
#             3. Temporary downtime of Nitter services
#
#             Please try:
#             1. Checking your internet connection
#             2. Using a VPN service
#             3. Trying again later""")
#
#             # Still allow text analysis even if tweet fetching isn't available
#             st.info("You can still use the text analysis feature below.")
#
#     # User input options
#     option = st.selectbox("Choose an option", ["Input text", "Get tweets from user"])
#
#     if option == "Input text":
#         text_input = st.text_area("Enter text to analyze sentiment")
#         if st.button("Analyze"):
#             if text_input.strip():
#                 with st.spinner("Analyzing sentiment..."):
#                     sentiment = predict_sentiment(text_input, model, vectorizer, stop_words)
#                     card_html = create_card(text_input, sentiment)
#                     st.markdown(card_html, unsafe_allow_html=True)
#             else:
#                 st.warning("Please enter some text to analyze.")
#
#     elif option == "Get tweets from user":
#         if not scraper:
#             st.warning("Tweet fetching is currently unavailable. Please use the text input option instead.")
#             return
#
#         username = st.text_input("Enter Twitter username (without @)")
#         if st.button("Fetch Tweets"):
#             if username.strip():
#                 with st.spinner("Fetching and analyzing tweets..."):
#                     tweets_data = fetch_tweets_with_retry(scraper, username)
#
#                     if tweets_data and 'tweets' in tweets_data:
#                         for tweet in tweets_data['tweets']:
#                             tweet_text = tweet.get('text', '')
#                             if tweet_text:
#                                 sentiment = predict_sentiment(tweet_text, model, vectorizer, stop_words)
#                                 card_html = create_card(tweet_text, sentiment)
#                                 st.markdown(card_html, unsafe_allow_html=True)
#                     else:
#                         st.error("""Unable to fetch tweets. This might be because:
#                         1. The username doesn't exist
#                         2. The account is private
#                         3. There are temporary connection issues
#
#                         Please try again later or use the text input option instead.""")
#             else:
#                 st.warning("Please enter a username.")
#
#
# if __name__ == "__main__":
#     main()


import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
from ntscraper import Nitter


# Download stopwords once, using Streamlit's caching
@st.cache_resource
def load_stopwords():
    nltk.download('stopwords')
    return stopwords.words('english')


# Load model and vectorizer once
@st.cache_resource
def load_model_and_vectorizer():
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer


# Define sentiment prediction function
def predict_sentiment(text, model, vectorizer, stop_words):
    # Preprocess text
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [word for word in text if word not in stop_words]
    text = ' '.join(text)
    text = [text]
    text = vectorizer.transform(text)

    # Predict sentiment
    sentiment = model.predict(text)
    return "Negative" if sentiment == 0 else "Positive"


# Initialize Nitter scraper
@st.cache_resource
def initialize_scraper():
    return Nitter(log_level=1)


# Function to create a colored card
def create_card(tweet_text, sentiment):
    color = "green" if sentiment == "Positive" else "red"
    card_html = f"""
    <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <h5 style="color: white;">{sentiment} Sentiment</h5>
        <p style="color: white;">{tweet_text}</p>
    </div>
    """
    return card_html


# Main app logic
def main():
    st.title("Twitter Sentiment Analysis")

    # Load stopwords, model, vectorizer, and scraper only once
    stop_words = load_stopwords()
    model, vectorizer = load_model_and_vectorizer()
    scraper = initialize_scraper()

    # User input: either text input or Twitter username
    option = st.selectbox("Choose an option", ["Input text", "Get tweets from user"])

    if option == "Input text":
        text_input = st.text_area("Enter text to analyze sentiment")
        if st.button("Analyze"):
            sentiment = predict_sentiment(text_input, model, vectorizer, stop_words)
            st.write(f"Sentiment: {sentiment}")

    elif option == "Get tweets from user":
        username = st.text_input("Enter Twitter username")
        if st.button("Fetch Tweets"):
            tweets_data = scraper.get_tweets(username, mode='user', number=5)
            if 'tweets' in tweets_data:  # Check if the 'tweets' key exists
                for tweet in tweets_data['tweets']:
                    tweet_text = tweet['text']  # Access the text of the tweet
                    sentiment = predict_sentiment(tweet_text, model, vectorizer,
                                                  stop_words)  # Predict sentiment of the tweet text

                    # Create and display the colored card for the tweet
                    card_html = create_card(tweet_text, sentiment)
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.write("No tweets found or an error occurred.")


if __name__ == "__main__":
    main()
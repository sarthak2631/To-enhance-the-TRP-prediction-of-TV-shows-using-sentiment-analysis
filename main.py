from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy
import html
import string
import re

# Variables
consumer_key = 'HghmNRgZ4dROcsDskyv4cY2yM'
consumer_secret = 'PqHb8QWRf8OjydXjNk0mYy2bD7BWZFqaKTNItFsJs5FCi5632U'
access_token = '1578098575-uppy0OpZMFCrkMf5YEIGzI3hy3tBnz6Th2fwvZD'
access_secret = '2ZK33MyqnsedDDjsRDpgrTlwV0H27c5fdRxltCY1cJt8p'

# authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# initialisation
api = tweepy.API(auth)


class Cleaner:
    def __init__(self):
        self.remove_punctuations = str.maketrans('', '', string.punctuation)

    def clean_tweets(self, tweet_str):
        html_escaped = html.unescape(tweet_str)
        comma_replacement = html_escaped.replace(';', '')

        # harmonize the cases
        lower_case_text = comma_replacement.lower()
        removed_url = re.sub(r'http\S+', '', lower_case_text)

        # remove hashtags
        removed_hash_tag = re.sub(r'#\w*', '', removed_url)  # hashtag

        # remove usernames from tweets
        removed_username = re.sub(r'@\w*\s?', '', removed_hash_tag)

        # removed retweets
        removed_retweet = removed_username.replace("rt", '', True)  # remove to retweet

        # removing punctuations
        removed_punctuation = removed_retweet.translate(self.remove_punctuations)
        # remove spaces
        remove_g_t = removed_punctuation.replace("&gt", "", True)

        remove_a_m_p = remove_g_t.replace("&amp", '', True)
        final_text = remove_a_m_p
        return final_text


def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.

    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict


def start_processing(input_string):
    recipient_posts = api.user_timeline(screen_name=input_string, count=150)
    cleaner = Cleaner()
    additionOfScore = 0.0
    for tweet in recipient_posts:
        formattedData = cleaner.clean_tweets(tweet.text)
        print("\n ~TWEET -> ", formattedData)
        sentiment_dict = sentiment_scores(formattedData)

        additionOfScore += sentiment_dict['compound']

        print("Overall sentiment dictionary is : ", sentiment_dict)
        print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
        print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
        print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")

        print("Sentence Overall Rated As", end=" ")

        # decide sentiment as positive, negative and neutral
        if sentiment_dict['compound'] >= 0.05:
            print("Positive")

        elif sentiment_dict['compound'] <= - 0.05:
            print("Negative")

        else:
            print("Neutral")
        print("Compound Score --- ", sentiment_dict['compound'], "Add --- ", additionOfScore)

    totalPostsLength = len(recipient_posts)
    print("\nTotal Posts --->>> ", totalPostsLength)
    finalCompoundScore = additionOfScore / totalPostsLength
    print("finalCompoundScore --->>> ", finalCompoundScore)
    formattedScoreToShow = finalCompoundScore * 10
    print("Compound formattedScoreToShow --->>> ", formattedScoreToShow)

    return formattedScoreToShow

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pathlib import Path

from webapp.db import db
from webapp.analysis.models import Query
from webapp.reddit_api.models import Post, Comment

DEMO_FILE = './demo_file'


def analyze(sentiments_dict: dict):
    analyzer = SentimentIntensityAnalyzer()
    result = {}
    for key in sentiments_dict:
        score = analyzer.polarity_scores(sentiments_dict[key])
        result[key] = score['compound']
    return result


def count_scores(score_dict):
    pos = list()
    neg = list()
    neu = list()
    for key, score in score_dict.items():
        if score > 0.05:
            pos.append(key)
        elif score < -0.05:
            neg.append(key)
        else:
            neu.append(key)

    return {
        'pos': len(pos),
        'neu': len(neu),
        'neg': len(neg)
    }


def get_score(sentiments_dict):
    score_dict = analyze(sentiments_dict)
    return count_scores(score_dict)


def demo():
    demo_path = Path(DEMO_FILE)
    with open(demo_path, encoding='UTF-8') as file:
        sentences_list = file.readlines()

    demo_dict = dict()
    if sentences_list:
        demo_dict = {key: value for key, value in enumerate(sentences_list, start=1)}

    if demo_dict:
        print('Demo Input:')
        print(demo_dict)
        for key, sentence in demo_dict.items():
            print('Key: {}, Sentence: {}'.format(key, sentence))
        score_dict = analyze(demo_dict)
        for key, score in score_dict.items():
            print('Key: {}, Score: {}'.format(key, score))
        result = count_scores(score_dict)
        print(result['pos'], result['neu'], result['neg'])


def analyze_db(query_id):
    query = Query.query.get(query_id)
    analyzer = SentimentIntensityAnalyzer()
    for post in query.posts:
        if not post.done:
            post.score = analyzer.polarity_scores(post.body)['compound']
            post.done = True
            for comment in post.comments:
                comment.score = analyzer.polarity_scores(comment.body)['compound']
    db.session.commit()


def main():
    demo()


if __name__ == '__main__':
    main()

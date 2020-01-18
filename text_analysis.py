from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pathlib import Path


DEMO_FILE = './demo_file'


def analyze(sentiments_dict: dict):
    analyzer = SentimentIntensityAnalyzer()
    score_list = [analyzer.polarity_scores(sentiment) for sentiment in sentiments_dict.values()]
    return {key: score['compound'] for key, score in zip(sentiments_dict.keys(), score_list)}


def count_scores(score_dict):
    pos = list()
    neg = list()
    neu = list()
    for key, score in zip(score_dict.keys(), score_dict.values()):
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
    with open(demo_path) as file:
        sentences_list = file.readlines()

    demo_dict = dict()
    if sentences_list:
        demo_dict = {key: value for key, value in enumerate(sentences_list, start=1)}

    if demo_dict:
        print('Demo Input:')
        for key, sentence in zip(demo_dict.keys(), demo_dict.values()):
            print('Key: {}\n, Sentence: {}\n'.format(key, sentence))
        score_dict = analyze(demo_dict)
        for key, score in zip(score_dict.keys(), score_dict.values()):
            print('Key: {}\n, Score: {}\n'.format(key, score))


def main():
    demo()


if __name__ == '__main__':
    main()

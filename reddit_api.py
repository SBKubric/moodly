from datetime import datetime
import praw

from settings import *


def reddit_auth():
    reddit = praw.Reddit(client_id=REDDIT_ID,
                         client_secret=REDDIT_SECRET,
                         user_agent='asd')
    return reddit


reddit = reddit_auth()


def main():
    subreddit_name = 'politics'              # Multiple subreddits can be combined with a + like so: 'politics+news'
    user_search = 'Iran'
    sort_type = 'relevance'                  # Can be one of: relevance, hot, top, new, comments.
    time = 'all'                             # Can be one of: all, day, hour, month, week, year.
    limit = None                             # None=all(Если не указывать лимит, вернет только 100)
    posts = submissions(user_search, subreddit_name, time, sort_type, limit)
    post_output(posts)


def post_output(posts):
    with open('output.txt', 'w', encoding='utf-8') as f:
        for key, value in posts.items():
            f.write(f'{key}:{value},\n')


def submissions(user_search, subreddit_name, time, sort_type='relevance', limit=None):
    posts = {}
    for submission in reddit.subreddit(subreddit_name).search(user_search, sort=sort_type, time_filter=time, limit=limit):
        submission.comment_sort = 'top'              # Include best, top, new, controversial, old and q&a.
        submission.comment_limit = 10
        timestamp = submission.created_utc           # Time the submission was created, represented in Unix Time.
        submission.comments.replace_more(limit=0)
        # com_dict = {}
        # for comment in submission.comments.list()[1:]:
        #     com_dict[comment.id] = comment.body
        # value = datetime.fromtimestamp(timestamp)
        # submission_time = value.strftime('%Y-%m-%d %H:%M:%S')       # Uncomment this for normal time.
        # post = {submission.name: {'title': submission.title, 'datetime': timestamp, 'comments': com_dict}}
        # posts.update(post)
        for comment in submission.comments.list()[1:]:
            posts.update({comment.id: comment.body})
        posts.update({submission.name: submission.title})
    return posts


if __name__ == '__main__':
    main()

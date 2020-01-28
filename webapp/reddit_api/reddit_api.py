from datetime import datetime
import praw

from webapp.db import db
from webapp.settings import *
from webapp.reddit_api.models import Comment, Post
from webapp.analysis.models import Query as Query1


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


def submissions(user_search, subreddit_name, time, sort_type='relevance', limit=None, coment_length=10):
    search = reddit.subreddit(subreddit_name).search(user_search, sort=sort_type, time_filter=time, limit=limit)
    posts = {}
    for submission in reddit.subreddit(subreddit_name).search(user_search, sort=sort_type, time_filter=time, limit=limit):
        submission.comment_sort = 'top'              # Include best, top, new, controversial, old and q&a.
        submission.comment_limit = coment_length
        timestamp = submission.created_utc           # Time the submission was created, represented in Unix Time.
        submission.comments.replace_more(limit=0)
        # com_dict = {}
        # for comment in submission.comments.list()[1:]:
        #     com_dict[comment.id] = comment.body
        # value = datetime.fromtimestamp(timestamp)
        # submission_time = value.strftime('%Y-%m-%d %H:%M:%S')       # Uncomment this for normal time.
        # post = {submission.name: {'title': submission.title, 'datetime': timestamp, 'comments': com_dict}}
        # posts.update(post)
        temp = {}
        for comment in submission.comments.list()[1:]:
            temp.update({comment.id: {'author': comment.author, 'body': comment.body, 'score': 0}})
        posts.update({submission.id: {'body': submission.title, 'comments': temp, 'score': 0}})
    return posts


def get_posts(user_search, subreddit_name, time, query_id, sort_type='relevance', limit=None, coment_length=10):
    search = reddit.subreddit(subreddit_name).search(user_search, sort=sort_type, time_filter=time, limit=limit)
    posts_list = [_.id for _ in search]
    posts_db = [_.reddit_id for _ in Post.query.filter(Post.reddit_id.in_(posts_list)).all()]
    query = Query1.query.get(query_id)
    index = 1
    for submission in reddit.subreddit(subreddit_name).search(user_search, sort=sort_type, time_filter=time, limit=limit):
        if submission.id not in posts_db:
            url = f'https://www.reddit.com{submission.permalink}/'
            new_post = Post(reddit_id=submission.id, body=submission.title, url=url, score=0)
            db.session.add(new_post)
            db.session.commit()
            submission.comment_sort = 'top'              # Include best, top, new, controversial, old and q&a.
            submission.comment_limit = coment_length
            timestamp = submission.created_utc           # Time the submission was created, represented in Unix Time.
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list()[1:]:
                url = f'https://www.reddit.com{comment.permalink}/{comment.id}/'
                new_comment = Comment(reddit_id=comment.id, body=comment.body,
                                      author=str(comment.author), post_id=new_post.id, url=url, score=0)
                db.session.add(new_comment)
            query.posts.append(new_post)
            query.percent = int(index / len(posts_list) * 100)
            db.session.commit()
            index += 1


if __name__ == '__main__':
    main()

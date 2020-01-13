import praw
import datetime


def reddit_auth():
    reddit = praw.Reddit(client_id='MiYLmXFcRgXUoQ',
                        client_secret='6eo6bQCAWsk90SNviVrLnFH-Ft0',
                        user_agent='asd')
    return reddit


def main():
    subreddit_name = 'politics'              # Multiple subreddits can be combined with a + like so: 'politics+news'
    user_search = 'Iran'                    
    sort_type = 'relevance'                  # Can be one of: relevance, hot, top, new, comments.
    time = 'all'                             # Can be one of: all, day, hour, month, week, year.
    limit = None                             # None=all(Если не указывать лимит, вернет только 100)
    reddit = reddit_auth()
    posts = submissions(reddit, user_search, subreddit_name, sort_type, time, limit)
    post_output(posts)


def post_output(posts):
    with open('output.txt', 'w', encoding='utf-8') as f:
        for post in posts:
            f.write(f'{post}\n')


def submissions(reddit, user_search, subreddit_name, sort_type, time, limit):
    posts = []
    for submission in reddit.subreddit(subreddit_name).search(user_search, sort=sort_type, time_filter=time, limit=limit):
        timestamp = submission.created_utc   # Time the submission was created, represented in Unix Time.
        value = datetime.datetime.fromtimestamp(timestamp)
        submission_time = value.strftime('%Y-%m-%d %H:%M:%S')
        # print(f'{num}:[{submission.name}] {submission.title}({submission_time})')
        posts.append({'name':submission.name,'title':submission.title,'time':submission_time})
    return posts

    # for num, submission in enumerate(reddit.subreddit(subreddit_name).search(user_search, sort=sort_type, time_ filter=time, limit=limit), 1):
    #     print(f'{num} : {submission.title}\n{submission.selftext}')


if __name__ == '__main__':
    main()
# This is the code to scrape comments from reddit - India
!pip -q install praw
import praw
import pandas as pd
import numpy as np

SECRET="wiL7KNJbsYzRvvc40MQOBonf-PSl2g"
ID="NWnTxGjYDwElTbwpg9SfgA"

# Authorized instance
reddit_authorized = praw.Reddit(client_id=ID,		 # your client id
								client_secret=SECRET,	 # your client secret
								user_agent="scrape",	 # your user agent
								username="FrequentObligation65" # your reddit username
								)

pd.set_option('max_colwidth', None)
df = []

subreddit = reddit_authorized.subreddit('India')

for post in subreddit.top(limit=101):
    df.append([post.title, post.id, post.score, post.url, post.num_comments, post.selftext])

top_100_posts_df = pd.DataFrame(df,columns=['title', 'id', 'score', 'url', 'num_comments', 'body'])

top_100_posts_df = top_100_posts_df.drop(44).set_index(pd.Index(range(100)))
top_100_posts_df.to_csv("posts.csv", index=False)

top_100_posts_df.info()

top_100_posts_df["num_comments"][44]

import time
for a in range(20):
  for b in range(5*a,5*(a+1)):
    post_id = top_100_posts_df["id"][b]
    submission = reddit_authorized.submission(post_id)
    submission.comments.replace_more(limit=None)
    all_comm=[]
    for comment in submission.comments.list():
        all_comm.append({
          "Comment ID": comment.id,
          "Comment Text": comment.body,
          "Comment Score": comment.score,
          "Comment Depth": comment.depth,
          "Created Timestamp": comment.created_utc,
          "Author": str(comment.author),
          "Edited":comment.edited,
        })
    print(b)
    comm_df = pd.DataFrame(all_comm)
    comm_df.to_csv(f"{post_id}.csv", index=False)
    time.sleep(60)
  time.sleep(10*60)

# Get the post object using the URL or ID
post = reddit_authorized.submission("mxe8r0")

# Create a list to store comment data
comment_data = []

# Retrieve and store comments for the post

post.comments.replace_more(limit=None)
comment_data=[]
for comment in post.comments.list():
    comment_data.append({
        "Comment ID": comment.id,
        "Comment Text": comment.body,
        "Comment Score": comment.score,
        "Comment Depth": comment.depth,
        "Created Timestamp": comment.created_utc,
        "Author": str(comment.author),
        "Edited":comment.edited,
        # Add additional comment information fields as needed
    })

# Create a pandas DataFrame from the comment data
comments_df = pd.DataFrame(comment_data)

# Add post metadata to the DataFrame
post_data = {
    "Title": post.title,
    "ID": post.id,
    "URL": post.url,
    "Score (Upvotes)": post.score,
    "Number of Comments": post.num_comments,
    "Created Timestamp": post.created_utc,
    "Subreddit": post.subreddit.display_name,
    "Upvote Ratio": post.upvote_ratio,
    "Author": str(post.author),
    #"Author Karma": post.author.link_karma,
    #"Account Age": (post.author.created_utc - reddit_authorized.user.me().created_utc) / (60*60*24),
    "Text Content": post.selftext,
}

post_df = pd.DataFrame([post_data])

comments_df.info()

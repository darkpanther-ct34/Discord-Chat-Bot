import praw
import random
import discord
# from discord.ext import commands
# import requests
import requests.auth
import os
from dotenv import load_dotenv
load_dotenv()

user_agent = "Discord_bot/0.1 by Discord_bot_7667"


ID = os.getenv('client_id')
secret = os.getenv('client_secret')

username = os.getenv('reddit_username')
password = os.getenv('reddit_password')


client_auth = requests.auth.HTTPBasicAuth(ID, secret)
post_data = {"grant_type": "password", "username": username, "password": password}
headers = {"User-Agent": user_agent}
response = requests.post("https://www.reddit.com/api/v1/access_token",
                         auth=client_auth,
                         data=post_data,
                         headers=headers
                         )
response.json()

authorisation_token = response.json()["token_type"]+' '+response.json()["access_token"]
headers = {"Authorization": authorisation_token, "User-Agent": user_agent}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
response.json()

reddit = praw.Reddit(
    client_id=ID,
    client_secret=secret,
    user_agent=user_agent,
    check_for_async=False
)


def display_meme(memes):
    for submission in reddit.subreddit("memes").hot(limit=30):
        memes.append({"author": str(submission.author),
                      "URL for img": submission.url,
                      "URL": ("https://www.reddit.com" + submission.permalink),
                      "title": submission.title,
                      "text": submission.selftext})
    chosenmeme = random.choice(memes)
    imageurl = chosenmeme["URL for img"]
    embedvar = discord.Embed(title=chosenmeme["title"], url=chosenmeme["URL"], description="", colour=0x3CA47C)
    embedvar.set_image(url=imageurl)
    embedvar.set_author(name=chosenmeme["author"], icon_url=(reddit.redditor(chosenmeme["author"])).icon_img)
    return embedvar


def display_cursed_image(cursed_images):
    for submission in reddit.subreddit("cursedimages").hot(limit=30):
        cursed_images.append({"author": str(submission.author),
                              "URL for img": submission.url,
                              "URL": ("https://www.reddit.com" + submission.permalink),
                              "title": submission.title,
                              "text": submission.selftext})
    chosencursed = random.choice(cursed_images)
    imageurl = chosencursed["URL for img"]
    embedvar = discord.Embed(title=chosencursed["title"], url=chosencursed["URL"], description="", color=0xD92C2C)
    embedvar.set_image(url=imageurl)
    embedvar.set_author(name=chosencursed["author"], icon_url=(reddit.redditor(chosencursed["author"])).icon_img)
    return embedvar


def display_art(art):
    for submission in reddit.subreddit("Art").hot(limit=30):
        art.append({"author": str(submission.author),
                    "URL for img": submission.url,
                    "URL": ("https://www.reddit.com" + submission.permalink),
                    "title": submission.title,
                    "text": submission.selftext})
    chosenart = random.choice(art)
    imageurl = chosenart["URL for img"]
    embedvar = discord.Embed(title=chosenart["title"], url=chosenart["URL"], description="", color=0x2CC9D9)
    embedvar.set_image(url=imageurl)
    embedvar.set_author(name=chosenart["author"], icon_url=(reddit.redditor(chosenart["author"])).icon_img)
    return embedvar


def display_cursed_comment(comment):
    for submission in reddit.subreddit("cursedcomments").hot(limit=30):
        comment.append({"author": str(submission.author),
                        "URL for img": submission.url,
                        "URL": submission.url_overridden_by_dest,
                        "title": submission.title,
                        "text": submission.selftext})
    chosencomment = random.choice(comment)
    embedvar = discord.Embed(title=chosencomment["title"], description=chosencomment["URL"], color=0x00ff00)
    embedvar.add_field(name="Posted by:", value=chosencomment["author"], inline=False)
    return embedvar


def display_joke(joke):
    for submission in reddit.subreddit("Jokes").hot(limit=30):
        joke.append({"author": str(submission.author), "URL": submission.url, "title": submission.title,
                     "text": submission.selftext})
    chosenjoke = random.choice(joke)
    while len(chosenjoke["title"]) > 256:
        chosenjoke = random.choice(joke)
    embedvar = discord.Embed(title=chosenjoke["title"], description=chosenjoke["text"], color=0x88D92C)
    embedvar.set_author(name=chosenjoke["author"], icon_url=(reddit.redditor(chosenjoke["author"])).icon_img)
    return embedvar

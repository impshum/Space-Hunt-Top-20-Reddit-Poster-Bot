from bs4 import BeautifulSoup
from requests import get
from time import sleep
import praw
import schedule
import demoji
import configparser


def lovely_soup(u):
    r = get(u, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'})
    return BeautifulSoup(r.text, 'lxml')


def runner(reddit, target_subreddit, post_title):
    soup = lovely_soup(
        'https://xaviesteve.com/pro/spacehuntbot/?rankings').text
    lines = demoji.replace(soup, '')
    lines = lines.split('\n')
    table = '**Rank**|**User**|**Score**\n:-:|:-:|:-:\n'

    for line in lines:
        parts = line.split(' ')
        parts[0] = parts[0].replace('.', '')
        new_line = f'{parts[0]}|{parts[2]}|{parts[3]}\n'
        table += new_line
    r = reddit.subreddit(target_subreddit).submit(
        post_title, selftext=table)
    print(f'Posted - https://reddit.com{r.permalink}')


def main():
    config = configparser.ConfigParser()
    config.read('conf.ini')
    reddit_user = config['REDDIT']['reddit_user']
    reddit_pass = config['REDDIT']['reddit_pass']
    client_id = config['REDDIT']['client_id']
    client_secret = config['REDDIT']['client_secret']
    target_subreddit = config['REDDIT']['target_subreddit']
    post_title = config['REDDIT']['post_title']

    reddit = praw.Reddit(
        username=reddit_user,
        password=reddit_pass,
        client_id=client_id,
        client_secret=client_secret,
        user_agent='Space Hunt Top 20 Reddit Poster Bot (by u/impshum)'
    )

    if not demoji.last_downloaded_timestamp():
        demoji.download_codes()

    print('Waiting until scheduled')
    schedule.every().monday.do(runner, reddit, target_subreddit, post_title)
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()

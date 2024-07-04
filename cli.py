import os
import argparse
import logging
import sys
import random
import requests
from datetime import datetime
from fpdf import FPDF
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import time
import csv
import os


# Configuration
LOG_PATH = "logs/user_finder_zeta.log"
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.3 Safari/602.3.12",
]

def print_banner():
    print("""
░▀▀█░█▀▀░▀█▀░█▀█░░░█▀█░█▀▀░▀█▀░█▀█░▀█▀
░▄▀░░█▀▀░░█░░█▀█░░░█░█░▀▀█░░█░░█░█░░█░
░▀▀▀░▀▀▀░░▀░░▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░
        """)

# List of social media platforms and their respective URL formats for usernames
PLATFORMS = {
    "Instagram": "https://www.instagram.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Twitter": "https://www.twitter.com/{}",
    "YouTube": "https://www.youtube.com/{}",
    "Blogger": "https://{}.blogspot.com",
    "Reddit": "https://www.reddit.com/user/{}",
    "WordPress": "https://{}.wordpress.com",
    "Pinterest": "https://www.pinterest.com/{}",
    "GitHub": "https://www.github.com/{}",
    "Tumblr": "https://{}.tumblr.com",
    "Flickr": "https://www.flickr.com/people/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Disqus": "https://disqus.com/{}",
    "Medium": "https://medium.com/@{}",
    "DeviantART": "https://{}.deviantart.com",
    "VK": "https://vk.com/{}",
    "About.me": "https://about.me/{}",
    "Imgur": "https://imgur.com/user/{}",
    "Flipboard": "https://flipboard.com/@{}",
    "SlideShare": "https://slideshare.net/{}",
    "Fotolog": "https://fotolog.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "MixCloud": "https://www.mixcloud.com/{}",
    "Scribd": "https://www.scribd.com/{}",
    "Badoo": "https://www.badoo.com/en/{}",
    "Patreon": "https://www.patreon.com/{}",
    "BitBucket": "https://bitbucket.org/{}",
    "DailyMotion": "https://www.dailymotion.com/{}",
    "Etsy": "https://www.etsy.com/shop/{}",
    "CashMe": "https://cash.me/{}",
    "Behance": "https://www.behance.net/{}",
    "GoodReads": "https://www.goodreads.com/{}",
    "Instructables": "https://www.instructables.com/member/{}",
    "Keybase": "https://keybase.io/{}",
    "Kongregate": "https://kongregate.com/accounts/{}",
    "LiveJournal": "https://{}.livejournal.com",
    "AngelList": "https://angel.co/{}",
    "Last.fm": "https://last.fm/user/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Codecademy": "https://www.codecademy.com/{}",
    "Gravatar": "https://en.gravatar.com/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Foursquare": "https://foursquare.com/{}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "Gumroad": "https://www.gumroad.com/{}",
    "Newgrounds": "https://{}.newgrounds.com",
    "Wattpad": "https://www.wattpad.com/user/{}",
    "Canva": "https://www.canva.com/{}",
    "CreativeMarket": "https://creativemarket.com/{}",
    "Trakt": "https://www.trakt.tv/users/{}",
    "500px": "https://500px.com/{}",
    "Buzzfeed": "https://buzzfeed.com/{}",
    "TripAdvisor": "https://tripadvisor.com/members/{}",
    "HubPages": "https://{}.hubpages.com",
    "Contently": "https://{}.contently.com",
    "Houzz": "https://houzz.com/user/{}",
    "Blip.fm": "https://blip.fm/{}",
    "Wikipedia": "https://www.wikipedia.org/wiki/User:{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "CodeMentor": "https://www.codementor.io/{}",
    "ReverbNation": "https://www.reverbnation.com/{}",
    "Designspiration": "https://www.designspiration.net/{}",
    "Bandcamp": "https://www.bandcamp.com/{}",
    "ColourLovers": "https://www.colourlovers.com/love/{}",
    "IFTTT": "https://www.ifttt.com/p/{}",
    "Ebay": "https://www.ebay.com/usr/{}",
    "Slack": "https://{}.slack.com",
    "OkCupid": "https://www.okcupid.com/profile/{}",
    "Trip": "https://www.trip.skyscanner.com/user/{}",
    "Ello": "https://ello.co/{}",
    "Tracky": "https://tracky.com/user/{}",
    "Tripit": "https://www.tripit.com/people/{}#/profile/basic-info",
    "Basecamp": "https://{}.basecamphq.com/login",
    "TikTok": "https://www.tiktok.com/@{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "MySpace": "https://myspace.com/{}",
    "Weibo": "https://weibo.com/{}",
    "WeChat": "https://www.wechat.com/en/{}",
    "Periscope": "https://www.pscp.tv/{}",
    "Vine": "https://vine.co/u/{}",
    "Telegram": "https://t.me/{}",
    "WhatsApp": "https://wa.me/{}",
    "Facebook": "https://www.facebook.com/public/{}",
    "Signal": "https://signal.me/#p/{}",
    "Matrix": "https://matrix.to/#/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Tumblr": "https://www.tumblr.com/{}",
    "Flickr": "https://www.flickr.com/photos/{}",
    "SoundCloud": "https://www.soundcloud.com/{}",
    "Spotify": "https://www.open.spotify.com/user/{}",
    "Vimeo": "https://www.vimeo.com/{}",
    "Dribbble": "https://www.dribbble.com/{}",
    "DeviantArt": "https://www.{}.deviantart.com/",
    "500px": "https://www.500px.com/{}",
    "Medium": "https://www.medium.com/@{}",
    "Quora": "https://www.quora.com/profile/{}",
    "Stack Overflow": "https://www.stackoverflow.com/users/{}",
    "GitLab": "https://www.gitlab.com/{}",
    "Bitbucket": "https://www.bitbucket.org/{}",
    "HackerRank": "https://www.hackerrank.com/{}",
    "CodePen": "https://www.codepen.io/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "Steam": "https://www.steamcommunity.com/id/{}",
    "Origin": "https://www.origin.com/id/{}",
    "Amazon": "https://www.amazon.com/gp/profile/{}",
    "IMDb": "https://www.imdb.com/user/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "Last.fm": "https://www.last.fm/user/{}",
    "TripAdvisor": "https://www.tripadvisor.com/members/{}",
    "VSCO": "https://www.vsco.co/{}",
    "Ello": "https://www.ello.co/{}",
    "WeHeartIt": "https://www.weheartit.com/{}",
    "Couchsurfing": "https://www.couchsurfing.com/people/{}",
    "Zillow": "https://www.zillow.com/profile/{}",
    "Realtor.com": "https://www.realtor.com/realestateagents/{}",
    "Airbnb": "https://www.airbnb.com/users/show/{}",
    "Booking.com": "https://www.booking.com/profile/{}",
    "Duolingo": "https://www.duolingo.com/profile/{}",
    "Reddit (Subreddit)": "https://www.reddit.com/r/{}",
    "Discord": "https://www.discordapp.com/users/{}",
    "Foursquare": "https://www.foursquare.com/user/{}",
    "Wikipedia": "https://www.en.wikipedia.org/wiki/User:{}",
    "Wikimedia Commons": "https://www.commons.wikimedia.org/wiki/User:{}",
    "Wiktionary": "https://www.en.wiktionary.org/wiki/User:{}",
    "Wikibooks": "https://www.en.wikibooks.org/wiki/User:{}",
    "Wikiquote": "https://www.en.wikiquote.org/wiki/User:{}",
    "Wikisource": "https://www.en.wikisource.org/wiki/User:{}",
    "Wikiversity": "https://www.en.wikiversity.org/wiki/User:{}",
    "Wikihow": "https://www.wikihow.com/User:{}",
    "Metacritic": "https://www.metacritic.com/user/{}",
    "Rotten Tomatoes": "https://www.rottentomatoes.com/user/id/{}",
    "Letterboxd": "https://www.letterboxd.com/{}",
    "Discogs": "https://www.discogs.com/user/{}",
    "Mixcloud": "https://www.mixcloud.com/{}",
    "Tidal": "https://www.listen.tidal.com/{}",
    "Hulu": "https://www.hulu.com/profiles/{}",
    "Crunchyroll": "https://www.crunchyroll.com/user/{}",
    "NPR": "https://www.npr.org/people/{}",
    "New York Times": "https://www.nytimes.com/by/{}",
    "Washington Post": "https://www.washingtonpost.com/people/{}",
    "The Guardian": "https://www.theguardian.com/profile/{}",
    "BBC": "https://www.bbc.com/user/{}",
    "CNN": "https://www.edition.cnn.com/profiles/{}",
    "Fox News": "https://www.foxnews.com/person/{}",
    "Reuters": "https://www.reuters.com/journalists/{}",
    "Bloomberg": "https://www.bloomberg.com/authors/{}",
    "CNBC": "https://www.cnbc.com/{}",
    "Forbes": "https://www.forbes.com/sites/{}",
    "Business Insider": "https://www.businessinsider.com/author/{}",
    "The Verge": "https://www.theverge.com/users/{}",
    "TechCrunch": "https://www.techcrunch.com/author/{}",
    "Wired": "https://www.wired.com/author/{}",
    "Ars Technica": "https://www.arstechnica.com/author/{}",
    "National Geographic": "https://www.nationalgeographic.com/contributors/{}",
    "NASA": "https://www.nasa.gov/profiles/{}",
    "ESPN": "https://www.espn.com/nba/player/_/id/{}",
    "NFL": "https://www.nfl.com/players/{}",
    "NBA": "https://www.nba.com/player/{}",
    "MLB": "https://www.mlb.com/player/{}",
    "NHL": "https://www.nhl.com/player/{}",
    "UEFA": "https://www.uefa.com/uefachampionsleague/clubs/{}",
    "FIFA": "https://www.fifa.com/fifa-world-ranking/{}",
    "Olympics": "https://www.olympics.com/tokyo-2020/olympic-games/en/results/all-sports/athletes/{}",
    "World Athletics": "https://www.worldathletics.org/athletes/{}",
    "IMDb Pro": "https://www.pro.imdb.com/profile/{}",
    "Academia.edu": "https://www.academia.edu/{}",
    "ResearchGate": "https://www.researchgate.net/profile/{}",
    "Google Scholar": "https://www.scholar.google.com/citations?user={}",
    "Microsoft Academic": "https://www.academic.microsoft.com/profile/{}",
    "ORCID": "https://www.orcid.org/{}",
    "Scopus": "https://www.scopus.com/authid/detail.uri?authorId={}",
    "Publons": "https://www.publons.com/researcher/{}",
    "Mendeley": "https://www.mendeley.com/profiles/{}",
    "Semantic Scholar": "https://www.semanticscholar.org/author/{}",
    "Academic Tree": "https://www.academictree.org/{}",
    "IEEE Xplore": "https://www.ieeexplore.ieee.org/author/{}",
    "Springer": "https://www.link.springer.com/{}",
    "ScienceDirect": "https://www.sciencedirect.com/scientist/{}",
    "PLOS": "https://www.plos.org/profile/{}",
    "Nature": "https://www.nature.com/srep/{}",
    "Reddit": "https://www.reddit.com/u/{}",

}

# List of email search patterns for platforms
EMAIL_PLATFORMS = {
    "facebook": "https://www.facebook.com/search/top/?q={}",
    "github": "https://www.github.com/search?q={}",
    "twitter": "https://www.twitter.com/i/api/1.1/users/email_available.json?email={}",
    "instagram": "https://www.instagram.com/accounts/account_recovery_send_ajax/email/",
    "instagram": "https://www.instagram.com/accounts/account_recovery_send_ajax/{}",
    "instagram": "https://www.instagram.com/accounts/account_recovery_send_ajax/email/{}",
    "linkedin": "https://www.linkedin.com/checkpoint/rp/request-password-reset-submit?email={}",
    "snapchat": "https://www.accounts.snapchat.com/accounts/password_reset_request",
    "pinterest": "https://www.pinterest.com/password/reset/?email={}",
    "reddit": "https://www.reddit.com/password/?email={}",
    "Gravatar": "https://www.gravatar.com/avatar/{}",
    "Facebook": "https://www.facebook.com/search/top/?q={}",
    "LinkedIn": "https://www.linkedin.com/search/results/all/?keywords={}",
    "Twitter": "https://twitter.com/search?q={}",
    "Pinterest": "https://www.pinterest.com/search/pins/?q={}",
    "Spotify": "https://open.spotify.com/user/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Medium": "https://medium.com/@{}",
    "VK": "https://vk.com/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "YouTube": "https://www.youtube.com/{}",
    "WordPress": "https://{}.wordpress.com",
    "Blogger": "https://{}.blogspot.com",
    "MixCloud": "https://www.mixcloud.com/{}",
    "Disqus": "https://disqus.com/{}",
    "DeviantART": "https://{}.deviantart.com",
    "Tumblr": "https://{}.tumblr.com",
    "AngelList": "https://angel.co/{}",
    "GoodReads": "https://www.goodreads.com/{}",
    "Kongregate": "https://kongregate.com/accounts/{}",
    "Keybase": "https://keybase.io/{}",
    "Behance": "https://www.behance.net/{}",
    "TripAdvisor": "https://tripadvisor.com/members/{}",
    "Instructables": "https://www.instructables.com/member/{}",
    "Foursquare": "https://foursquare.com/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Newgrounds": "https://{}.newgrounds.com",
    "Canva": "https://www.canva.com/{}",
    "CreativeMarket": "https://creativemarket.com/{}",
    "Trakt": "https://www.trakt.tv/users/{}",
    "500px": "https://500px.com/{}",
    "Buzzfeed": "https://buzzfeed.com/{}",
    "Contently": "https://{}.contently.com",
    "Houzz": "https://houzz.com/user/{}",
    "Blip.fm": "https://blip.fm/{}",
    "Wikipedia": "https://www.wikipedia.org/wiki/User:{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "CodeMentor": "https://www.codementor.io/{}",
    "ReverbNation": "https://www.reverbnation.com/{}",
    "Designspiration": "https://www.designspiration.net/{}",
    "Bandcamp": "https://www.bandcamp.com/{}",
    "ColourLovers": "https://www.colourlovers.com/love/{}",
    "IFTTT": "https://www.ifttt.com/p/{}",
    "Ebay": "https://www.ebay.com/usr/{}",
    "Slack": "https://{}.slack.com",
    "OkCupid": "https://www.okcupid.com/profile/{}",
    "Trip": "https://www.trip.skyscanner.com/user/{}",
    "Ello": "https://ello.co/{}",
    "Tracky": "https://tracky.com/user/{}",
    "Tripit": "https://www.tripit.com/people/{}#/profile/basic-info",
    "Basecamp": "https://{}.basecamphq.com/login",
    "TikTok": "https://www.tiktok.com/@{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "MySpace": "https://myspace.com/{}",
    "Weibo": "https://weibo.com/{}",
    "WeChat": "https://www.wechat.com/en/{}",
    "Periscope": "https://www.pscp.tv/{}",
    "Vine": "https://vine.co/u/{}",
    "Telegram": "https://t.me/{}",
    "WhatsApp": "https://wa.me/{}",
    "Signal": "https://signal.me/#p/{}",
    "Matrix": "https://matrix.to/#/@{}",
    "Discord": "https://discord.com/users/{}"
}

PLATFORMS_API = {
    "Github": "https://github.com/search",
    "Mastodon": "https://mastodon.social/api/v2/search",
    "Discords": "https://discords.com/api-v2/bio/search"
}

# Helper functions
def get_random_user_agent():
    return random.choice(USER_AGENT_LIST)

def is_file(filepath):
    return os.path.isfile(filepath)

def get_lines_from_file(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file]

def create_save_directory():
    if not os.path.exists("results"):
        os.makedirs("results")

def generate_unique_filename(base_filename, extension):
    counter = 0
    while True:
        if counter == 0:
            filename = f"{base_filename}.{extension}"
        else:
            filename = f"{base_filename}({counter}).{extension}"
        if not os.path.exists(f"results/{filename}"):
            return filename
        counter += 1

def save_to_csv(data, base_filename):
    filename = generate_unique_filename(base_filename, "csv")
    with open(f"results/{filename}", "w") as file:
        for line in data:
            file.write(line + "\n")

def save_to_txt(data, base_filename):
    filename = generate_unique_filename(base_filename, "txt")
    with open(f"results/{filename}", "w") as file:
        for line in data:
            file.write(line + "\n")

def save_to_pdf(data, base_filename):
    filename = generate_unique_filename(base_filename, "pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in data:
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(f"results/{filename}")

def display_progress(current, total):
    progress = (current / total) * 100
    print(f"Progress: {progress:.2f}%")

# Core functions
def check_platform(platform, url, identifier, headers):
    full_url = url.format(identifier)
    try:
        response = requests.get(full_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return f"{platform}: {full_url}/"
        else:
            return None
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        logging.error(f"Error checking {full_url}: {e}")
        return None

def verify_username(username):
    print(f"Verifying username: {username}")
    found_accounts = []
    headers = {"User-Agent": get_random_user_agent()}
    total_platforms = len(PLATFORMS)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(check_platform, platform, url, username, headers) for platform, url in PLATFORMS.items()]
        for count, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                found_accounts.append(result)
                print(result)
            display_progress(count, total_platforms)
    return found_accounts

def verify_email(email):
    print(f"Verifying email: {email}")
    found_accounts = []
    headers = {"User-Agent": get_random_user_agent()}
    total_platforms = len(EMAIL_PLATFORMS)
    hashed_email = hashlib.md5(email.encode()).hexdigest()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(check_platform, platform, url, hashed_email, headers) for platform, url in EMAIL_PLATFORMS.items()]
        for count, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                found_accounts.append(result)
                print(result)
            display_progress(count, total_platforms)
    return found_accounts

class Permute:
    def __init__(self, elements):
        self.elements = elements

    def gather(self, way):
        if way == "strict":
            return ["".join(self.elements)]
        elif way == "all":
            return ["".join(self.elements), "".join(reversed(self.elements))]

def github_api_driver(URL, user_input):
    print(":: Searching on Github ...")

    output_file = "./results/github-profiles.txt" # add prefix to file name
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}
    user_input.replace(" ", "+")

    r = requests.get(URL, f"q={user_input}&type=users", headers=headers)
    print(r.url)
    text = r.text
    text_json = json.loads(text) # convert to json object
    page_count = text_json["payload"]["page_count"] # Get page count
    result_count = text_json["payload"]["result_count"] # Get result count
    profile = text_json["payload"]["results"]

    print(f"Page count: {page_count}")
    print(f"Result count: {result_count}")
    output_file = open(output_file, "w")
    csv_writer = csv.writer(output_file)

    for page in range(1, page_count+1):
        r = requests.get(URL, f"q={user_input}&type=users&p={page}", headers=headers)
        if r.status_code == 429:
            print("Github API rate limited Reached !! ... retrying in 60 seconds")
            page = page - 2
            time.sleep(40)
            print("resuming :)")
        else:
            text_json = json.loads(r.text)
            text_json = text_json["payload"]["results"] # Extract profiles data

            # Write data in csv file
            write_csv(text_json, csv_writer)
            time.sleep(2)

    output_file.close()

def mastodon_api_driver(URL, user_input):

    output_file = "results/mastodon.txt"
    MASTODON_API = os.environ.get("MASTODON_API")

    if not MASTODON_API:
        print("Error: Mastodon API token not found!\nSee manual for adding token.") # TODO add in help section
        return

    print(":: Searching on Mastodon ...")
    print("Mastodon API Token found!")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
                        "Authorization": f"Bearer {MASTODON_API}"}
    parameters = f"q={user_input}&type=accounts"
    user_input = user_input.replace(" ", "+")

    r = requests.get(URL, parameters, headers=headers)
    print(r.url)
    text = r.text
    text_json = json.loads(text) # convert to json object

    output_file = open(output_file, "w")
    csv_writer = csv.writer(output_file)

    r = requests.get(URL, parameters, headers=headers)
    text_json = json.loads(r.text)
    text_json = text_json["accounts"] # extract accounts data

    # Write to file
    write_csv(text_json, csv_writer)
    output_file.close()

def discord_api_driver(URL, user_input):
    print(":: Searching on Discord ...")
    output_file = "results/discord.txt" # add prefix to file name
    parameters = f"term={user_input}"
    user_input.replace(" ", "+")

    r = requests.get(URL, params=parameters)
    print(r.url)
    text = r.text
    text_json = json.loads(text) # convert to json object
    page_count = text_json["pages"] # Get page count
    print(f"Page count: {page_count}")

    output_file = open(output_file, "w")
    csv_writer = csv.writer(output_file)

    for page in range(1, page_count+1):
        r = requests.get(URL, parameters)
        if r.status_code == 429: # Rate limit logic
            print("Discord API rate limited Reached !! ... retrying in 60 seconds")
            page = page - 2
            time.sleep(40)
            print("resuming :)")
        else:
            text_json = json.loads(r.text)
            text_json = text_json["users"] # Extract users data
            print(text_json)
            # Write data in csv file
            write_csv(text_json, csv_writer)
            time.sleep(2)

    output_file.close()

def write_csv(text_json, csv_writer):
    count = 0
    for profile in text_json:
        if count == 0: # write headers
            header = profile.keys()
            csv_writer.writerow(header)
            count += 1

        csv_writer.writerow(profile.values())

def main():
    print_banner()

    if not os.path.exists("logs/"):
        os.makedirs("logs/")
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(
        prog="user-finder-zeta",
        description="An OSINT tool to search for accounts by username or email in social networks.",
    )
    parser.add_argument("-u", "--username", nargs="*", type=str, help="One or more usernames to search.")
    parser.add_argument("-uf", "--username-file", help="The list of usernames to be searched.")
    parser.add_argument("--permute", action="store_true", help="Permute usernames, ignoring single elements.")
    parser.add_argument("--permuteall", action="store_true", help="Permute usernames, all elements.")
    parser.add_argument("-e", "--email", nargs="*", type=str, help="One or more emails to search.")
    parser.add_argument("-ef", "--email-file", help="The list of emails to be searched.")
    parser.add_argument("--csv", action="store_true", help="Generate a CSV with the results.")
    parser.add_argument("--pdf", action="store_true", help="Generate a PDF with the results.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose output.")
    parser.add_argument("--filter", help='Filter sites to be searched by list property value. E.g., --filter "cat=social"')
    parser.add_argument("--no-nsfw", action="store_true", help="Removes NSFW sites from the search.")
    parser.add_argument("--dump", action="store_true", help="Dump HTML content for found accounts.")
    parser.add_argument("--proxy", help="Proxy to send HTTP requests through.")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds for each HTTP request (Default is 30).")
    parser.add_argument("--max-concurrent-requests", type=int, default=30, help="Specify the maximum number of concurrent requests allowed. Default is 30.")
    parser.add_argument("--no-update", action="store_true", help="Don't update sites lists.")
    parser.add_argument("--about", action="store_true", help="Show about information and exit.")
    parser.add_argument("-p", "--profile", dest="profile",metavar="NAME" , help="Search related profiles - API key may required!")

    args = parser.parse_args()

    username = args.username
    username_file = args.username_file
    permute = args.permute
    permuteall = args.permuteall
    csv = args.csv
    pdf = args.pdf
    filter = args.filter
    no_nsfw = args.no_nsfw
    dump = args.dump
    proxy = args.proxy
    verbose = args.verbose
    timeout = args.timeout
    max_concurrent_requests = args.max_concurrent_requests
    email = args.email
    email_file = args.email_file
    no_update = args.no_update
    about = args.about
    profile = args.profile

    create_save_directory()
    if about:
        print("""
        Author: Team Zeta ITSOLERA
        Description: User-Finder-Zeta is an OSINT tool that performs reverse search in username and emails.
        """)
        sys.exit()
    if (hasattr(args, "profile") and args.profile):
        print("\\o/:: Searching profile")
        github_api_driver(PLATFORMS_API["Github"], args.profile)
        mastodon_api_driver(PLATFORMS_API["Mastodon"], args.profile)
        discord_api_driver(PLATFORMS_API["Discords"], args.profile)
        exit()

    if not username and not email and not username_file and not email_file:
        print("Must profile -u/--username, -e/--email, or -p/--profile is required")
        sys.exit()
    if not username and (permute or permuteall):
        print("Permutations requires --username")
        sys.exit()

    all_found_accounts = []

    # Load usernames from file
    if username_file:
        if is_file(username_file):
            username = get_lines_from_file(username_file)
            print(f'Successfully loaded {len(username)} usernames from "{username_file}"')
        else:
            print(f'Could not read file "{username_file}"')
            sys.exit()

    # Permute usernames if required
    if username:
        if (permute or permuteall) and len(username) > 1:
            elements = " ".join(username)
            way = "all" if permuteall else "strict"
            permute = Permute(username)
            username = permute.gather(way)
            print(f'Successfully loaded {len(username)} usernames from permuting {elements}')

        # Verify usernames
        for user in username:
            all_found_accounts.extend(verify_username(user))

        # Save results if required
        if csv:
            save_to_csv(all_found_accounts, "usernames_results")
        if pdf:
            save_to_pdf(all_found_accounts, "usernames_results")
        save_to_txt(all_found_accounts, "found-result-usernames")

    # Load emails from file
    if email_file:
        if is_file(email_file):
            email = get_lines_from_file(email_file)
            print(f'Successfully loaded {len(email)} emails from "{email_file}"')
        else:
            print(f'Could not read file "{email_file}"')
            sys.exit()

    # Verify emails
    if email:
        for mail in email:
            all_found_accounts.extend(verify_email(mail))

        # Save results if required
        if csv:
            save_to_csv(all_found_accounts, "emails_results")
        if pdf:
            save_to_pdf(all_found_accounts, "emails_results")
        save_to_txt(all_found_accounts, "found-result-emails")

    # Save all found accounts to PDF
    if all_found_accounts:
        save_to_pdf(all_found_accounts, "found-results")

if __name__ == "__main__":
    main()

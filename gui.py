import os
import argparse
import logging
import sys
import random
import requests
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from fpdf import FPDF
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import time
import csv

# Configuration
LOG_PATH = "logs/user_finder_zeta.log"
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.3 Safari/602.3.12",
]
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
    create_save_directory()  # Ensure the results directory exists
    filename = generate_unique_filename(base_filename, "csv")
    with open(f"results/{filename}", "w") as file:
        for line in data:
            file.write(line + "\n")

def save_to_txt(data, base_filename):
    create_save_directory()  # Ensure the results directory exists
    if data:  # Only save if there is data
        filename = generate_unique_filename(base_filename, "txt")
        with open(f"results/{filename}", "w") as file:
            for line in data:
                file.write(line + "\n")
        return filename
    return None

def save_to_pdf(data, base_filename):
    create_save_directory()  # Ensure the results directory exists
    if data:  # Only save if there is data
        filename = generate_unique_filename(base_filename, "pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in data:
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(f"results/{filename}")
        return filename
    return None

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

def verify_username(username, progress_callback=None):
    print(f"Verifying username: {username}")
    found_accounts = []
    headers = {"User-Agent": get_random_user_agent()}
    total_platforms = len(PLATFORMS)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(check_platform, platform, url, username, headers) for platform, url in PLATFORMS.items()]
        for index, future in enumerate(as_completed(futures)):
            result = future.result()
            if result:
                found_accounts.append(result)
            if progress_callback:
                progress = (index + 1) / total_platforms * 100
                progress_callback(progress)
    return found_accounts

def verify_email(email, progress_callback=None):
    print(f"Verifying email: {email}")
    found_accounts = []
    headers = {"User-Agent": get_random_user_agent()}
    total_platforms = len(EMAIL_PLATFORMS)
    hashed_email = hashlib.md5(email.encode()).hexdigest()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(check_platform, platform, url, hashed_email, headers) for platform, url in EMAIL_PLATFORMS.items()]
        for index, future in enumerate(as_completed(futures)):
            result = future.result()
            if result:
                found_accounts.append(result)
            if progress_callback:
                progress = (index + 1) / total_platforms * 100
                progress_callback(progress)
    return found_accounts

def run_tool(usernames, emails, permute, permuteall, progress_callback):
    all_found_accounts = []
    txt_filename = pdf_filename = None
    if usernames:
        for user in usernames:
            found_accounts = verify_username(user, progress_callback)
            if found_accounts:
                all_found_accounts.extend(found_accounts)
        if all_found_accounts:
            txt_filename = save_to_txt(all_found_accounts, "found-result-usernames")
            if txt_filename:
                pdf_filename = txt_filename.replace(".txt", ".pdf")
                save_to_pdf(all_found_accounts, pdf_filename)

    all_found_accounts = []  # Reset for email results
    if emails:
        for email in emails:
            found_accounts = verify_email(email, progress_callback)
            if found_accounts:
                all_found_accounts.extend(found_accounts)
        if all_found_accounts:
            txt_filename = save_to_txt(all_found_accounts, "found-result-emails")
            if txt_filename:
                pdf_filename = txt_filename.replace(".txt", ".pdf")
                save_to_pdf(all_found_accounts, pdf_filename)

    if txt_filename and pdf_filename:
        messagebox.showinfo("Info", f"Search completed successfully and results saved as {txt_filename} and {pdf_filename}.")
    else:
        messagebox.showinfo("Info", "No accounts found.")

def update_progress(progress):
    progress_var.set(progress)
    root.update_idletasks()

def start_search():
    usernames = [username.strip() for username in entry_usernames.get().split()]
    emails = [email.strip() for email in entry_emails.get().split()]
    permute = var_permute.get()
    permuteall = var_permuteall.get()
    progress_var.set(0)
    Thread(target=run_tool, args=(usernames, emails, permute, permuteall, update_progress)).start()

def main():
    global root, entry_usernames, entry_emails, var_permute, var_permuteall, progress_var
    root = tk.Tk()
    root.title("User Finder Zeta")

    tk.Label(root, text="Usernames (space-separated):").grid(row=0, column=0)
    entry_usernames = tk.Entry(root, width=50)
    entry_usernames.grid(row=0, column=1)

    tk.Label(root, text="Emails (space-separated):").grid(row=1, column=0)
    entry_emails = tk.Entry(root, width=50)
    entry_emails.grid(row=1, column=1)

    var_permute = tk.BooleanVar()
    tk.Checkbutton(root, text="Permute Usernames (strict)", variable=var_permute).grid(row=2, column=0, columnspan=2)

    var_permuteall = tk.BooleanVar()
    tk.Checkbutton(root, text="Permute Usernames (all)", variable=var_permuteall).grid(row=3, column=0, columnspan=2)

    tk.Button(root, text="Start Search", command=start_search).grid(row=4, column=0, columnspan=2)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, length=300, mode='determinate', variable=progress_var)
    progress_bar.grid(row=5, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()

import requests
from config import console, usernameFoundAccounts

class UsernameChecker:
    def __init__(self, username):
        self.username = username
        self.results = []

    def check_site(self, site_name, url, not_found_text):
        check = requests.get(url).text
        if not_found_text not in check:
            self.results.append(f"{site_name}: {url}")
            console.print(f"[green]Found![/green] {url}")
        else:
            console.print(f"[red]Not Found![/red] {site_name}")

    def run(self):
        self.check_site("Instagram", f"https://www.instagram.com/{self.username}", "The link you followed may be broken")
        self.check_site("Facebook", f"https://www.facebook.com/{self.username}", "not found")
        self.check_site("Twitter", f"https://www.twitter.com/{self.username}", "page doesn’t exist")
        self.check_site("YouTube", f"https://www.youtube.com/{self.username}", "Not Found")
        self.check_site("Blogger", f"https://{self.username}.blogspot.com", "HTTP/2 404")
        self.check_site("Reddit", f"https://www.reddit.com/user/{self.username}", "HTTP/2 404")
        self.check_site("WordPress", f"https://{self.username}.wordpress.com", "Do you want to register")
        self.check_site("Pinterest", f"https://www.pinterest.com/{self.username}", "?show_error")
        self.check_site("GitHub", f"https://www.github.com/{self.username}", "404 Not Found")
        self.check_site("Tumblr", f"https://{self.username}.tumblr.com", "HTTP/2 404")
        self.check_site("Flickr", f"https://www.flickr.com/people/{self.username}", "Not Found")
        self.check_site("Steam", f"https://steamcommunity.com/id/{self.username}", "The specified profile could not be found")
        self.check_site("Vimeo", f"https://vimeo.com/{self.username}", "404 Not Found")
        self.check_site("SoundCloud", f"https://soundcloud.com/{self.username}", "404 Not Found")
        self.check_site("Disqus", f"https://disqus.com/{self.username}", "404 NOT FOUND")
        self.check_site("Medium", f"https://medium.com/@{self.username}", "HTTP/2 404")
        self.check_site("DeviantART", f"https://{self.username}.deviantart.com", "HTTP/2 404")
        self.check_site("VK", f"https://vk.com/{self.username}", "HTTP/2 404")
        self.check_site("About.me", f"https://about.me/{self.username}", "HTTP/2 404")
        self.check_site("Imgur", f"https://imgur.com/user/{self.username}", "HTTP/2 404")
        self.check_site("Flipboard", f"https://flipboard.com/@{self.username}", "HTTP/2 404")
        self.check_site("SlideShare", f"https://slideshare.net/{self.username}", "HTTP/2 404")
        self.check_site("Fotolog", f"https://fotolog.com/{self.username}", "HTTP/2 404")
        self.check_site("Spotify", f"https://open.spotify.com/user/{self.username}", "HTTP/2 404")
        self.check_site("MixCloud", f"https://www.mixcloud.com/{self.username}", "error-message")
        self.check_site("Scribd", f"https://www.scribd.com/{self.username}", "show_404")
        self.check_site("Badoo", f"https://www.badoo.com/en/{self.username}", "404 Not Found")
        self.check_site("Patreon", f"https://www.patreon.com/{self.username}", "HTTP/2 404")
        self.check_site("BitBucket", f"https://bitbucket.org/{self.username}", "HTTP/2 404")
        self.check_site("DailyMotion", f"https://www.dailymotion.com/{self.username}", "404 Not Found")
        self.check_site("Etsy", f"https://www.etsy.com/shop/{self.username}", "HTTP/2 404")
        self.check_site("CashMe", f"https://cash.me/{self.username}", "404 Not Found")
        self.check_site("Behance", f"https://www.behance.net/{self.username}", "404 Not Found")
        self.check_site("GoodReads", f"https://www.goodreads.com/{self.username}", "404 Not Found")
        self.check_site("Instructables", f"https://www.instructables.com/member/{self.username}", "404 NOT FOUND")
        self.check_site("Keybase", f"https://keybase.io/{self.username}", "404 Not Found")
        self.check_site("Kongregate", f"https://kongregate.com/accounts/{self.username}", "404 Not Found")
        self.check_site("LiveJournal", f"https://{self.username}.livejournal.com", "404 Not Found")
        self.check_site("AngelList", f"https://angel.co/{self.username}", "404 Not Found")
        self.check_site("Last.fm", f"https://last.fm/user/{self.username}", "HTTP/2 404")
        self.check_site("Dribbble", f"https://dribbble.com/{self.username}", "HTTP/2 404")
        self.check_site("Codecademy", f"https://www.codecademy.com/{self.username}", "HTTP/2 404")
        self.check_site("Gravatar", f"https://en.gravatar.com/{self.username}", "HTTP/2 404")
        self.check_site("Pastebin", f"https://pastebin.com/u/{self.username}", "location: /index")
        self.check_site("Foursquare", f"https://foursquare.com/{self.username}", "404 Not Found")
        self.check_site("Roblox", f"https://www.roblox.com/user.aspx?username={self.username}", "404 Not Found")
        self.check_site("Gumroad", f"https://www.gumroad.com/{self.username}", "404 Not Found")
        self.check_site("Newgrounds", f"https://{self.username}.newgrounds.com", "HTTP/2 404")
        self.check_site("Wattpad", f"https://www.wattpad.com/user/{self.username}", "HTTP/2 404")
        self.check_site("Canva", f"https://www.canva.com/{self.username}", "HTTP/2 404")
        self.check_site("CreativeMarket", f"https://creativemarket.com/{self.username}", "404eef72")
        self.check_site("Trakt", f"https://www.trakt.tv/users/{self.username}", "HTTP/2 404")
        self.check_site("500px", f"https://500px.com/{self.username}", "404 Not Found")
        self.check_site("Buzzfeed", f"https://buzzfeed.com/{self.username}", "HTTP/2 404")
        self.check_site("TripAdvisor", f"https://tripadvisor.com/members/{self.username}", "HTTP/2 404")
        self.check_site("HubPages", f"https://{self.username}.hubpages.com", "HTTP/2 404")
        self.check_site("Contently", f"https://{self.username}.contently.com", "404 Not Found")
        self.check_site("Houzz", f"https://houzz.com/user/{self.username}", "an error has occurred")
        self.check_site("blip.fm", f"https://blip.fm/{self.username}", "404 Not Found")
        self.check_site("Wikipedia", f"https://www.wikipedia.org/wiki/User:{self.username}", "HTTP/2 404")
        self.check_site("HackerNews", f"https://news.ycombinator.com/user?id={self.username}", "No such user")
        self.check_site("CodeMentor", f"https://www.codementor.io/{self.username}", "HTTP/2 404")
        self.check_site("ReverbNation", f"https://www.reverbnation.com/{self.username}", "HTTP/2 404")
        self.check_site("Designspiration", f"https://www.designspiration.net/{self.username}", "HTTP/2 404")
        self.check_site("Bandcamp", f"https://www.bandcamp.com/{self.username}", "HTTP/2 404")
        self.check_site("ColourLovers", f"https://www.colourlovers.com/love/{self.username}", "HTTP/2 404")
        self.check_site("IFTTT", f"https://www.ifttt.com/p/{self.username}", "HTTP/2 404")
        self.check_site("Ebay", f"https://www.ebay.com/usr/{self.username}", "HTTP/2 404")
        self.check_site("Slack", f"https://{self.username}.slack.com", "HTTP/2 404")
        self.check_site("OkCupid", f"https://www.okcupid.com/profile/{self.username}", "HTTP/2 404")
        self.check_site("Trip", f"https://www.trip.skyscanner.com/user/{self.username}", "HTTP/2 404")
        self.check_site("Ello", f"https://ello.co/{self.username}", "HTTP/2 404")
        self.check_site("Tracky", f"https://tracky.com/user/{self.username}", "profile:username")
        self.check_site("Tripit", f"https://www.tripit.com/people/{self.username}#/profile/basic-info", "location: https://www.tripit.com/home")
        self.check_site("Basecamp", f"https://{self.username}.basecamphq.com/login", "HTTP/2 404")
        
        if self.results:
            usernameFoundAccounts = self.results

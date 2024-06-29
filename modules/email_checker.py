import requests
from config import console, emailFoundAccounts

class EmailChecker:
    def __init__(self, email):
        self.email = email
        self.results = []

    def check_site(self, site_name, url, not_found_text):
        check = requests.get(url).text
        if not_found_text not in check:
            self.results.append(f"{site_name}: {url}")
            console.print(f"[green]Found![/green] {url}")
        else:
            console.print(f"[red]Not Found![/red] {site_name}")

    def run(self):
        # Implement email checking on various platforms
        # Similar to UsernameChecker but with email checks
        pass
        
        if self.results:
            emailFoundAccounts = self.results

import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
from googlesearch import search
import random
import heapq  # For priority queue
from urllib.parse import urljoin


class WebCrawler:
    def __init__(self, keyword):
        self.keyword = keyword.lower()
        self.visited = set()
        self.queue = []  # Priority Queue (score, URL)

    # Getting 100 initial links from google
    def get_google_results(self, query):
        urls = []
        # Getting 1000 websites
        for url in search(query, 20):
            urls.append(url)

        # Pick 100 websites randomly instead of first 100 websites
        random.shuffle(urls)
        
        # Save the links to a file
        with open("links.txt", "w", encoding="utf-8") as f:
            for url in urls[:100]:
                f.write(url + "\n")

        print("Found 100 links and save in initial_links.txt")
        return urls[:100]
    
    # another search engine
    # Note: Since I made requests to many on google search, they currently put me on cooldown for requesting,
    #       so I'm using duckduckgo as an alternative to do this assignment.
    def get_duckduckgo_results(self, query):
        urls = []
        with DDGS() as ddgs:
            for url in ddgs.text(query, 20):
                urls.append(url['href'])

            
        # Save the links to a file
        with open("initial_links.txt", "w", encoding="utf-8") as f:
            for url in urls:
                f.write("inital url: " + url + "\n")

        print("Found 100 links and save in initial_links.txt")
        return urls
    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None
        
    # Find all relevant links in the html
    def extract_links(self, html, url):
        if not html:
            return []  # Return an empty list instead of None
        
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        # check for links with absolute path and relative path
        for link in soup.find_all('a', href=True):
            path = link.get('href')
            if path.startswith('/'):
                path = urljoin(url, path)
            elif not path.startswith('http'):
                continue  # Ignore invalid links
            links.append(path)

        return links
    
    # return percentage of keywords appear in overall words in webpage
    def calculate_score(self, text):
        key_words = text.lower().count(self.keyword)
        total_words = len(text.split())
        return  key_words / total_words 

    # Crawling function
    def crawl(self):
        pages_downloaded = 0

        # Seed URLs
        for url in self.get_duckduckgo_results(self.keyword):
            heapq.heappush(self.queue, (-1, url))  # Seed URLs get score 1 (highest priority)

        # while queue is not empty and pages downloaded is less 100 if crawling
        while self.queue and pages_downloaded < 100:
            _, url = heapq.heappop(self.queue)
            
            # Check if the links already exist in the Queue or have been visited before 
            if url in self.visited:
                continue

            # Add the web need to be visit
            print(f"[+] Visiting: {url}")
            self.visited.add(url)
            
            # Get page in text which will be later use to convert into html
            html = self.fetch_page(url)
            

            if html:
                # filter the relevant links only (use keyword matching) 
                if self.keyword in html.lower():
                    pages_downloaded += 1
                    
                    # Write as the html file
                    with open(f"page_{pages_downloaded}.html", "w", encoding="utf-8") as f:
                        f.write(html)
                        
                    # Add the downloaded link to the file
                    with open("links.txt", "a", encoding="utf-8") as f:
                        f.write("downloaded url: " + url + "\n")
                            
                    # Extract links and assign scores
                    for link in self.extract_links(html, url):
                        # if the links not visited put in the queue 
                        if link not in self.visited:
                            score = self.calculate_score(html)
                            heapq.heappush(self.queue, (-score, link))

        print(f"Crawl finished. {pages_downloaded} pages downloaded.")

if __name__ == "__main__":
    user_query = input("Enter your search query: ")
    keyword=user_query
    crawler = WebCrawler(keyword)
    crawler.crawl()
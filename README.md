A Python web crawler that searches and downloads web pages based on a given keyword using Google and DuckDuckGo.

Features
    
Retrieves 100 random links from search results.
  
Extracts and scores pages based on keyword relevance.
Downloads up to 100 relevant web pages.

Requirements: use "pip install requests duckduckgo-search beautifulsoup4 googlesearch-python"
    
requests
duckduckgo-search
beautifulsoup4
googlesearch-python

Run: 
    python webcrawler.py

Notes
    
Uses DuckDuckGo as an alternative if Google search is rate-limited. (Google only allow 1000 requests a day)
Prioritizes pages with higher keyword density.

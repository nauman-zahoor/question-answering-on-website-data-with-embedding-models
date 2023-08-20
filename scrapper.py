
import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import pickle


# User-Agent Spoofing
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

headers = {'User-Agent': user_agent}


# Rate Limiting
def random_delay():
    sleep(randint(1, 4))  # Simulate human-like behavior

# Parse HTML
def parse_html(url):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

# Pagination and Crawling
def crawl_pages(start_url,document_links):
    depth=100000000
    visited_urls = set()
    to_visit = [start_url]
    ix=0

    while to_visit and depth > 0:
        current_url = to_visit.pop(0)
        if current_url in visited_urls:
            continue
        print(' current_url: ',current_url, ' visited_urls: ',len(visited_urls), ' to_visit: ',len(to_visit), 'document_links: ', len(document_links) )
        
        if ('.pdf' in current_url )or ('doc' in current_url) or ('docx' in current_url) or ('ppt' in current_url) or( 'pptx' in current_url):
            document_links.append(current_url)
            with open('document_links.pkl', 'wb') as pickle_file:
                pickle.dump(document_links, pickle_file)
            continue
            
        
        soup = parse_html(current_url)
        visited_urls.add(current_url)
        depth -= 1

        # Extract data or perform actions here
        page_text = soup.get_text()
        save_to_file(current_url, page_text,ix)
        ix=ix+1

        # Find and add links to to_visit list
        links = [link.get('href') for link in soup.find_all('a', href=True)]
        for link in links:
            if link.startswith('/'):
                link = target_domain + link
            if link.startswith(target_domain) and link not in visited_urls:
                to_visit.append(link)

        random_delay() 

# Step 10: Data Extraction

# Save page text to a file
def save_to_file(url, content,ix):
    filename = url.replace('/', '_') +str(ix) +'.txt'
    filename = filename.replace('/', '_')
    filename = filename.replace(':', '_')
    filename = "text/" + domain + "/"+ filename
    #print(filename)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Start crawling

target_domain = "http://example.com"
domain = 'example.com' 
pdf_links = []

crawl_pages(target_domain,document_links)
print(len(document_links))
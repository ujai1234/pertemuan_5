from collections import deque
import re
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

# Input the starting URL
user_url = str(input("[+] Masukan url: "))
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0

try:
    while True:
        count += 1
        if count > 10:
            break
        
        # Get the next URL from the queue
        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = f'{parts.scheme}://{parts.netloc}'
        path = url[:url.rfind('/')] + '/' if '/' in parts.path else url
        
        print(f'{count} Memproses {url}')

        try:
            # Request the URL
            response = requests.get(url)
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"[-] Error fetching {url}: {e}")
            continue

        # Find emails in the page content
        new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@[a-z\.\-]+\.[a-z]+', response.text, re.I))
        emails.update(new_emails)

        # Parse the HTML content and extract links
        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all('a'):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            link = urllib.parse.urljoin(base_url, link)  # Use urljoin for more robust normalization
            
            # Add new links to the queue if they haven't been processed
            if not link in urls and not link in scraped_urls:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Closing!')
    
print('\n Proses Selesai!')
print(f'\n Ditemukan {len(emails)} email ditemukan \n')

# Print out the found emails
for mail in emails:
    print(f'- {mail}')

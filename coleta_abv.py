import requests
from bs4 import BeautifulSoup

url = "https://www.ebullient.dev/projects/ttrpg-convert-cli/docs/sourceMap.html?utm_source=chatgpt.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                  }
response = requests.get(url, timeout=20, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

for tr in soup.find_all('tr'):
    print(tr.find('td').text if tr.find('td') else "")
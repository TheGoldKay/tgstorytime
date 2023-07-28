from bs4 import BeautifulSoup as bs 
import requests

tg = "https://www.tgstorytime.com/search.php?searchtype=advanced&catid=-1&formname=search&wordlow=-500&wordhigh=1000000&sortorder=alpha&offset=0"

response = requests.get(tg)
html_content = response.text
soup = bs(html_content, 'html.parser')

odd_list = soup.find_all('div', class_='listbox odd')
even_list = soup.find_all('div', class_='listbox even')
"""
for div in odd_list:
    print(div.get_text())
"""

print(even_list[-1].get_text())
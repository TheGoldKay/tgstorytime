from bs4 import BeautifulSoup 
import requests 
import warnings
from bs4 import UserWarning
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def chapters(url):
    chapter_count = 0
    res = requests.get(url)
    html = res.content 
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all('div', {'class': 'bigblock'})
    try:
        error_div = soup.find('div', class_='errormsg')
        if error_div:
            error_message = error_div.get_text(strip=True)
            print("Error message:", error_message)
    except Exception as e:
        print("Error occurred while parsing error message:", e)

    

url = "https://www.tgstorytime.com/viewstory.php?sid=7332"
chapters(url)
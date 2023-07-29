from bs4 import BeautifulSoup as bs 
import requests
import os

page = 0
tg = "https://www.tgstorytime.com/search.php?searchtype=advanced&catid=-1&formname=search&wordlow=-500&wordhigh=1000000&sortorder=alpha&offset="
stories = []
i = 0
done = False 
while(not done):
    try:
        url = tg + str(page)
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
        else:
            print("Error: Unable to fetch the webpage.")
            exit()
        soup = bs(html_content, 'html.parser')
        odd_list = list(soup.find_all('div', class_='listbox odd'))
        stories.extend(odd_list)
        even_list = list(soup.find_all('div', class_='listbox even'))
        stories.extend(even_list)
        os.system('clear')
        if(not odd_list or not even_list):
            print("It's Done\n")
            done = True 
        else:
            i += 1
            page += 127
            print(f"Pages scraped: {i}")
    except Exception as e:
        print(f"Error: {e}")
        exit()

print(f"Number of stories: {len(stories)} || Pages: {i}")
"""for story in stories:
    title = story.find_all('div', class_ = 'title')[1]
    print(title.get_text())
"""  
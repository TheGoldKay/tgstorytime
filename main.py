from bs4 import BeautifulSoup as bs 
import requests
import os
import re

tg = "https://www.tgstorytime.com/browse.php?type=titles&offset={}"
stories = []
page = 0
i = 0
done = False 

def get_story_data(page_stories):
    # some data processing
    for story_div in page_stories:
        story = story_div.find_all('div', class_='title')[1] # there are two instances of the 'title' div class
        summary = story_div.find('div', class_='summarytext')
        title_author = story.find_all('a') # there are two links, one for the story and one for the author page
        title, author = title_author[0], title_author[1]
        title_link, author_link = title.get('href'), author.get('href')
        if(title_link.startswith('javascript')):
            url_pattern = r"location = '([^']+)'"
            title_link = re.search(url_pattern, title_link).group(1)
        title_link = "www.tgstorytime.com/" + title_link
        author_link = "www.tgstorytime.com/" + author_link
        data = {
            "title": title.get_text(),
            "author": author.get_text(),
            "summary": summary.get_text(),
            "story_link": title_link,
            "author_link": author_link
        }
        stories.append(data)
        #print(f"Title: {title.get_text()}\nAuthor: {author.get_text()}\nSummary: {summary.get_text()}")
        #print(f"Story URL: {title_link} || Author URL Page: {author_link}")
        
while(not done):
    try:
        #url = tg + str(page)
        url = tg.format(page)
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
        else:
            print("Error: Unable to fetch the webpage.")
            exit()
        soup = bs(html_content, 'html.parser')
        page_stories = list(soup.find_all('div', class_='listboxtop'))
        os.system('clear')
        if(not page_stories):
            print("It's Done\n")
            done = True 
        else:
            i += 1
            page += 127
            print(f"Pages scraped: {i}")
        done = True # do the first page <<< FOR TESTING ONLY >>>
        get_story_data(page_stories)
    except Exception as e:
        print(f"Error: {e}")
        exit()

print(f"Number of stories: {len(stories)} || Pages: {i}\n")
print(stories[-1])
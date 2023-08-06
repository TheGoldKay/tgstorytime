from bs4 import BeautifulSoup
import requests
import os
import re
from get_novels import save_data

tg = "https://www.tgstorytime.com/browse.php?type=titles&offset={}"
stories = []
count = 0

def get_story_content(link):
    ch = 1
    url = link + "&textsize=0&chapter="
    text = []
    done = False 
    while (not done):
        res = requests.get(url + str(ch))
        html = res.content 
        soup = BeautifulSoup(html, 'html.parser')
        story_div = soup.find('div', id='story')
        txt_with_newlines = story_div.get_text(separator='\n')  # Get text content with newlines
        txt = txt_with_newlines.replace('\xa0', ' ')  # Replace non-breaking spaces with regular spaces
        if(txt == ''):
            done = True 
        else:
            text.append(txt)
            ch += 1
    return text 
    

def get_story_data(page_stories):
    global count
    # some data processing
    for story_div in page_stories:
        story = story_div.find_all('div', class_='title')[1] # there are two instances of the 'title' div class
        summary = story_div.find('div', class_='summarytext')
        title_author = story.find_all('a') # there are two links, one for the story and one for the author page
        title, author = title_author[0], title_author[1]
        title_link, author_link = title.get('href'), author.get('href')
        # if the story has any warnings js will raise a red flag
        if(title_link.startswith('javascript')):
            url_pattern = r"location = '([^']+)'"
            title_link = re.search(url_pattern, title_link).group(1)
        title_link = "https://www.tgstorytime.com/" + title_link
        author_link = "https://www.tgstorytime.com/" + author_link
        data = {
            "title": title.get_text(),
            "author": author.get_text(),
            "summary": summary.get_text(),
            "story_link": title_link,
            "author_link": author_link
        }
        count += 1
        save_data(data)
        #data["text"] = get_story_content(title_link)
        #stories.append(data)
        #save_story(data)
        #print(f"Story: {data['title']} || Count: {count}")
        #print(f"Title: {title.get_text()}\nAuthor: {author.get_text()}\nSummary: {summary.get_text()}")
        #print(f"Story URL: {title_link} || Author URL Page: {author_link}")
        ###########break # do the first story <<< FOR TESTING ONLY >>>

def save_story(story):
    folder = f"data/{story['title']}"
    os.mkdir(folder) # story's directory
    with open(f"{folder}/summary.txt", 'w') as file:
        file.write(story["summary"])
    for i, chapter in enumerate(story["text"], 1):
        with open(f"{folder}/{i}.txt", 'w') as file:
            file.write(chapter)
    
def make_data_dir(dir_name="data"):
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        os.system("rm -rf data")
        os.mkdir(dir_name)
    except OSError as e:
        print(f"Error: {e}")
        
def main():
    done = False 
    page = 4699
    i = 0
    #make_data_dir()
    while(not done):
        try:
            url = tg.format(page)
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.content
            else:
                print("Error: Unable to fetch the webpage.")
                exit()
            soup = BeautifulSoup(html_content, 'html.parser')
            page_stories = list(soup.find_all('div', class_='listboxtop'))
            #os.system('clear')
            if(not page_stories):
                print("It's Done\n")
                done = True 
            else:
                i += 1
                page -= 127
                print(f"Pages Id: {page}")
            get_story_data(page_stories)
            #########done = True # do the first page <<< FOR TESTING ONLY >>>
        except Exception as e:
            print(f"Error: {e}")
            exit()
main()
#print(f"Number of stories: {len(stories)} || Pages: {i}\n")
#print(stories[-1])
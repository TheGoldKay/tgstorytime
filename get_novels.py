from bs4 import BeautifulSoup 
import requests 
import os
import secrets
import string

# Define the characters to use for the random ID
allowed_characters = string.ascii_letters + string.digits  # You can add more characters if needed.

site = "https://www.tgstorytime.com/{}"

def get_id():
    # Set the desired length of the random ID
    id_length = 5  # You can choose any length you prefer.
    # Generate a random ID
    random_id = ''.join(secrets.choice(allowed_characters) for _ in range(id_length))
    return random_id

def save_data(data):
    url = data['story_link']
    res = requests.get(url)
    html = res.content 
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all('a', href=True)
    for div in content:
        txt = div.get_text()
        #print(txt)
        if(txt == "Download ePub" or txt == "Story"):
            href = div.get('href')
            link = site.format(href)
            res = requests.get(link)
            if res.status_code == 200:
                title = href.split('/')[-1]
                dir_name = data['title'].replace('/', '-')
                try:
                    os.mkdir(f"data/{dir_name}")
                    with open(f"data/{dir_name}/summary.txt", 'w') as file:
                        file.write(data['summary'])
                    with open(f"data/{dir_name}/url.txt", 'w') as file:
                        file.write(f"Story Link: {data['story_link']}\n")
                        file.write(f"Author Link: {data['author_link']}\n")
                    with open(f"data/{dir_name}/{title}", 'wb') as file:
                        file.write(res.content)
                        #print(f"----------------> {title}")
                except FileExistsError:
                    #print("******************** FILE ALREADY EXISTS *****************************")
                    pass
            else:
                print(">-------- Failure! -----------<")
                print(data)
                print(">-------- Failure! -----------<")

#url = "https://www.tgstorytime.com/viewstory.php?sid=7381"
#chapters(url)
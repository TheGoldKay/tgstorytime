from bs4 import BeautifulSoup 
import requests 

site = "https://www.tgstorytime.com/{}"

def save_data(data):
    url = data['story_link']
    res = requests.get(url)
    html = res.content 
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all('a')
    for div in content:
        txt = div.get_text()
        #print(txt)
        if(txt == "Download ePub" or txt == "Story"):
            href = div.get('href')
            link = site.format(href)
            res = requests.get(link)
            if res.status_code == 200:
                title = href.split('/')[-1]
                with open(f"data/{str(title)}", 'wb') as file:
                    file.write(res.content)
                    print(f"----------------> {title}")
            else:
                print(">-------- Failure! -----------<")
                print(data)
                print(">-------- Failure! -----------<")

#url = "https://www.tgstorytime.com/viewstory.php?sid=7381"
#chapters(url)
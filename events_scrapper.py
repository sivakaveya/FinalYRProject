from bs4 import BeautifulSoup
import requests

from datetime import datetime
class ExEvent:
    def __init__(self, name, detail, url, image, date,loc):
        self.name = name
        self.detail = detail
        self.url = url
        self.image = image
        self.date = date

        self.loc=loc


    def __str__(self):
        return self.name + '<br/> ' + str(self.detail) + '<br/> ' + self.url + '<br/>' + self.image + '<br/>' + self.date

def knowafest():
    URL = "https://www.knowafest.com/explore/events"
    page = requests.get(URL).text
    soup = BeautifulSoup(page, 'lxml')
    results = soup.find_all("a", class_="card card-ghost card-transition-zoom h-100")
    
    items = []

    for result in results:
        name = result.find('span', class_= 'badge bg-dark text-white card-pinned-top-end').text
        detail = result.find('p', class_= 'card-text').text 

    i=0
    for result in results:
        # i+=1
        #print(i)
        #print(result)
        name = result.find('span', class_= 'badge bg-dark text-white card-pinned-top-end').text
        detail = result.find('p', class_= 'card-text').text 
        #print(detail)

        image = result.find('img', class_='card-img').attrs['src']
        url="https://www.knowafest.com/explore/" + result.attrs['href']
        loc= result.find('p').text.split()[0]
        date=result.find('span', class_= 'fs-6 fw-bold text-primary').text

        date=date.replace('-', '')
        #print(date)
        #print(datetime.strptime(date, "%y-%m-%d"))
        items.append(ExEvent(name, detail, url, image, date,loc))

    return items
    

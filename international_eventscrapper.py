from bs4 import BeautifulSoup
import requests

class InternationalEvent:
    def __init__(self, name, detail, url, image, date):
        self.name = name
        self.detail = detail
        self.url = url
        self.image = image
        self.date = date

    def __str__(self):
        return self.name + '<br/> ' + str(self.detail) + '<br/> ' + self.url + '<br/>' + self.image + '<br/>' + self.date

def int_event(domain='0'):
    if domain=='0':
        URL = "https://10times.com/top100/technology"
    else:
        URL = "https://10times.com/top100/"+domain.lower().replace(' ','-')
    page = requests.get(URL).text
    soup = BeautifulSoup(page, 'lxml')
    results = soup.find_all("tr", class_="align-middle top100-event")
    # print(results)
    items = []
    for result in results:
        name = result.find('span', class_= 'line-2').text
        try:
            detail = result.find('div', class_= 'small text-orange').text 
        except:
            detail='International top events'
        image='default'
        url="https://10times.com/top100/technology/" + result.find('a',class_='text-decoration-none me-2').attrs['href']
        date=result.find('div', class_= 'text-muted').text
        items.append(InternationalEvent(name, detail, url, image, date))
    # print(items)
    return items


# int_event('Cyber Security')
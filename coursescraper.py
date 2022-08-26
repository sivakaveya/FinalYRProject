from bs4 import BeautifulSoup
import requests

class Course:
    def __init__(self, name, detail, url, image, site):
        self.name = name
        self.detail = detail
        self.url = url
        self.image = image
        self.site = site

    def __str__(self):
        return self.name + '<br/> ' + str(self.detail) + '<br/> ' + self.url + '<br/>' + self.image + '<br/>' + self.site

def scrimba(domain):
    if domain=='Web Developement':
        URL = "https://scrimba.com/allcourses?price=free"
        page = requests.get(URL).text
        soup = BeautifulSoup(page, 'lxml')
        results = soup.find_all("a", class_="n-ah card n_af")
        # print(results)
        items = []
        for result in results:
            # print(result)
            name = result.find('span', class_= 's-ai heading').text
            detail = result.find('div', class_= 'n-al small n_af').text #+result.find('div', class_= 'n-am n_af')
            image = "default image"
            url="https://scrimba.com" + result.attrs['href']
            items.append(Course(name, detail, url, image, 'https://scrimba.com'))
            # print(name, detail, url, image)
        return items
    else:
        return []
        

def codecademy(domain):
    if domain=='Computer Science':
        URL = "https://www.codecademy.com/catalog/subject/computer-science"
        URL1 = "https://www.codecademy.com/catalog/subject/cyber-security"
    elif domain=='Machine Learning' or domain=='Artificial Intelligence':
        URL = "https://www.codecademy.com/catalog/subject/machine-learning"
        URL1 = "https://www.codecademy.com/catalog/subject/data-science"
    elif domain=='Web Developement':
        URL = "https://www.codecademy.com/catalog/subject/web-development"
        URL1 = "https://www.codecademy.com/catalog/subject/mobile-development"
    elif domain=='Data Science':
        URL = "https://www.codecademy.com/catalog/language/"+domain.lower().replace(' ','-')
        URL1 = "https://www.codecademy.com/catalog/subject/data-visualization"
    else:
        URL = "https://www.codecademy.com/catalog/language/"+domain.lower().replace(' ','-')
        URL1 = "https://www.codecademy.com/catalog/subject/"+domain.lower().replace(' ','-')
    page = requests.get(URL).text
    page1 =  requests.get(URL1).text
    soup = BeautifulSoup(page, 'lxml')
    soup1 = BeautifulSoup(page1, 'lxml')
    #bhai livk chahiye toh a use karlena ...scarpper was working
    results = soup.find_all("a", class_="e14vpv2g1 gamut-1x28z2k-ResetElement-Anchor-AnchorBase e1bhhzie0")
    results1 = soup1.find_all("a", class_="e14vpv2g1 gamut-1snn8i9-ResetElement-Anchor-AnchorBase e1bhhzie0")
    # print(results)
    items = []
    for result in results:
        # print(result)
        # print()
        name = result.find('h3', class_= 'gamut-19g9xb9-Text e8i0p5k0').text
        detail = result.find('div', class_= 'gamut-17tfmc2-FlexBox e1tc6bzh0').text 
        image = "default image"
        url="https://www.codecademy.com" + result.attrs['href']
        items.append(Course(name, detail, url, image, 'www.codecademy.com'))
        # print(name, detail, url, image)
    for result1 in results1:
        # print(result)
        # print()
        name = result1.find('h3', class_= 'gamut-19g9xb9-Text e8i0p5k0').text
        detail = result1.find('div', class_= 'gamut-17tfmc2-FlexBox e1tc6bzh0').text 
        image = "default image1"
        url="https://www.codecademy.com" + result1.attrs['href']
        items.append(Course(name, detail, url, image, 'www.codecademy.com'))
        # print(name, detail, url, image)
    return items

def edx(domain):
    if domain=='Computer Science':
        URL = "https://www.edx.org/search?q=computer%20science&tab=course"
        URL1 = "https://www.edx.org/search?q=programming&tab=course"
    elif domain=='Machine Learning' or domain=='Artificial Intelligence':
        URL = "https://www.edx.org/search?q=machine%20learning&tab=course"
        URL1 = "https://www.edx.org/search?q=data%20science&tab=course"
    elif domain=='Web Developement':
        URL = "https://www.edx.org/search?q=web%20development&tab=course"
        URL1 = "https://www.edx.org/search?q=mobile%20app%20development&tab=course"
    elif domain=='Data Science':
        URL = "https://www.edx.org/search?q=business&tab=course"
        URL1 = "https://www.edx.org/search?q=data%20visualization&tab=course"
    else:
        URL = "https://www.edx.org/search?q="+domain.lower().replace(' ','%20')+"&tab=course"
        URL1 = "https://www.edx.org/search?q="+domain.lower().replace(' ','%20')+"&tab=course"
    
    page = requests.get(URL).text
    soup = BeautifulSoup(page, 'lxml')
    page1 = requests.get(URL1).text
    soup1 = BeautifulSoup(page1, 'lxml')
    #bhai livk chahiye toh a use karlena ...scarpper was working
    results = soup.find_all("a", class_="discovery-card-link bg-white text-black")
    results1 = soup1.find_all("a", class_="discovery-card-link bg-white text-black")
    # print(results)
    items = []
    for result in results:
        # print(result)
        # print()
        name = result.find('div', class_= 'd-card-body pl-4 pt-4 mt-2').text 
        detail = 'Edx Course'
        image = 'default'
        url="https://www.edx.org" + result.attrs['href']
        print(name)
        items.append(Course(name, detail, url, image, 'www.edx.org'))
        
    for result1 in results1:
        # print(result)
        # print()
        name = result1.find('div', class_= 'd-card-body pl-4 pt-4 mt-2').text 
        detail = 'Edx Course'
        image = 'default'
        url="https://www.edx.org" + result1.attrs['href']
        items.append(Course(name, detail, url, image, 'www.edx.org'))
    return items
        

def courses(domain):
    if domain=='Computer Science':
        URL = "https://www.courses.com/computer-science"
    elif domain=='Machine Learning' or domain=='Artificial Intelligence':
        URL = "https://www.courses.com/artificial-intelligence"
    elif domain=='Web Developement':
        URL = "https://www.courses.com/programming"
    else:
        URL = "https://www.courses.com/"+domain.lower().replace(' ','-')
    page = requests.get(URL).text
    soup = BeautifulSoup(page, 'lxml')
    #bhai livk chahiye toh a use karlena ...scarpper was working
    results = soup.find_all("div", class_="course")
    # print(results)
    items = []
    for result in results:
        # print(result)
        # print()
        name = result.find('h4').text
        try:
            detail = result.find('p').text
        except Exception as e:
            detail = 'Course from www.courses.com'
        image = "default image"
        url="https://www.courses.com" + result.find('h4').find('a').attrs['href']
        items.append(Course(name, detail, url, image, 'www.courses.com'))
    return items


def scrapallcourse(domain):
    items = []
    items += scrimba(domain)
    items += courses(domain)
    # items += codecademy(domain)
    # items += edx(domain)
    
    return items

# if __name__=='__main__':
#     print(scrimba('Machine Learning'))
#     print(codecademy('Machine Learning'))
#     print(edx('Machine Learning'))
#     print(courses('Machine Learning'))
#     print(futurelearn('Machine Learning'))

# print(scrapallcourse('cmpn'))
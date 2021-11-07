from bs4 import BeautifulSoup
from bs4 import Comment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from sys import platform
import os
if platform == "linux" or platform == "linux2":
    from pyvirtualdisplay import Display

"""
Courtesy from scraper.ipynb by Bhavya
"""


# pip install bs4 selenium
class JavaScript_scrape():
    """
    scrapping javascript based website,
    extracting the url, abstract, and title for all websites
    """

    def __init__(self):
        """
        generate search links
        :param query:
            search keywords
        :type  query:
            `unicode`
        :param source_weight:
            source priority
        :type  source_weight:
            `float`
        """

    def get_js_soup(self, url):
        """
        uses webdriver object to  generate the first 10 results ( first page)
        execute javascript code and
        get dynamically loaded webcontent
        """
        # create a webdriver object and set options for headless browsing
        options = Options()
        options.headless = True
        options.page_load_strategy = 'eager'

        #skip information that's only valuable for human beings
        prefs = {"profile.managed_default_content_settings.images":2,
         "profile.default_content_setting_values.notifications":2,
         "profile.managed_default_content_settings.stylesheets":2,
         "profile.managed_default_content_settings.cookies":2,
         "profile.managed_default_content_settings.javascript":1,
         "profile.managed_default_content_settings.plugins":1,
         "profile.managed_default_content_settings.popups":2,
         "profile.managed_default_content_settings.geolocation":2,
         "profile.managed_default_content_settings.media_stream":2,
        }
        options.add_experimental_option("prefs",prefs)

        #chrome driver version and system
        driver_version = "95.0.4638.54"
        driver_os = ""

        if platform == "linux" or platform == "linux2":
            # linux
            driver_os = "linux"

            #added for cloud containers
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        elif platform == "darwin":
            # OS X
            driver_os = "mac"
        elif platform == "win32":
            # Windows...
            driver_os = "windows"

        #start a display if the system is linux
        display = None
        if platform == "linux" or platform == "linux2":
            display = Display(visible=0, size=(800, 800))  
            display.start()

        driver = webdriver.Chrome(f'./chromedriver' + '-' + driver_version + '-' + driver_os, options=options)
        driver.get(url)
        res_html = driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(res_html, 'html.parser')  # beautiful soup object to be used for parsing html content
        driver.quit()

        #close the display if the system is linux
        if platform == "linux" or platform == "linux2":
            display.stop()
            
        return soup


    def scrape_medicalNewsToday(self, limit=5):
        """
        extracts the title, url, and abstract for upToDate
        """
        news_links = []
        base_url = 'https://www.medicalnewstoday.com/'

        # scrape to find news links in the base url
        soup = self.get_js_soup(base_url)

        for i, link_holder in enumerate(soup.find_all('figure',class_='css-ymgzhk')):
            links = link_holder.find('a')['href'] #get url
            news_links.append(links) 

            if i+1 >= limit:
                break


        print('Found Medical News Today Links', len(news_links))

        articles = []
        # scrape articles
        for link in news_links:
            #url returned is relative, so we need to add base url
            soup = self.get_js_soup(base_url+link)
            article = ""

            #get div that contains the article
            article_holder = soup.find('div', class_='css-z468a2')

            if article_holder == None:
                continue 

            #get article titles
            if article_holder.find('h1') != None:
                article+= article_holder.find('h1').text + '\n'

            #get paragraphs
            for p_holder in article_holder.find_all('p'):
                if p_holder != None:
                    article+= p_holder.text + '\n'
            
            if len(article) > 0:
                articles.append(article)

        return articles

    def scrape_aapNews(self, limit=5):
        """
        extracts the title, url, and abstract for upToDate
        """
        news_links = []
        news_url = 'https://www.aappublications.org/news'
        base_url = 'https://www.aappublications.org/'

        # scrape to find news links in the base url
        soup = self.get_js_soup(news_url)

        for i, link_holder in enumerate(soup.find_all('div',class_='highwire-cite-highwire-news-story')):
            if link_holder != None:
                links = link_holder.find('a')['href'] #get url
                news_links.append(links) 
            
            if i+1 >= limit:
                break

        print('Found AAP News Links', len(news_links))
        print(news_links)
        articles = []

        # scrape articles
        for link in news_links:
            #url returned is relative, so we need to add base url
            soup = self.get_js_soup(base_url+link)
            article = ""
            print(base_url+link)

            #get div that contains the article
            article_holder = soup.find('div', class_='panel-display panels-960-layout jcore-2col-layout')

            if article_holder == None:
                continue 

            #get article titles
            title_holder = article_holder.find('div', {"id": "page-title"})
            if title_holder != None and title_holder.find('span') != None:
                article+= article_holder.find('span').text + '\n'

            #get paragraphs
            for p_holder in article_holder.find_all('p'):
                if p_holder != None:
                    article+= p_holder.text + '\n'

            if len(article) > 0:
                articles.append(article)

        return articles
        

if __name__ == '__main__':
    items = JavaScript_scrape().scrape_aapNews()
    print(items)
    print('articles', len(items))


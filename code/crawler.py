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
    scrapping javascript based website
    """

    def get_js_soup(self, url):
        """
        uses webdriver object to  generate the first 10 results ( first page)
        execute javascript code and get dynamically loaded webcontent
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
        
        #remove script and style
        for script in soup(["script", "style"]):
            script.decompose()

        return soup        

    def process_output(self, articles=[], output='list', source="unknown"):
        """
        Processes the output according to the user needs
        """
        if output == 'txt':
            curr_path = os.getcwd()
            output_path = curr_path + '\\articles'
            
            if len(articles) == 0:
                return []

            #make directory articles if it does not exist 
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            #iterate through articles and print them out
            for i, article in enumerate(articles):                
                if len(article) < 1:
                    continue
                
                with open(output_path+'\\'+source+'-'+str(i)+'.txt', 'w') as f:
                    f.write(article)

        return articles

    def removeNonAsciiCharacters(self, string):
        return string.encode('ascii',errors='ignore').decode('utf-8')   #removes non-ascii characters


    def scrape_medicalNewsToday(self, limit=5, output='list'):
        """
        extracts newest articles from medical news today
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
                article+= self.removeNonAsciiCharacters(article_holder.find('h1').text) + '\n'

            #get paragraphs
            for p_holder in article_holder.find_all('p'):
                if p_holder != None:
                    article+= self.removeNonAsciiCharacters(p_holder.text) + '\n'
            
            if len(article) > 0:
                articles.append(article)

        return self.process_output(articles=articles, output=output, source='medicalNewsToday')

    def scrape_aapNews(self, limit=5, output='list'):
        """
        extracts newest articles from AAP news
        """
        news_links = []
        news_url = 'https://www.aappublications.org/news'
        base_url = 'https://www.aappublications.org/'

        # scrape to find news links in the base url
        soup = self.get_js_soup(news_url)

        for i, link_holder in enumerate(soup.find_all('div',class_='widget-SelectableContentList')):
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
            soup = self.get_js_soup(link)
            article = ""

            #get div that contains the article

            if soup == None:
                continue 

            #get article titles
            title_holder = soup.find('span', {"class": "header-title"})
            if title_holder != None:
                article+= self.removeNonAsciiCharacters(title_holder.text) + '\n'
    
            #get paragraphs
            for p_holder in soup.find_all('p'):
                if p_holder != None:
                    article+= self.removeNonAsciiCharacters(p_holder.text) + '\n'

            if len(article) > 0:
                articles.append(article)

        return self.process_output(articles=articles, output=output, source='aapNews')
        

if __name__ == '__main__':
    items = JavaScript_scrape().scrape_aapNews(limit=1, output='txt')
    print(items)
    print('articles', len(items))


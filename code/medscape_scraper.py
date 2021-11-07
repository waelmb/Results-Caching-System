from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib
import time

#create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver',options=options)

#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,driverdriver):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

#tidies extracted text 
def process_text(text):
    text = text.encode('ascii',errors='ignore').decode('utf-8')       #removes non-ascii characters
    text = re.sub('\s+',' ',text)       #repalces repeated whitespace characters with single space
    text = re.sub('Text Body: ','',text)
    return text

''' More tidying
Sometimes the text extracted HTML webpage may contain javascript code and some style elements. 
This function removes script and style tags from HTML so that extracted text does not contain them.
'''
def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup


#Checks if url is a valid homepage
def is_valid_homepage(text_url,dir_url):
    if text_url.endswith('.pdf'): #we're not parsing pdfs
        return False
    try:
        ret_url = urllib.request.urlopen(text_url).geturl() 
    except:
        return False       #unable to access bio_url
    urls = [re.sub('((https?://)|(www.))','',url) for url in [ret_url,dir_url]] #removes url scheme (https,http or www) 
    return not(urls[0]== urls[1])

#extracts all News page urls from the Main Page
def scrape_page(dir_url,driver):
    print ('-'*20,'Scraping news page','-'*20)
    news_links = []
    # base_url = 'https://www.medscape.com/'
    #execute js on webpage to load news listings on webpage and get ready to parse the loaded HTML 
    soup = get_js_soup(dir_url,driver)    
    for link_holder in soup.findAll('a'): #get list of all <a>

        if (link_holder.has_attr('href')):
            rel_link = link_holder['href'] #get url
            #url returned is relative, so we need to add base url
            if ('viewarticle' not in rel_link):
                continue
            if (rel_link.startswith('//')):
                rel_link = rel_link[rel_link.find('//') + 2:]
            if ('medscape' not in rel_link and '//' not in rel_link and rel_link.find('/') == 0):
                rel_link = 'https://www.medscape.com' + rel_link
            if ('https' not in rel_link):
                rel_link = 'https://' + rel_link
            news_links.append(rel_link) 
    print ('-'*20,'Found {} news urls'.format(len(news_links)),'-'*20)
    return list(set(news_links))


def scrape_news_page(news_url,driver):
    soup = get_js_soup(news_url,driver)
    homepage_found = False
    article_url = ''
    text = ''
    article_sec = soup.find('div',class_='article-wrapper')
    if article_sec is not None:
        # parent = profile_sec.('div',class_='even')
        # next_tag = parent.find_next('p')
        # relevant = next_tag.next_sibling
        # print(relevant)
        if not homepage_found:
            article_url = news_url #treat faculty profile page as homepage
            text = process_text(article_sec.get_text(separator=' '))

    return article_url,text
def write_lst(lst,file_):
    with open(file_,'w') as f:
        f.write('\n'.join(lst))
dir_url = 'https://www.medscape.com/' #url of home page
news_links = scrape_page(dir_url,driver)
# with open('/Users/shirleymao/cs410/MP2_private/bio_urls.txt', 'w') as f:
#     f.write('\n'.join(faculty_links))
article_urls, articles = [], []
tot_urls = len(news_links)
for i,link in enumerate(news_links):
    print ('-'*20,'Scraping article url {}/{}'.format(i+1,tot_urls),'-'*20)
    print(link)
    article_url,article = scrape_news_page(link,driver)
    if (i > 30):
        break
    if article.strip()!= '' and article_url.strip()!='':
        article_urls.append(article_url.strip())
        articles.append(article)
    else:
        print ('-'*20,'Dropping empty article url {}/{}'.format(i+1,tot_urls),'-'*20)
driver.close()

article_urls_file = '../medscape_urls.txt'
articles_file = '../medscape_articles.txt'
write_lst(article_urls,article_urls_file)
write_lst(articles,articles_file)

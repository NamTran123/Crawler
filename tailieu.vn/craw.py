from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_soup(link_cate):
    chrome_options = Options()


    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chromedriver = "./chromedriver_linux64/chromedriver"


    driver = webdriver.Chrome(executable_path=chromedriver ,chrome_options=chrome_options)
    driver.get(link_cate)

    data = driver.page_source
    driver.close()

    soup = BeautifulSoup(data, "html.parser")
    return soup

def get_link(link_cate):
    soup = get_soup(link_cate)
    div = soup.find("div", {"id": "loaddocdetail"})
    # print(new_feeds)
    iframe = div.find_all('iframe', {'id': 'loaddocdetail2'})

    link = iframe[0].get('src')
    link = link[51:]
    print('Link: {}'.format( link))

enter_link  = 'https://tailieu.vn/bst/dap-an-de-thi-thpt-quoc-gia-nam-2019-418707.html'
get_link(enter_link)
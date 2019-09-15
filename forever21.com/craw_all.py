from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests


def get_list_cat(list_cate, main):
    list_ = []
    for i in list_cate:
        list_.append(main+i)
    return list_


def get_soup(link_cate):
    chrome_options = Options()


    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(link_cate)

    data = driver.page_source
    driver.close()

    soup = BeautifulSoup(data, "html.parser")
    return soup


def get_all_list_pages(link_category):
    soup = get_soup(link_category)
    a = soup.find("div", {"id": "products-count"})
    c = a.text
    list_c = list(c.split(" "))
    x = round(int(list_c[0])/120)
    list_page = []
    for i in range(1, x+1):
        link = link_category
        link = link+'#pageno='+str(i)
        list_page.append(link)
    return list_page


def get_all_list_product(link_cate, main='https://www.forever21.com'):
    soup = get_soup(link_cate)
    new_feeds = soup.findAll("div", {"class": "pi_container"})
    n_link = []
    for ne in new_feeds:
        A = ne.find_all('a', {'class': 'item_slider product_link'})

        link = A[0].get('href')
        # print('Link: {}'.format( link))
        n_link.append(main+link)
    # print(*n_link,  sep = "\n")
    return n_link

# a = get_all_list_pages('https://www.forever21.com/us/shop/catalog/category/f21/dress',soup)
# print(a)

# n_link  =  get_all_list_product(soup, main)


def craw_item(link_item, cate):
    print(link_item)
    soup = get_soup(link_item)
    name = soup.find("h1", {"id": "h1Title"}).getText()
    d = soup.find("div", {"class": "p_price ws_100 row mb_10"})
    price = ''
    if (soup.find("span", {"class": "pr_20"}) != None):
        price = soup.find("span", {"class": "pr_20"}).text
    else:
        price = soup.find("span", {"class": "p_sale t_bold t_pink pt_10"}).text

    color = soup.find("p", {"id": "selectedColorName"}).text
    list_size = []
    d = soup.find("ul", {"id": "sizeButton"})
    for i in d.findAll('span'):
        list_size.append(i.text)

    list_link = soup.find("ul", {"id": "imageButtonList"})
    li = list_link.findAll('li')
    n_link = []
    for i in li:
        A = i.find_all('img', {'class': 'ae-img'})

        link = A[0].get('src')
        # print('Link: {}'.format( link))
        n_link.append(link)

    list_details = []
    details = soup.findAll("div", {"class": "d_content"})
    for i in details:
        list_details.append(i.text)

    feature = [[cate], [name], [price], [color],
               [list_size], [n_link], [list_details]]
    return feature

# ls  = craw_item('https://www.forever21.com/us/shop/catalog/product/f21/top_blouses-long-sleeves/2000373112')
# # print(*ls,sep = "\n")


if __name__ == "__main__":
    out = csv.writer(open("myfile7.csv", "w+"),
                     delimiter=',', quoting=csv.QUOTE_ALL)
    women_main = 'https://www.forever21.com/us/shop/catalog/category/f21/'
    list_cate = ['sets', 'sweater', 'swimwear_all', 'top_blouses']
    list_category = get_list_cat(list_cate, women_main)
    for i in list_cate:
        for cate in list_category:
            list_pages = get_all_list_pages(cate)
            for page in list_pages:
                products = get_all_list_product(page)
                for pr in products:
                    item = craw_item(pr, i)
                    out.writerow(item)

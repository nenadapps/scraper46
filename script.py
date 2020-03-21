from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

def get_html(url):
    
    headers = {
        'Host': 'www.shieldsstampsandcoins.com ',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.shieldsstampsandcoins.com/banknotes',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
       
    html_content = ''
    try:
        page = requests.get(url, headers=headers)
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp
    
    try:
        title = html.select('#productName')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None      
    
    try:
        raw_text = html.select('#productDescription')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
    
    try:
        price = html.select('#productPrices')[0].get_text().strip()
        price = price.replace('$', '').strip().replace(',', '')
        stamp['price'] = price
    except:
        stamp['price'] = None  
        
    try:
        category = html.select('#navBreadCrumb a')[1].get_text().strip()
        stamp['category'] = category
    except:
        stamp['category'] = None  
       
    try:
        subcategory = html.select('#navBreadCrumb a')[2].get_text().strip()
        stamp['subcategory'] = subcategory
    except:
        stamp['subcategory'] = None     
        
    try:
        subsubcategory = html.select('#navBreadCrumb a')[3].get_text().strip()
        stamp['subsubcategory'] = subsubcategory
    except:
        stamp['subsubcategory'] = None     

    stamp['currency'] = 'AUD'
    
    # image_urls should be a list
    images = []                    
    try:
        image_parts1 = str(html).split('document.write(\'<a href="')
        if image_parts1[1]:
            image_parts2 = image_parts1[1].split('"')
            img = 'http://www.shieldsstampsandcoins.com/' + image_parts2[0]
            if img not in images:
                 images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = url
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''
    
    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.itemTitle a'):
            item_link = item.get('href').replace('&amp;', '&')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    try:
        next_items = html.select('.navSplitPagesLinks a')
        for next_item in next_items:
            next_text = next_item.get_text().strip()
            next_href = next_item.get('href').replace('&amp;', '&')
            if '[Next' in next_text:
                next_url = next_href
    except:
        pass   
    
    shuffle(list(set(items)))
    
    return items, next_url

def get_categories(url, index):
   
    items = []

    try:
        html = get_html(url)
    except:
        return items
    
    if index == 2:
        index_string = '  '
    elif index == 4:    
        index_string = '    '
        
    try:
        for item in html.select('.betterCategories a'):
            if index_string in item:
                item_link = item.get('href').replace('&amp;', '&')
                if item_link not in items: 
                    items.append(item_link)
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items

def get_category_page_items(page_url):    
    while(page_url):
        page_items, page_url = get_page_items(page_url)
        for page_item in page_items:
            stamp = get_details(page_item) 

item_dict = {
"Banknotes": "http://www.shieldsstampsandcoins.com/banknotes",
"Coins": "http://www.shieldsstampsandcoins.com/coins",
"Medals and Militaria": "http://www.shieldsstampsandcoins.com/military",
"Sport": "http://www.shieldsstampsandcoins.com/sport",
"Stamps": "http://www.shieldsstampsandcoins.com/stamps"
    }
    
for key in item_dict:
    print(key + ': ' + item_dict[key])   

selection = input('Choose category: ')

selected_main_category = item_dict[selection]

categories = get_categories(selected_main_category, 2) 
for category in categories:
    subcategories = get_categories(category, 4) 
    if len(subcategories):
        for subcategory in subcategories:
            get_category_page_items(subcategory)
    else:
        get_category_page_items(category)
    

import random
import string
import requests
import MySQLdb
import re
from cfg import *
from bs4 import BeautifulSoup
import urllib.parse

def python_web_crawler(url):
    db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DATABASE)
    cursor = db.cursor() #made to execute sql commands 
    request = requests.get(url) 
    status = int(request.status_code) #to check request was successful or not
    content_type = request.headers['Content-Type']
    content_length = len(request.content)
    path_name = None
    bool = 0
    latest_date = 'SELECT MAX(created_at) INTO @last_crawl_date FROM webscrapper WHERE source_link ="{}" AND is_crawled IS TRUE ORDER BY created_at DESC LIMIT 1'.format(url)
    cursor.execute(latest_date)
    if status == 200:
        search = re.search("text/html(.*)",content_type) 
        if search:
            res_text = request.text
            soup = BeautifulSoup(res_text, "html.parser") #For pulling data out of html file
            to_write = soup.prettify() 
            links = soup.find_all('a')
            extension = '.html';
            mode = 'w'
            en = 'not_bin' 
        else:   
            to_write = request.content
            extension = '.' + content_type
            mode = 'wb'
            en = 'bin'
        name = "".join(random.choice(char) for n in range(11))
        path_name = "files/" +name + extension
        file = open('files/{}'.format(name) + extension, mode, encoding = encod[en])
        file.write(to_write)
        file.close()
    elif status != 200:
        sql_a = "INSERT INTO webscrapper(source_link, is_crawled, last_crawl_date, response_status, content_type, content_length, created_at) VALUES ('{}', {}, {}, '{}', '{}', '{}', {})".format(url, 'TRUE', '@last_crawl_date', status, content_type, content_length, 'NOW()')
        cursor.execute(sql_a)
        db.commit()
        db.close()
        return bool
    for i in range(len(links)):
        link_string = links[i].get('href')
        if link_string == None: 
            continue 
        search1 = re.search('javascript:;',link_string)
        if search1 or len(link_string) <= 2:
            continue
        link_string = urllib.parse.urljoin(url, link_string)
        search2 = re.search("http(.*)",link_string)
        result =urllib.parse.urlparse(link_string)
        if all([result.scheme, result.netloc]) and search2:#scheme for starting 
        	pass
        else:
        	continue
        sql_b = 'SELECT "{}" INTO @link_to_check'.format(link_string)
        cursor.execute(sql_b)
        sql_c = "INSERT INTO webscrapper(link, source_link, is_crawled, last_crawl_date, response_status, content_type, content_length, filepath, created_at) VALUES ('{}', '{}', {}, {}, '{}', '{}', '{}', '{}', {})".format(link_string, url, 'TRUE', '@last_crawl_date', status, content_type, content_length, path_name, 'NOW()')
        cursor.execute(sql_c)
        db.commit()
        if status == 200:
        	list_of_found_links.append(link_string)
        	print(link_string)
        	if len(list_of_found_links) >= 5000:
        	    print('Maximum limit reached')
        	    bool = 1
        	    db.rollback()
        	    db.close()
        	    return bool
        else:
        	pass
        
    db.close()
    return bool

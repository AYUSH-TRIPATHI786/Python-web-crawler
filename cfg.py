import string

HOST = "localhost"
USERNAME = "ayush"
PASSWORD = ""
DATABASE = "python-web-crawler"
char = string.ascii_letters + string.digits

first_url = "https://flinkhub.com/"
links_to_crawl = [first_url]
list_of_found_links=[]
encod = {'not_bin':'utf-8', 'bin':None} #changed

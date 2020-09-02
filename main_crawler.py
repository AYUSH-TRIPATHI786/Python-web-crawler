import time
from cfg import *
from utils import *
import concurrent.futures

if __name__ == "__main__":  
    while True:
        list_of_found_links.clear()
        with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
        	for urls in links_to_crawl:
        		try:
        		    futures = executor.submit(python_web_crawler, urls)
        		    return_value = futures.result()
        		    if return_value == 1:
        			    break
        		except:
        			pass
        links_to_crawl.clear()   
        links_to_crawl.extend(list_of_found_links)
        if len(links_to_crawl) == 0:
            print("All links crawled")
            links_to_crawl.append(first_url)
        time.sleep(5)

# URL crawler for references
# (Currently) returns url and status code of website.
# Also included: attempts at parallelism that ended up slower than the regular option
import requests
import logging
import aiohttp
import asyncio
import time

class Crawler:

    def __init__(self, urls=[]):
        self.urls_to_visit = urls
        self.results = [{"url": str, "code": str}]
    
    def crawl(self, url):                
        try:
            resp_code = requests.get(url, timeout=1).status_code
        except Exception as e:
            logging.error("Could not get url {}, error: {}".format(url, str(e)))
            resp_code = 0

        '''
        try:
            async with session.get(url) as resp:
                resp_code = resp.status
        except Exception as e:
            logging.error("Could not get url " + url + " , error: " + str(e))
            resp_code = 404
        '''
        newResult = [{"url": url, "code": str(resp_code)}]
        self.results.append(newResult)
        
    def run(self):
        start = time.time()
        self.results.clear()
        '''
        async with aiohttp.ClientSession() as session:
            try:
                await asyncio.gather(*(self.crawl(url, session) for url in self.urls_to_visit))
            except Exception as e:
                logging.error("Error in Crawler: " + str(e))
        '''
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.debug("Getting url: {}".format(url))
            self.crawl(url)      
        end = time.time()
        print("Took {} seconds".format(end - start))
        return self.results

# Test
if __name__ == "__main__":
    Crawler(urls=["https://www.google.com/", "https://www.facebook.com/"]).run()
    #test = asyncio.run(Crawler(urls=["https://www.google.com/", "https://www.facebook.com/"]).run())
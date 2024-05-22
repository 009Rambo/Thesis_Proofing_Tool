# URL crawler for references
# (Currently) returns url and status code of website.
# Also included: first version, which was a class. Current version is 10x faster.
import requests
import logging
import aiohttp
import asyncio
import time

async def crawl(url, session):                
        '''
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
            resp_code = 0
        
        newResult = [{'url': url}, {'resp': resp_code}]
        return newResult
        
async def run(urls_to_visit):
    start = time.time()
    results = []
        
    async with aiohttp.ClientSession() as session:
        try:
            newresult = await asyncio.gather(*(crawl(url, session) for url in urls_to_visit))
        except Exception as e:
            logging.error("Error in Crawler: " + str(e))
        results.append(newresult)
        '''
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.debug("Getting url: {}".format(url))
            self.crawl(url)      
        '''
    end = time.time()
    print("Took {} seconds".format(end - start))
    return results

'''
class Crawler:

    def __init__(self, urls=[]):
        self.urls_to_visit = urls
        self.results = [{"url": str, "code": str}]
    
    async def crawl(self, url, session):                
        try:
            async with session.get(url) as resp:
                resp_code = resp.status
        except Exception as e:
            logging.error("Could not get url " + url + " , error: " + str(e))
            resp_code = 0
        
        newResult = [{"url": url, "code": str(resp_code)}]
        self.results.append(newResult)
        
    async def run(self):
        start = time.time()
        self.results.clear()
        
        async with aiohttp.ClientSession() as session:
            try:
                await asyncio.gather(*(self.crawl(url, session) for url in self.urls_to_visit))
            except Exception as e:
                logging.error("Error in Crawler: " + str(e))
        end = time.time()
        print("Took {} seconds".format(end - start))
        return self.results
'''
# Test
#if __name__ == "__main__":
    #Crawler(urls=["https://www.google.com/", "https://www.facebook.com/"]).run()
    #test = asyncio.run(Crawler(urls=["https://www.google.com/", "https://www.facebook.com/"]).run())
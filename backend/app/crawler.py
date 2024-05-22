# URL crawler for references
# (Currently) returns url and status code of website.

import logging
import aiohttp
import asyncio
import time

#Crawl - pings url, returns status code & pinged url
async def crawl(url, session):                
        try:
            async with session.get(url) as resp:
                resp_code = resp.status
        except Exception as e:
            logging.error("Could not get url " + url + " , error: " + str(e))
            resp_code = 0
        
        newResult = [{'url': url}, {'resp': resp_code}]
        return newResult
        
async def run_crawler(urls_to_visit):
    start = time.time() #timer
    results = []
    
    async with aiohttp.ClientSession() as session:
        try:
            newresult = await asyncio.gather(*(crawl(url, session) for url in urls_to_visit))
        except Exception as e:
            logging.error("Error in Crawler: " + str(e))
        results.append(newresult)

    end = time.time()
    logging.debug("Took {} seconds to ping {} urls.".format(end - start, len(urls_to_visit)))
    return results

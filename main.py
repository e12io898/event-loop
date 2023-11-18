import asyncio
import aiohttp
from more_itertools import chunked

from models import init_db, Session, SwapiPeople


async def get_person(id, session):
    url = f'https://swapi.dev/api/people/{id}/'
    response = await session.get(url)
    data = await response.json()

    return data


async def main():
    for id_chunk in chunked(range(1, 100), 10):
        session = aiohttp.ClientSession()
        coros = [get_person(id, session) for id in id_chunk]

        result = await asyncio.gather(*coros)
        print(result)

        await session.close()

if __name__ == "__main__":
    asyncio.run(main())

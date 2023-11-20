import asyncio
import aiohttp
from more_itertools import chunked

from models import init_db, Session, SwapiPeople


# Запрос на вложенные ссылки. Возврат наименований в виде строки.
async def internal_data(url_list, session):
    string = []
    for url in url_list:
        responce = await session.get(url)
        data = await responce.json()
        string.append(data['name'] if 'name' in data else data['title'])

    return ', '.join(string)


async def get_person(id, session):

    try:
        url = f'https://swapi.dev/api/people/{id}/'
        response = await session.get(url)
        data = await response.json()

        if response.status == 404:
            return

        del data['created']
        del data['edited']
        del data['url']

        data['people_id'] = id
        data['films'] = await internal_data(data['films'], session)
        data['species'] = await internal_data(data['species'], session)
        data['starships'] = await internal_data(data['starships'], session)
        data['vehicles'] = await internal_data(data['vehicles'], session)

        return data

    except:
        return


# Добавление в базу существующих персонажей.
async def insert_to_db(people_list: list):
    async with Session() as db_session:
        people = [SwapiPeople(**data) for data in people_list if data is not None]
        db_session.add_all(people)
        await db_session.commit()


async def main():
    await init_db()

    session = aiohttp.ClientSession()

    for id_chunk in chunked(range(1, 84), 10):

        coros = [get_person(id, session) for id in id_chunk]
        result = await asyncio.gather(*coros)
        asyncio.create_task(insert_to_db(result))

    await session.close()
    set_of_tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*set_of_tasks)


if __name__ == "__main__":
    asyncio.run(main())

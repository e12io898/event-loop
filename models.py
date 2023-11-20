from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


DB_DSN = 'sqlite+aiosqlite:///db.sqlite'
engine = create_async_engine(DB_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = 'swapi_people'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    people_id: Mapped[int] = mapped_column(Integer)
    birth_year: Mapped[str] = mapped_column(String(20))
    eye_color: Mapped[str] = mapped_column(String(20))
    films: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String(20))
    hair_color: Mapped[str] = mapped_column(String(20))
    height: Mapped[int] = mapped_column(Integer)
    homeworld: Mapped[str] = mapped_column(String)
    mass: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(50))
    skin_color: Mapped[str] = mapped_column(String(20))
    species: Mapped[str] = mapped_column(String)
    starships: Mapped[str] = mapped_column(String)
    vehicles: Mapped[str] = mapped_column(String)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

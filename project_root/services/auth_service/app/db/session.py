from sqlalchemy.ext.asyncio import create_async_engine ,async_sessionmaker
from app.core.config import settings




# движок для подключения к бд
engine = create_async_engine(
    settings.DATABASE_URL,
    echo = True,
)


# фабрика сессий
async_session = async_sessionmaker(
    bind = engine,
    expire_on_commit = False,
    autocommit = False,
    autoflush = False,
)

# генератор сессий, создаёт сессию на один HTTP-запрос, для инъекции зависимостей
async def get_db():
    async with async_session() as db:
        yield db
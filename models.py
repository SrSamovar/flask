import atexit
import datetime
import os
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRESS_PASSWORD = os.getenv("POSTGRESS_PASSWORD", "password")
POSTGRES_DB = os.getenv('POSTGRES_DB', "site")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

POSTGRES_DSN = (f"postgresql://"
                f"{POSTGRES_USER}:{POSTGRESS_PASSWORD}@"
                f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
                f"{POSTGRES_DB}")

engine = create_engine(POSTGRES_DSN)

Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = 'post'

    post_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    author: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    def dict(self):
        return {
            "id": self.post_id,
            "title": self.title,
            "description": self.description,
            'created_at': self.created_at.isoformat()
        }


Base.metadata.create_all(engine)

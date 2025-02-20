from sqlalchemy import Column, Integer, BigInteger, String, Float

from models.base import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nick_name = Column(String, unique=True, nullable=True, default=None)
    guild_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    level = Column(Integer, default=0)
    matches = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    kills = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    score = Column(Float, default=0.0)
    description = Column(String, default=None, nullable=True)
    avatar = Column(String, default=None, nullable=True)

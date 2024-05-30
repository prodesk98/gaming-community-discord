from sqlalchemy import Column, Integer, ForeignKey, func, DateTime

from models.base import Base


class Scores(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    value = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

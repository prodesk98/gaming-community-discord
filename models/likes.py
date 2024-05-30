from sqlalchemy import Column, Integer, ForeignKey, DateTime, func

from models.base import Base


class Likes(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    target_id = Column(Integer, ForeignKey('profiles.id'))
    created_at = Column(DateTime, server_default=func.now())

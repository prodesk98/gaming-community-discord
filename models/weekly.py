from sqlalchemy import Column, Integer, ForeignKey, DateTime, func

from models.base import Base


class Weekly(Base):
    __tablename__ = 'weekly'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    level = Column(Integer)
    kills = Column(Integer)
    wons = Column(Integer)
    losses = Column(Integer)
    assist = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

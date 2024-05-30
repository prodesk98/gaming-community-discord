from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class StatsORM(BaseModel):
    level: int = 0
    matches: int = 0
    wins: int = 0
    losses: int = 0
    kills: int = 0
    assists: int = 0
    score: float = 0.0


class MatchAttributes(BaseModel):
    id: datetime


class MatchMetadata(BaseModel):
    timestamp: datetime
    isGrouped: bool


class SegmentAttributes(BaseModel):
    accountId: str


class Stat(BaseModel):
    value: Optional[float | int] = 0


class Stats(BaseModel):
    matchesCompleted: Optional[Stat] = Stat()
    matchesWon: Optional[Stat] = Stat()
    matchesLost: Optional[Stat] = Stat()
    playerLevel: Optional[Stat] = Stat()
    kills: Optional[Stat] = Stat()
    score: Optional[Stat] = Stat()
    assists: Optional[Stat] = Stat()
    mvpCount: Optional[Stat] = Stat()


class Segment(BaseModel):
    type: str
    attributes: SegmentAttributes
    metadata: Optional[dict] = Field(default_factory=dict)
    expiryDate: datetime
    stats: Stats


class Match(BaseModel):
    attributes: MatchAttributes
    metadata: MatchMetadata
    segments: List[Segment]


class Data(BaseModel):
    matches: List[Match]


class Root(BaseModel):
    data: Data

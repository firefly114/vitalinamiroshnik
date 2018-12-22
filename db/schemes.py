from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)

    fullname = Column(String)
    birth = Column(Date)
    pos = Column(String)
    club_id = Column(Integer)
    agent_id = Column(Integer)
    market_value = Column(Integer)

    def __repr__(self):
        return "<Player(№%d | %s | %s | %s | %d)>" \
               % (self.id, self.fullname, str(self.birth), self.pos, self.market_value)


class Club(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True)

    title = Column(String)
    coach = Column(String)
    league = Column(String)
    euro_cups = Column(Boolean)

    def __repr__(self):
        return "<Club(№%d | %s | %s | %s | %s)>" \
               % (self.id, self.title, self.coach, self.league, str(self.euro_cups))


class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True)

    fullname = Column(String)
    salary = Column(Integer)

    def __repr__(self):
        return "<Agent(№%d | %s | %d)>" \
               % (self.id, self.fullname, self.salary)

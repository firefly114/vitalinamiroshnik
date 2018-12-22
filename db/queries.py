from sqlalchemy.orm import sessionmaker
import sqlalchemy
from db.schemes import Player
from db.schemes import Club
from db.schemes import Agent
import sys
import random
from string import punctuation
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Database:
    engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:1234@localhost/lab1')
    _Session = sessionmaker(bind=engine)

    def __init__(self):
        engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:1234@localhost/lab1')
        _Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        self.session = _Session()

    def get_players(self):
        rows = []
        for p in self.session.query(Player).\
                order_by(Player.id):
            rows.append(p)
        return rows

    def get_clubs(self):
        rows = []
        for p in self.session.query(Club). \
                filter(Club.id > 0). \
                order_by(Club.id):
            rows.append(p)
        return rows

    def get_agents(self):
        rows = []
        for p in self.session.query(Agent). \
                filter(Agent.id > 0). \
                order_by(Agent.id):
            rows.append(p)
        return rows

    def get_player_id(self, id):
        return self.session.query(Player).get(id)

    def get_club_id(self, id):
        return self.session.query(Club).get(id)

    def get_agent_id(self, id):
        return self.session.query(Agent).get(id)

    def get_random_club_id(self):
        rows = self.get_clubs()
        id = rows[random.randint(0, len(rows) - 1)]
        return int(''.join(c for c in str(id) if c not in punctuation))

    def get_random_agent_id(self):
        rows = self.get_agents()
        id = rows[random.randint(0, len(rows) - 1)]
        return int(''.join(c for c in str(id) if c not in punctuation))

    def new_player(self, player):
        self.session.add(player)
        self.session.commit()

    def new_club(self, club):
        self.session.add(club)
        self.session.commit()

    def new_agent(self, agent):
        self.session.add(agent)
        self.session.commit()

    def update_player(self, player):
        self.new_player(player)

    def update_club(self, club):
        self.new_club(club)

    def update_agent(self, agent):
        self.new_agent(agent)

    def delete_player(self, pid):
        self.session.delete(self.get_player_id(pid))
        self.session.commit()

    def delete_club(self, cid):
        for player in self.session.query(Player). \
                filter(Player.club_id == cid):
            player.club_id = 0
            self.update_player(player)
        self.session.delete(self.get_club_id(cid))
        self.session.commit()

    def delete_agent(self, aid):
        for player in self.session.query(Player). \
                filter(Player.agent_id == aid):
            player.agent_id = 0
            self.update_player(player)
        self.session.delete(self.get_agent_id(aid))
        self.session.commit()

    def search_clubs_euro(self, cond):
        return self.session.query(Club). \
            filter(Club.euro_cups == cond and Club.id > 0). \
            order_by(Club.id)

    def search_range_players(self, n1, n2):
        return self.session.query(Player, Club). \
            filter(n1 < Player.market_value < n2). \
            filter(Player.club_id == Club.id). \
            order_by(Player.id)

    def search_range_agents(self, n1, n2):
        return self.session.query(Agent). \
            filter(n1 < Agent.salary < n2). \
            order_by(Agent.id)

    def search(self, text):
        sql = f"SELECT ts_headline(fullname, q), players.id, birth, market_value, ts_headline(pos, q), club_id, agent_id \
                        FROM to_tsquery('{text}') AS q, players \
                      WHERE make_tsvector(players.fullname) @@ q OR \
                      make_tsvector(players.pos) @@ q"

        return self.engine.execute(sql).fetchall()

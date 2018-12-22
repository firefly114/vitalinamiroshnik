from ui.input import *
from db.schemes import Player
from db.schemes import Club
from db.schemes import Agent


def check_input(cb, helpstr, db=None):
    while True:
        try:
            if db is not None:
                return cb(helpstr, db)
            return cb(helpstr)
        except ValueError:
            print("Try again...")
            continue


def input_player(db):
    print("Input required values and press enter...")
    p = Player(fullname=input("Fullname: "),
               market_value = check_input(input_num, "Market value: "),
               birth=check_input(input_date, "Date of birth (dd-mm-yyyy): "),
               pos=input("Position: "),
               club_id=check_input(input_club_id, "Please input club id that exists or 0: ", db),
               agent_id=check_input(input_agent_id, "Please input agent id that exists or 0: ", db))
    db.new_player(p)


def input_club(db):
    print("Input required values and press enter...")
    c = Club(title=input("Title: "),
             coach=input("Coach: "),
             league=input("League: "),
             euro_cups=input("Is club plays at euro cups (True or False): ") == "True")
    db.new_club(c)


def input_agent(db):
    print("Input required values and press enter...")
    a = Agent(fullname=input("Fullname: "),
              salary=check_input(input_num, "Salary: "))
    db.new_agent(a)


def update_player(db, id):
    # select cols to update
    # input(col)
    player = db.get_player_id(id)
    print("Input required values and press enter...")
    inp = input("Position: ")
    new_p = Player(fullname=player.fullname,
                   market_value=check_input(input_num, "Market value: "),
                   birth=player.birth,
                   pos=inp if inp is not '' else player.pos,
                   club_id=check_input(input_club_id, "Please input club id: ", db),
                   agent_id=check_input(input_agent_id, "Please input agent id: ", db))
    db.update_player(new_p)


def update_club(db, id):
    club = db.get_club_id(id)

    print("Input required values and press enter...")
    coach = input("Coach: ")
    league = input("League: ")
    euro = input("Is club plays at euro cups (True or False): ")
    new_c = Club(title=club.title,
                 coach=coach if coach is not '' else club.coach,
                 league=league if league is not '' else club.league,
                 euro_cups=euro == "True" if euro is not '' else club[4])
    db.update_club(new_c)


def update_agent(db, id):
    agent = db.get_agent_id(id)
    print("Input required values and press enter...")
    new_a = Agent(fullname=agent.fullname,
                  salary=check_input(input_num, "Salary: "))
    db.update_agent(new_a)

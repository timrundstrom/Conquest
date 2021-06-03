import random
import time
import json
from datetime import datetime

display_rounds = True

class Country:

    all_countries = []
    countries_alive = []
    kicked_out_countries = []
    countries_remaining = 0

    def __init__(self, name, neighbours):
        self.name = name
        self.controlled_by = name
        self.neighbours = neighbours
        self.borders = neighbours
        self.kicked_out_by = ""

def overtake(winner, loser):
    for i in Country.all_countries:
        if(i.name == loser):
            if(i.controlled_by == i.name):
                i.controlled_by = winner
                update_borders(winner)
                update_borders(loser)
                if(display_rounds):
                    print(f'{winner} takes over {loser}!')
                break
            else:
                for j in Country.all_countries:
                    if(j.name == i.controlled_by):
                        i.controlled_by = winner
                        update_borders(winner)
                        update_borders(loser)
                        update_borders(j.name)
                        if(display_rounds):
                            print(f'{winner} takes over {loser} from {j.name}!')
                        break
    kick_out_country()

def update_borders(country):
    controlling_land = []
    for i in Country.all_countries:
        if (i.controlled_by == country and i.name not in controlling_land):
            controlling_land.append(i.name)

    possible_borders = []
    for i in Country.all_countries:
        for j in controlling_land:
            if (i.name == j):
                for k in i.neighbours:
                    if (k not in possible_borders):
                        possible_borders.append(k)
    
    borders = []
    for i in Country.all_countries:
        for j in possible_borders:
            if (i.name == j):
                if(i.controlled_by != country and i.name not in borders):
                    borders.append(i.name)

    for i in Country.all_countries:
        if (i.name == country):
            i.borders = borders

def kick_out_country():
    for i in Country.all_countries:
        safe = False
        if(i.controlled_by == i.name):
            safe = True
        else:
            for j in Country.all_countries:
                if (j.controlled_by == i.name):
                    safe = True
        if (safe == False):
            if (i.name not in Country.kicked_out_countries):
                if(display_rounds):
                    print(f'{i.name} is kicked out!')
                Country.kicked_out_countries.append(i.name)
                for j in Country.countries_alive:
                    if (j.name == i.name):
                        Country.countries_alive.remove(j)
                        if(len(Country.countries_alive) <= 30):
                            print(f'{j.name} is kicked out!')
                            current_time = datetime.now()
                            current_time = current_time.strftime('%H:%M:%S')
                            print(f'{len(Country.countries_alive)} countries left at round {round} ({current_time})\n')
                Country.countries_remaining = len(Country.all_countries) - len(Country.kicked_out_countries)
                i.kicked_out_by = i.controlled_by
                if(display_rounds):
                    print(f'{Country.countries_remaining} countries remaining.')

with open('countries.json', 'r') as openfile:
    json_object = json.load(openfile)

for key in json_object:
    Country.all_countries.append(Country(key, json_object[key]))

round = 1
Country.countries_remaining = len(Country.all_countries)
Country.countries_alive += Country.all_countries
timer = time.time()
show_score = True

while(Country.countries_remaining > 1):

    if(len(Country.countries_alive) == 10 and show_score):
        print()
        print(20*'-'+'TOP TEN'+20*'-')
        for i in Country.countries_alive:
            ground = 0
            for j in Country.all_countries:
                if (j.controlled_by == i.name):
                    ground += 1
            print(f'{i.name} : {ground} ')
        print(47*'-')
        print()
        show_score = False

    if(display_rounds):
        print(20*'-'+str(round)+20*'-')
    winner = ""
    winner = Country.countries_alive[random.randrange(0, len(Country.countries_alive))]
    
    if (len(winner.borders) == 1):
        loser = winner.borders[0]
    else:
        loser = winner.borders[random.randrange(0, len(winner.borders))]
    overtake(winner.name, loser)

    if(display_rounds):
        print(f'{Country.countries_remaining} countries remaining.')
        print(20*'-'+len(str(round))*'-'+20*'-'+'\n\n')
    round += 1


if(Country.countries_remaining == 1):
    print(f'The winner is {Country.countries_alive[0].name}!\nThe war took {round} rounds.')
else:
    print(f'{Country.countries_remaining} countries out of {len(Country.all_countries)} left after {round} rounds!')

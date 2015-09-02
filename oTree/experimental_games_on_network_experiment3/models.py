# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
import otree.constants
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>
from numpy import *

author = 'NIGG'

doc = """
Your app description
"""

class Constants():
    name_in_url = 'experimental_games_on_network_experiment3'
    players_per_group = 5
    num_rounds = 2

    # define more constants here
    network_type_group = ["Orange network", "Green network", "Purple network"]
    weight = [0.8, 0.1, 0.1]
    network_type = random.choice(network_type_group, p=weight)   

    if network_type == "Orange network":
        network = {"A":["B"], "B":["A", "C", "D"], "C":["B", "D"], "D":["B", "C", "E"], "E":["D"]}
    elif network_type == "Green network":
        network = {"A":["B"], "B":["A", "C"], "C":["B", "D"], "D":["C", "E"], "E":["D"]}
    else:
        network = {"A":["B"], "B":["A", "C", "D"], "C":["B"], "D":["B", "E"], "E":["D"]}
    
    assign_player = [i for i in range(players_per_group)]
    assign_place = network.keys()
    k = 0
    i = 0
    while len(assign_place) > 0:
        selected_place = random.choice(assign_place)   
        assign_player[i] = selected_place
        assign_place.remove(selected_place)
        k += 1
        i += 1
        
    assign_nghb = [i for i in range(players_per_group)]
    for i in range(len(assign_nghb)):
        assign_nghb[i] = network[assign_player[i]]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    active_or_inactive = models.CharField()

    def set_payoffs(self):
        player = [i for i in range(Constants.players_per_group)]
        num_active = [0 for i in range(Constants.players_per_group)]
        for i in range(Constants.players_per_group):
            player[i] = self.get_player_by_role(Constants.assign_player[i])
            for k in range(len(Constants.assign_nghb[i])):
                if self.get_player_by_role(Constants.assign_nghb[i][k]).decision == 'ACTIVE':
                    num_active[i] += 1
            player[i].payoff = float(100*num_active[i]/3)

class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    decision = models.CharField(
        choices=['ACTIVE', 'INACTIVE'],
        doc="""このプレイヤーの選択は""",
        widget=widgets.RadioSelect()
    )

    def place(self):
        self.place = Constants.assign_player[self.id_in_group - 1]
        return self.place

    def nghb(self):
        self.nghb = Constants.assign_nghb[self.id_in_group - 1]
        return self.nghb 


    def other_player(self):      
        return self.get_others_in_group()[0]

    def role(self):
        return  Constants.assign_player[self.id_in_group - 1]            

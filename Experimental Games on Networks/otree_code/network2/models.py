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
    name_in_url = 'network2'
    players_per_group = 5
    num_rounds = 40
    places = ['A', 'B', 'C', 'D', 'E']
    p = 0.2
    weight = [p, (1-p)/2, (1-p)/2]

    # define more constants here

class Subsession(BaseSubsession):

    def before_session_starts(self):
        Group.network_histry = []
        for i in range(Constants.num_rounds):
            for group in self.get_groups():
                Group.network_tp = group.network_type()
                Group.network_group = group.network()
                players = group.get_players()
                random.shuffle(players)
                group.set_players(players)
            Group.network_histry.append([ Group.network_group[0],  Group.network_group[1]])

class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    networktype = models.CharField()
    
    def network_type(self):
        network_type_group = ['Blue network', 'Red network', 'Brown network']
        network_type = random.choice(network_type_group, p=Constants.weight)   
        return network_type

    def network(self):
        network_type = str(self.network_tp)
        if network_type == 'Blue network':
            network = {'A':['B'], 'B':['A', 'C', 'E'], 'C':['B', 'D', 'E'], 'D':['C', 'E'], 'E':['B', 'C', 'D']}
        elif network_type == 'Red network':
            network = {'A':['B'], 'B':['A', 'C'], 'C':['B', 'D', 'E'], 'D':['C', 'E'], 'E':['C', 'D']}
        else:
            network = {'A':['B'], 'B':['A', 'C', 'E'], 'C':['B', 'D'], 'D':['C', 'E'], 'E':['B', 'D']}
        network_group = [network_type, network]
        return network_group

    def set_payoffs(self):
        network_group = self.network_histry[self.subsession.round_number-1]
        self.network_type = network_group[0]
        self.network = network_group[1]
        player = [0 for i in range(Constants.players_per_group)]
        active = [0 for i in range(Constants.players_per_group)]
        i = 0 
        for role in Constants.places:
            player[i] = self.get_player_by_role(role)
            assign_nghb = self.network[role]
            for other_role in assign_nghb:
                if self.get_player_by_role(other_role).decision == 'ACTIVE':
                    active[i] += 1
            player[i].payoff = float(100*active[i]/3)
            player[i].num_active = active[i]
            i += 1

        
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

    nghb = models.PositiveIntegerField()
    num_active = models.PositiveIntegerField()

    def other_player(self):      
        return self.get_others_in_group()[0]

    def role(self):
        return Constants.places[self.id_in_group - 1]  

    def num_nghb(self):
        return  len(Group.network_histry[self.subsession.round_number-1][1][self.role()])
        

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

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'spacial_competiton'
    players_per_group = 2
    num_rounds = 5
    leader_follower = ['leader', 'follower'] 

    # define more constants here


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    type = models.CharField(
        choices=['SIM', 'SEQ'],
        doc="""今回のゲームのタイプは""",
        widget=widgets.RadioSelect()
    )

    def place(self):
        place = [[0,0],[0,0]]
        players = self.get_players()
        i = 0
        for p in players:
            place[i][0] = p.x_place
            place[i][1] = p.y_place
            i += 1
        return place

    def place2(self):
        o_place = [0,0]
        p = self.get_player_by_id(1)
        o_place[0] = p.x_place
        o_place[1] = p.y_place
        return o_place

    def game_type(self):
        self.type = self.in_previous_rounds()[0].type

    def set_payoffs(self):   
        p1 = self.get_player_by_id(1) 
        p2 = self.get_player_by_id(2) 
        Fx = 0.0
        for i in range(50):
            for j in range(20):
                mytotalcomsumer = (p1.x_place - i)**2 + (p1.y_place - j)**2
                othertotalcomsumer= (p2.x_place - i)**2 + (p2.y_place - j)**2
                if mytotalcomsumer < othertotalcomsumer:
                    Fx += 1.0
                elif mytotalcomsumer == othertotalcomsumer:
                    Fx += 0.5
        mycomsumer = 0.0
        othercomsumer = 0.0
        for i in range(50):
            for j in range(20):
                mytotalprice = 100 + (p1.x_place - i)**2 + (p1.y_place - j)**2
                othertotalprice= ((1000-Fx)/Fx*100) + (p2.x_place - i)**2 + (p2.y_place - j)**2
                if mytotalprice < othertotalprice:
                    mycomsumer += 1.0
                elif mytotalprice == othertotalprice:
                    mycomsumer += 0.5
                    othercomsumer += 0.5
                else:
                    othercomsumer += 1.0
        p1.payoff = 100*mycomsumer
        p2.payoff = ((1000-Fx)/Fx*100)*othercomsumer

class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>
    x_place = models.FloatField()
    y_place = models.FloatField()
    price = models.CurrencyField(
        doc="""The mill price""",
    )

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    

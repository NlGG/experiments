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

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    normal_or_storm_group = ["normal","storm"]
    weight1 = [0.99, 0.1]
    normal_or_storm = random.choice(normal_or_storm_group, p=weight1)
    if normal_or_storm == "storm":
        weather = "storm"
    else:
        weather = 
    weather 
    name_in_url = 'bento_game'
    players_per_group = None
    num_rounds = 1

    # define more constants here


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0 # change to whatever the payoff should be


class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    def role(self):
        # you can make this depend of self.id_in_group
        return ''

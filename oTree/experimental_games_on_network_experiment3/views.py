# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Active_or_Inactive(Page):

    form_model = models.Player
    form_fields = ['decision']

class ResultsWaitPage(WaitPage):

    def body_text(self):
        return 'Waiting for the other participant to choose.'

    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Results(Page):
    def vars_for_template(self):

        self.group.set_payoffs()

        return {
            'num_active': self.player.payoff*3/100,
        }


page_sequence = [
    Active_or_Inactive,
    ResultsWaitPage,
    ResultsWaitPage,
    Results
]

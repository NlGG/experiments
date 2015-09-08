# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

def vars_for_all_templates(self):
    network_group = self.group.network_group

    return {'total_rounds': Constants.num_rounds,
            'round_number': self.subsession.round_number,
            'role': self.player.role(),
            'network_type': self.group.network_histry[self.subsession.round_number-1][0] ,
            'nghb':self.group.network_histry[self.subsession.round_number-1][1][self.player.role()]#

            }

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

class ResultsSummary(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()


        return {'player_in_all_rounds': player_in_all_rounds,
                'total_payoff': sum([p.payoff for p in self.player.in_all_rounds()])}

page_sequence = [
    Active_or_Inactive,
    ResultsWaitPage,
    Results,
    ResultsSummary
]

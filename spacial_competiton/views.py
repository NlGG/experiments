# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class ChoiceGame(Page):
	def is_displayed(self):
		return self.subsession.round_number == 1 and self.player.id_in_group == 1

	form_model = models.Group
	form_fields = ['type']

class ChoiceOne(Page):

    def is_displayed(self):
    	if self.subsession.round_number == 1:
    		return self.group.type == 'SEQ' and self.player.id_in_group == 1
    	else:
    		return self.group.in_previous_rounds()[0].type == 'SEQ' and self.player.id_in_group == 1

    def vars_for_template(self):
		if self.subsession.round_number == 1:
			return {'past_x': 25,
					'past_y': 10,
					}
		else:
			o_player = self.player.get_others_in_group()[0]
			return {'past_x': o_player.in_previous_rounds()[len(o_player.in_previous_rounds())-1].x_place,
					'past_y': 20.0 - o_player.in_previous_rounds()[len(o_player.in_previous_rounds())-1].y_place,
					}

    template_name = 'spacial_competiton/LocationGame.html'

    form_model = models.Player
    form_fields = ['x_place', 'y_place']

class ResultsWaitPage0(WaitPage):
	pass

class ChoiceTwoWaitPage(WaitPage):
	def is_displayed(self):
		if self.subsession.round_number == 1:
		    return self.group.type == 'SEQ'
		else:
		    return self.group.in_previous_rounds()[0].type == 'SEQ'

	def body_text(self):
		if self.player.id_in_group == 1:
			return "Waiting for the other participant to decide."
		else:
			return 'You are to decide second. Waiting for the other participant to decide first.'

class LocationGame2(Page):
	def is_displayed(self):
		if self.subsession.round_number == 1:
			return self.group.type == 'SEQ' and self.player.id_in_group == 2
		else:
			return self.group.in_previous_rounds()[0].type == 'SEQ' and self.player.id_in_group == 2

	def vars_for_template(self):
		return {'o_x_place': self.group.place2()[0],
				'o_y_place': self.group.place2()[1],
				}

	form_model = models.Player
	form_fields = ['x_place', 'y_place']

class LocationGame(Page):
	def is_displayed(self):
		if self.subsession.round_number == 1:
			return self.group.type == 'SIM'
		else:
			return self.group.in_previous_rounds()[0].type == 'SIM'

	form_model = models.Player
	form_fields = ['x_place', 'y_place'] 

	def vars_for_template(self):
		if self.subsession.round_number == 1:
			return {'past_x': 25,
					'past_y': 10,
					}
		else:
			o_player = self.player.get_others_in_group()[0]
			return {'past_x': o_player.in_previous_rounds()[len(o_player.in_previous_rounds())-1].x_place,
					'past_y': 20.0 - o_player.in_previous_rounds()[len(o_player.in_previous_rounds())-1].y_place,
					}

class ResultsWaitPage1(WaitPage):
    def after_all_players_arrive(self):
        self.group.place2()
        if self.subsession.round_number != 1:
        	self.group.game_type()

class ResultsWaitPage2(WaitPage):
	def is_displayed(self):
		return self.subsession.round_number == Constants.num_rounds

	def after_all_players_arrive(self):
		self.group.set_payoffs()
		self.group.place()
  
class Results(Page):
	def is_displayed(self):
		return self.subsession.round_number == Constants.num_rounds

	def vars_for_template(self):
		return {'p1_payoff': self.group.get_player_by_id(1).payoff,
				'p2_payoff': self.group.get_player_by_id(2).payoff,
				'1_x_place': self.group.place()[0][0],
				'1_y_place': self.group.place()[0][1],
				'2_x_place': self.group.place()[1][0],
				'2_y_place': self.group.place()[1][1],
				}

page_sequence = [
	ChoiceGame,
	ResultsWaitPage0,
	ChoiceOne,
	ChoiceTwoWaitPage,
	LocationGame2,
    LocationGame,
    ResultsWaitPage1,
    ResultsWaitPage2,
    Results
]

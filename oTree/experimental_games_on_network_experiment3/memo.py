points_matrix = {}
        nghb_num = [0 for i in range(players_per_group)]
        nghb = [0 for i in range(players_per_group)]
        payoff = [0 for i in range(players_per_group)]
        
        for i in range(players_per_group):  
            nghb[i] = network[i+1]
            for k in range(len(nghb)):
                if self.other_player()[nghb[k]].decision == "ACTIVE":
                    nghb_num += 1 
            payoff[i] = (100*nghb_num)/3
            
        for p in self.get_players():
            p.payoff = 200


            p = [i for i in range(players_per_group)]

        for i in range(players_per_group):
            p[i] = self.get_player_by_id(i+1)

        if players_per_group == 20:
            network = {1: [5], 2:[18], 3:[19], 4:[9, 13, 20], 5:[1, 4, 10], 6:[16], 7:[13, 16], 8:[4, 14], 9:[11], 10:[5], 11:[9, 17, 20], 12:[19], 13:[4, 7], 14:[8], 15:[16, 20], 16:[6, 15, 19], 17:[11, 18], 18:[2, 17], 19:[3, 12, 16], 20:[4, 11, 15]}
        elif players_per_group == 2:
            network = {1: [2], 2:[2]}
        else:
            network = {1: [2], 2:[2]}
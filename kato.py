round_num = 0
first_or_not = None

def tit_for_tat(my_history, opponent_history):
    global round_num
    global first_or_not
    p = 0
    
    if round_num == None and first_or_not == 1:
        first_or_not = 1
        
    if first_or_not == 1:
        round_num += 1
    
    if len(opponent_history)-1 == round_num:
        return 1
    elif len(opponent_history) < 1:
        return 0
    else:
        return opponent_history[-1]

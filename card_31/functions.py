def value(hand):
    hand_suit = []
    hand_value= []
    
    for i in range(3):
        hand_suit.append(hand[i].suit)
        hand_value.append(hand[i].value)
        
    if len(set(hand_suit)) == 3:
        return max(hand_value)
    
    if len(set(hand_suit)) == 2:
        if hand_suit[0] == hand_suit[1]:
            return max(hand_value[0] + hand_value[1], hand_value[2])
        elif hand_suit[0] == hand_suit[2]:
            return max(hand_value[0] + hand_value[2], hand_value[1])
        else:
            return max(hand_value[1] + hand_value[2], hand_value[0])
        
    return sum(hand_value)
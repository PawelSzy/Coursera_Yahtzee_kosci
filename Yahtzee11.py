"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_handequence = list(partial_sequence)
                new_handequence.append(item)
                temp_set.add(tuple(new_handequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """

    if hand == ():
        return 0

    if type(hand) is int:
        return hand
    
    unique_dices = set(hand)
    
    score = dict([(dummy_e,0) for dummy_e in unique_dices])
    
    for kostka in hand:
        score[kostka]+=kostka

    max_value = 0
    for dice in score:
        if score[dice] > max_value:
            max_value = score[dice]
    return max_value


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    #check if are free dices to roll
    if num_free_dice<=0 :
        return score(held_dice)
    
    #check if are held dices
    if held_dice == 0:
        held_dices = []
    else:
        held_dices = held_dice
    
    propability = 1./(num_die_sides**num_free_dice)
 
#    print "propability: ", propability
    
    #make a list of values of each side of the dice
    dices = [dice+1 for dice in range(num_die_sides)]
    
    #generate all sequences of evry posible dices
    sequences = gen_all_sequences(dices, num_free_dice)
    
    #give me expected value of roll
    #expected_value = sum(x1*P1+....xn*Pn)
    #xn = value of n sequence, P - probability of xn - random sequence
    expected_value = 0.0
    for seq in sequences:
        #compute the values of helded dices and all random sequence
        #use this values to compute expected value of rool
        dices_hand_and_seg = list(seq) + list(held_dices)
        expected_value+=score(dices_hand_and_seg)*propability
    
    #print sequences
    
#    print "expected_value ",expected_value

    return expected_value +0.0


def combinations(hand,all_holds):
    """
    Function compute all combinations of numbers in hand
    Function put combinations into all_holds set
     hand: full yahtzee hand 
    all_holds set - set to write combinations
    """
    
    if len(hand) <= 0:
        return
    
    all_holds.add(tuple(hand))
    
    for k_number in range(len(hand)):
        new_hand = list(hand)
        new_hand.pop(k_number)
        all_holds.add(tuple(new_hand))
        combinations(new_hand, all_holds)
    
    return all_holds


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
        
    all_holds = set([()])
    
    #write all possible combinations of hand into all_holds set    
    combinations(hand, all_holds)
    
    #print all_holds
    return all_holds




def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    #create all combinations of list
    combinations_list = gen_all_holds(hand)

    max_val = (expected_value(0,num_die_sides,len(hand)), ())
    
    #print max_val
    length_hand = len(hand)
    
    #find then hold of dices with the maximall expected value
    for hold_dices in combinations_list:
        exp_val = expected_value(hold_dices,num_die_sides, length_hand-len(hold_dices))
        if float(exp_val) > max_val[0]:
            max_val =(float(exp_val),hold_dices )
 
    
    return max_val


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 8
    hand = (4,4)
    
    hand_score = score(hand)
    
    print "score of hand", hand_score
    
    print"-----------expected value-------------"
    
    held_dice = [4,4] 
    num_die_sides = 6 
    num_free_dice= 5
    
    exp_value =  expected_value(held_dice, num_die_sides, num_free_dice)

    print "expected value:", exp_value
    
    print gen_all_holds(hand)
    
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

###
#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



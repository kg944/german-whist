import argparse
import random as r
from enum import Enum
from functools import cmp_to_key

# global vars
deck = []
player_cards = []
opponent_cards = []
trump_suit = None
broken = False # if trump suit has been broken yet
stage = 'BUILD'

# suit
class Suit(Enum):
    SPADE = 0
    HEART = 1
    CLUB = 2
    DIAMOND = 3
Suit = Enum('Suit', ['SPADE', 'HEART', 'CLUB', 'DIAMOND'])

"""
Ace = 1, Jack = 11, Queen = 12, King = 13
"""
def get_suit_unicode(suit):
    symbols = ['\u2664', '\u2661', '\u2667', '\u2662']
    return symbols[suit.value - 1]

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def get_val_string(self):
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return values[self.val - 1].rjust(2)

    def __str__(self):
        return f"{get_suit_unicode(self.suit)} {self.get_val_string()}"

    def __eq__(self, other):
        return self.suit == other.suit and self.val == other.val

    def __lt__(self, other):
        if self.suit == other.suit:
            return self.val < other.val
        elif self.suit == trump_suit:
            return False
        elif other.suit == trump_suit:
            return True
        else:
            return other.val < self.val

def deal_cards():
    for i in range(13):
        player_cards.append(deck.pop())
        opponent_cards.append(deck.pop())

# positive when c1 > c2
# if diff suit compare on suit 'value' otherwise card val
def visual_compare(c1, c2):
    if c1.suit != c2.suit:
        return c1.suit.value - c2.suit.value
    return c1.val - c2.val

def print_hand():
    global player_cards
    # custom sort for view order not value order
    player_cards = sorted(player_cards, key=cmp_to_key(lambda item1, item2: visual_compare(item1, item2)))
    for i in range(len(player_cards)):
        card = player_cards[i]
        print(f"{str(i)}:\t{str(card)}")
    print("")

def print_hand_2():
    global player_cards
    # custom sort for view order not value order
    player_cards = sorted(player_cards, key=cmp_to_key(lambda item1, item2: visual_compare(item1, item2)))
    print("")
    for i in range(len(player_cards)):
        card = player_cards[i]
        print(f"{str(card)}\t", end='')
    print("")
    # print indicies
    for j in range(len(player_cards)):
        print(f" {j}\t", end = '')
    print("")

# return a list of integers associated with the card index to play
def get_valid_indicies(hand, card_on_table = None):
    valid_indicies = []
    if not hand:
        return valid_indicies
    # valid starting moves are all suits except trump if unbroken, otherwise all suits
    if not card_on_table:
        for i in range(len(hand)):
            card = hand[i]
            if card.suit == trump_suit:
                if broken:
                    valid_indicies.append(i)
            else:
                valid_indicies.append(i)
    # a valid second move is following suit if hand contains it, otherwise any suit
    else:
        for i in range(len(hand)):
            card = hand[i]
            if card.suit == card_on_table.suit:
                valid_indicies.append(i)
        # if there were no cards of same suit as card_on_table
        if not valid_indicies:
            valid_indicies = [x for x in range(len(hand))]
    return valid_indicies


"""
1. create deck
2. shuffle deck
3. deal cards to players
"""
def start_game():
    for suit in list(Suit):
        for v in range(13):
            deck.append(Card(suit, v + 1))
    r.shuffle(deck)
    deal_cards()

def draw_card(card):
    print(f"\nCard on pile: {str(card)}")

def get_opponent_input(card = None):
    global opponent_cards
    valid_indicies = get_valid_indicies(opponent_cards, card)
    # for now just pick a random valid move
    index = r.randrange(len(valid_indicies))
    card_to_play = opponent_cards[valid_indicies[index]]
    opponent_cards = opponent_cards[0:index] + opponent_cards[index+1:]
    return card_to_play


def get_player_input(card = None):
    global player_cards
    print_hand_2()
    valid_indicies = get_valid_indicies(player_cards, card)
    selection = None
    # keep geting input until its valid
    while selection is None or selection not in valid_indicies:
        selection = int(input("choose a card:"))
    selected = player_cards[int(selection)]
    player_cards = player_cards[0:int(selection)] + player_cards[int(selection)+1:]
    return selected

# true if pc beats oc
def did_player_win(pc, oc, lead_suit):
    if pc.suit == oc.suit:
        return oc < pc
    elif pc.suit == trump_suit:
        return True
    elif oc.suit == trump_suit:
        return False
    # if suits differ and neither player trump suit
    else:
        if pc.suit == lead_suit:
            return True
    return False

# display a card
def display_card(card, draw_deck = False):
    if draw_deck:
        print("┌─────────┐┌─────────┐")
        print(f"│         ││ {get_suit_unicode(card.suit)}       │")
        print("│         ││         │")
        print("│         ││         │")
        print(f"│    {str(len(deck)).ljust(2)}   ││   {card.get_val_string()}    │")
        print("│         ││         │")
        print("│         ││         │")
        print(f"│         ││      {get_suit_unicode(card.suit)}  │")
        print("└─────────┘└─────────┘")
    else:
        print("┌─────────┐")
        print(f"│ {get_suit_unicode(card.suit)}       │")
        print("│         │")
        print("│         │")
        print(f"│   {card.get_val_string()}    │")
        print("│         │")
        print("│         │")
        print(f"│      {get_suit_unicode(card.suit)}  │")
        print("└─────────┘")



def main():
    parser = argparse.ArgumentParser(description='German whist, 2 or 1 player')
    #parser.add_argument('num_players', type=str, help='number of players')
    #parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')

    args = parser.parse_args()

    #if args.verbose:
    #print(f"{args.num_players}")

    won = False
    turn = 0 # 0 p0, 1 p1
    start_game()
    player_pts = 0
    global stage
    global deck
    global player_cards
    global opponent_cards
    global trump_suit
    global broken
    player_pts = 0
    opp_pts = 0
    while not won:
        """
        build round
        1. draw card
        2. get player / cpu input
        3. compare, add cards to hands
        """
        if stage == "BUILD":
            if deck:
                card = deck.pop()
                if not trump_suit:
                    trump_suit = card.suit
                print(f"trump: {get_suit_unicode(trump_suit)}")
                # get inputs
                if turn == 0:
                    display_card(card, True)
                    pc = get_player_input()
                    print(f"player played {str(pc)}")
                    oc = get_opponent_input(pc)
                    # print(f"opponent played {str(oc)}")
                    lead_suit = pc.suit
                else:
                    oc = get_opponent_input()
                    # print(f"opponent played {str(oc)}")
                    display_card(oc)
                    display_card(card, True)
                    pc = get_player_input(oc)
                    print(f"player played {str(pc)}")
                    lead_suit = oc.suit
                # if one of the players broke trump suit
                if (oc.suit == trump_suit or pc.suit == trump_suit) and not broken:
                    print("***********")
                    print("* BROKEN! *")
                    print("***********")
                    broken = True
                # get winner
                if did_player_win(pc, oc, lead_suit):
                    new_card = deck.pop()
                    print(f"player won {str(card)}")
                    # print(f"opp got {str(new_card)}") # debug
                    player_cards.append(card)
                    opponent_cards.append(new_card)
                    turn = 0
                else:
                    new_card = deck.pop()
                    print(f"player got {str(new_card)}")
                    opponent_cards.append(card)
                    # print(f"opp won {str(card)}") # debug
                    player_cards.append(new_card)
                    turn = 1
            else:
                stage = 'BATTLE'
        else:
            """
            battle round
            0. check if game over
            1. first player picks a card
            2. card is shown
            3. other player decides
            4. cards distributed and points awarded
            """
            # if game is over
            if not player_cards or not opponent_cards:
                print(f"player points: {player_pts}")
                print(f"opponent points: {opp_pts}")
                exit()
            if turn == 0:
                pc = get_player_input()
                print(f"player played {str(pc)}")
                oc = get_opponent_input(pc)
                print(f"opponent played {str(oc)}")
                lead_suit = pc.suit
            else:
                oc = get_opponent_input()
                display_card(oc, True)
                pc = get_player_input(oc)
                print(f"player played {str(pc)}")
                lead_suit = oc.suit
            # if one of the players broke trump suit
            if (oc.suit == trump_suit or pc.suit == trump_suit) and not broken:
                print("***************************")
                print("* BROKEN in battle round! *")
                print("***************************")
                broken = True
            # get winner
            if did_player_win(pc, oc, lead_suit):
                print("player won a point")
                turn = 0
                player_pts += 1
                # print(f"opp got {str(new_card)}") # debug
            else:
                print("opponent won a point")
                turn = 1
                opp_pts += 1
                # print(f"opp won {str(card)}") # debug


if __name__ == '__main__':
    main()

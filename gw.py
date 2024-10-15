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
class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def __str__(self):
        symbols = ['\u2664', '\u2661', '\u2667', '\u2662']
        values = ['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return f"{values[self.val]}{symbols[self.suit.value - 1]}"

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
    for card in player_cards:
        print(f"{str(card)}")
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
    card_to_play = opponent_cards[index]
    opponent_cards = opponent_cards[0:index] + opponent_cards[index+1:]
    return card_to_play


def get_player_input(card = None):
    print_hand()
    selection = input()
    global player_cards
    selected = player_cards[int(selection)]
    player_cards = player_cards[0:int(selection)] + player_cards[int(selection)+1:]
    return selected

def did_player_win(pc, oc):
    return oc < pc

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
    while not won:
        """
        build round
        1. draw card
        2. get player / cpu input
        3. compare, add cards to hands
        battle round
        1. first player picks a card
        2. card is shown
        3. other player decides
        4. cards distributed and points awarded
        """
        if stage == "BUILD":
            if deck:
                card = deck.pop()
                print(card.val)
                print(card.suit)
                if not trump_suit:
                    trump_suit = card.suit
                    print(f"trump suit is {trump_suit.name}S")
                draw_card(card)
                # get inputs
                if turn == 0:
                    pc = get_player_input()
                    print(f"player played {str(pc)}")
                    oc = get_opponent_input(pc)
                    print(f"opponent played {str(oc)}")
                else:
                    oc = get_opponent_card()
                    print(f"opponent played {str(oc)}")
                    pc = get_player_input(oc)
                    print(f"player played {str(pc)}")
                # get winner
                if did_player_win(pc, oc):
                    new_card = deck.pop()
                    print(f"player won {str(card)}")
                    print(f"opp got {str(new_card)}")
                    player_cards.append(card)
                    opponent_cards.append(new_card)
                else:
                    new_card = deck.pop()
                    print(f"player got {str(new_card)}")
                    opponent_cards.append(card)
                    print(f"opp won {str(card)}")
                    player_cards.append(new_card)
            else:
                stage = 'BATTLE'
                print("implement battle !!!")
                exit()
        else:
            exit()


if __name__ == '__main__':
    main()

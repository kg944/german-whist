import unittest

import gw

class TestGw(unittest.TestCase):
    def test_0(self):
        self.assertEqual(1, 1)

    def test_get_valid_indicies_card_on_table_match(self):
        # arrange
        card_on_table = gw.Card(gw.Suit.SPADE, 2)
        gw.trump_suit = gw.Suit.HEART
        cards = [
            gw.Card(gw.Suit.DIAMOND, 3),
            gw.Card(gw.Suit.DIAMOND, 4),
            gw.Card(gw.Suit.SPADE, 3),
            gw.Card(gw.Suit.SPADE, 4),
            gw.Card(gw.Suit.SPADE, 5),
            gw.Card(gw.Suit.SPADE, 10),
            gw.Card(gw.Suit.HEART, 3),
            gw.Card(gw.Suit.HEART, 4),
            gw.Card(gw.Suit.HEART, 10)
        ]
        expected = [2, 3, 4, 5]
        # act
        actual = gw.get_valid_indicies(cards, card_on_table)
        # assert
        self.assertEqual(actual, expected)


    def test_get_valid_indicies_card_on_table_no_match(self):
        # arrange
        card_on_table = gw.Card(gw.Suit.CLUB, 2)
        gw.trump_suit = gw.Suit.HEART
        cards = [
            gw.Card(gw.Suit.DIAMOND, 3),
            gw.Card(gw.Suit.DIAMOND, 4),
            gw.Card(gw.Suit.SPADE, 3),
            gw.Card(gw.Suit.SPADE, 4),
            gw.Card(gw.Suit.SPADE, 5),
            gw.Card(gw.Suit.SPADE, 10),
            gw.Card(gw.Suit.HEART, 3),
            gw.Card(gw.Suit.HEART, 4),
            gw.Card(gw.Suit.HEART, 10)
        ]
        # no matching to card on table so we can play any card
        expected = [i for i in range(len(cards))]
        # act
        actual = gw.get_valid_indicies(cards, card_on_table)
        # assert
        self.assertEqual(actual, expected)
    
    def test_get_valid_indicies_no_card_on_table_unbroken(self):
        # arrange
        gw.trump_suit = gw.Suit.HEART
        gw.broken = False
        cards = [
            gw.Card(gw.Suit.DIAMOND, 3),
            gw.Card(gw.Suit.DIAMOND, 4),
            gw.Card(gw.Suit.SPADE, 3),
            gw.Card(gw.Suit.SPADE, 4),
            gw.Card(gw.Suit.SPADE, 5),
            gw.Card(gw.Suit.SPADE, 10),
            gw.Card(gw.Suit.HEART, 3),
            gw.Card(gw.Suit.HEART, 4),
            gw.Card(gw.Suit.HEART, 10)
        ]
        expected = [0, 1, 2, 3, 4, 5]
        # act
        actual = gw.get_valid_indicies(cards)
        # assert
        self.assertEqual(actual, expected)

    def test_get_valid_indicies_no_card_on_table_broken(self):
        # arrange
        gw.trump_suit = gw.Suit.HEART
        gw.broken = True
        cards = [
            gw.Card(gw.Suit.DIAMOND, 3),
            gw.Card(gw.Suit.DIAMOND, 4),
            gw.Card(gw.Suit.SPADE, 3),
            gw.Card(gw.Suit.SPADE, 4),
            gw.Card(gw.Suit.SPADE, 5),
            gw.Card(gw.Suit.SPADE, 10),
            gw.Card(gw.Suit.HEART, 3),
            gw.Card(gw.Suit.HEART, 4),
            gw.Card(gw.Suit.HEART, 10)
        ]
        expected = [i for i in range(len(cards))]
        # act
        actual = gw.get_valid_indicies(cards)
        # assert
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()

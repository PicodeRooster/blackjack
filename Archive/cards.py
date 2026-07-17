import random

cards = {
    "SUITS" : [":heart_suit:", ":spade_suit:", ":diamond_suit:", ":club_suit:"],
    # (display rank, blackjack value) — one entry per card, so 13 per suit.
    # Ace starts at 11; get_hand_total downgrades it to 1 when the hand would bust.
    "RANKS" : [
        ("Ace", 11),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("10", 10),
        ("Jack", 10),
        ("Queen", 10),
        ("King", 10),
    ]
}

deck = []
for suit in cards["SUITS"]:
    for rank, value in cards["RANKS"]:
        deck.append({"suit": suit, "rank": rank, "value": value})

random.shuffle(deck)
shuffled_deck = deck
# Example usage to for display: print(shuffled_deck[0]['rank']) //Returns "Ace", for example

'''
class Deck:
    def __init__(self, cards):
        self.cards = {
            "SUITS" : [":heart_suit:", ":spade_suit:", ":diamond_suit:", ":club_suit:"],
            # (display rank, blackjack value) — one entry per card, so 13 per suit.
            # Ace starts at 11; get_hand_total downgrades it to 1 when the hand would bust.
            "RANKS" : [
            ("Ace", 11),
            ("2", 2),
            ("3", 3),
            ("4", 4),
            ("5", 5),
            ("6", 6),
            ("7", 7),
            ("8", 8),
            ("9", 9),
            ("10", 10),
            ("Jack", 10),
            ("Queen", 10),
            ("King", 10),
        ]
    }
    
    def build_deck(self): 
        deck = []
        for suit in cards["SUITS"]:
            for rank, value in cards["RANKS"]:
                deck.append({"suit": suit, "rank": rank, "value": value})
        
        random.shuffle(deck)
        return deck

                
'''
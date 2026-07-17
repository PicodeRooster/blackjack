import random

cards = {
    "SUITS" : [":heart_suit:", ":spade_suit:", ":diamond_suit:", ":club_suit:"],
    "VALUES" : {
        1: "Ace",
        2 : "2",
        3 : "3",
        4 : "4",
        5 : "5",
        6 : "6",
        7 : "7",
        8 : "8",
        9 : "9",
        10: "10",
        11: "Ace",
        "Jack": "10",
        "Queen": "10", 
        "King" : "10"
    }
}

deck = []
for suit in cards["SUITS"]:
    for key, value in cards["VALUES"].items():
        if key == (1, 11):
            deck.append({"suit": suit, "rank": value, "value": key})
        elif isinstance(key, tuple):
            for name in key:
                deck.append({"suit": suit, "rank": name, "value": value})
        else:
            deck.append({"suit": suit, "rank": value, "value": key})

random.shuffle(deck)
shuffled_deck = deck
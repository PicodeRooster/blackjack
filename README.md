```
playing_cards = {
    "SUITS" : [":heart_suit:", ":spade_suit:", ":diamond_suit:", ":club_suit:"],
    "VALUES" : {
        (1, 11): "Ace",
        2 : "2",
        3 : "3",
        4 : "4",
        5 : "5",
        6 : "6",
        7 : "7",
        8 : "8",
        9 : "9",
        10: "10",
        ("Jack", "Queen", "King") : "10"
    }
}
```
Changed bcz was easier c/o tuples

### Refactor
While working through this project, I made a couple of changes worth explaining. First, I was mistaken about how a real deck works in Blackjack — I originally built two separate 52-card decks, one for the dealer and one for the player, assuming each side draws from their own pile. Turns out real Blackjack uses a single shared deck (or "shoe") that both dealer and player draw from, so I refactored the code to reflect that: there's now just one deck list that both participants pop cards from. Second, this project is also where I learned how to use classes for the first time. The dealer and player were originally separate dictionaries with a lot of duplicated structure, held together by loose functions that took a dict as an argument and reached into its keys. I'm in the process of converting them into a Participant base class (with a Player subclass for the extra wallet/betting fields), so that shared behavior lives in one place instead of being copy-pasted across dealer/player logic. The original version of this file, before these changes, has been moved to the /Archive folder for reference.
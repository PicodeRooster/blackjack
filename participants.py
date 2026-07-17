from cards import shuffled_deck

class Participant:
    def __init__(self, deck):
        self.deck = deck
        self.current_hand = {}
        self.rounds_won = 0
            
    def deal_new_cards(self):
        card_count = len(self.current_hand) + 1
        self.current_hand[f"card {card_count}"] = self.deck.pop()
    
    def deal_new_hand(target):
        if target == "dealer".strip():
            dealer_hand = {
                "card 1": shuffled_deck.pop(),
                "card 2": shuffled_deck.pop()
            }

        if target == "player".strip():
            player_hand = {
                "card 1": shuffled_deck.pop(),
                "card 2": shuffled_deck.pop()
            }

        return target 
        
    def get_hand_total(self):
        total = 0
        ace_count = 0

        for card in self.current_hand.values():
            rank = card["rank"]  # this is the display string, e.g. "Ace", "10", "7"

            if rank == "Ace":
                total += 11
                ace_count += 1
            elif rank == "10":
                total += 10  # covers 10, Jack, Queen, King — they all share rank "10"
            else:
                total += int(rank)  # "2".."9" convert cleanly to ints

        # Downgrade Aces from 11 to 1, one at a time, if we're busting
        while total > 21 and ace_count > 0:
            total -= 10  # 11 -> 1 is a difference of 10
            ace_count -= 1

        return total

class Player(Participant):
    def __init__(self, deck, wallet=5000):
        super().__init__(deck)
        self.wallet = wallet
        self.current_bet = 0

class Dealer(Participant):
    def must_hit(self, hand_total):
        return hand_total < 17
    
dealer = Dealer(shuffled_deck)
player = Player(shuffled_deck)    
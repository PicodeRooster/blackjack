from Archive.cards import shuffled_deck

class Participant:
    def __init__(self, deck):
        self.deck = deck
        self.current_hand = {}
        self.rounds_won = 0
            
    def deal_new_cards(self):
        card_count = len(self.current_hand) + 1
        self.current_hand[f"card {card_count}"] = self.deck.pop()
    
    def deal_new_hand(self):
        self.current_hand = {
            "card 1": self.deck.pop(),
            "card 2": self.deck.pop()
        }
        
    def get_hand_total(self):
        total = 0
        ace_count = 0

        for card in self.current_hand.values():
            total += card["value"]  # numeric value: Ace=11, face cards=10
            if card["value"] == 11:
                ace_count += 1

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

shoe = playing_cards.build_deck()

dealer = Dealer(shoe)
player = Player(shoe)    
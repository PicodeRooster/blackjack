from rich import print
import random
import sys

chips_display = f"[bold white][5] [10] [25] [50][/bold white] [bold blue][100] [200] [300][/bold blue] [bold red][400] [500][/bold red]"
game_options_display = ["SPLIT", "DOUBLE", "DEAL", "BET", "STAND", "QUIT"]

class Cards:
    def __init__(self):
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
        for suit in self.cards["SUITS"]:
            for rank, value in self.cards["RANKS"]:
                deck.append({"suit": suit, "rank": rank, "value": value})
        
        random.shuffle(deck)
        return deck

playing_cards = Cards()

class Participant:
    def __init__(self, deck):
        self.deck = deck
        # A hand is a list of card dicts. A participant holds a LIST of hands
        # so the player can split into more than one. active_hand indexes the
        # hand currently being played.
        self.hands = [[]]
        self.active_hand = 0
        self.rounds_won = 0

    @property
    def current_hand(self):
        return self.hands[self.active_hand]

    def deal_card(self, hand=None):
        # Add one card to a hand (a "hit"). Defaults to the active hand.
        (self.current_hand if hand is None else hand).append(self.deck.pop())

    def deal_new_hand(self):
        # Reset to a single fresh 2-card hand.
        self.hands = [[self.deck.pop(), self.deck.pop()]]
        self.active_hand = 0
        return self.current_hand

    def get_hand_total(self, hand=None):
        # Works on any hand; defaults to the active one.
        hand = self.current_hand if hand is None else hand

        total = sum(card["value"] for card in hand)  # Ace=11, face cards=10
        ace_count = sum(1 for card in hand if card["value"] == 11)

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
        self.bets = [0]  # one bet per hand, index-aligned with self.hands

    def can_split(self):
        hand = self.current_hand
        return (len(self.hands) < 4                       # cap total splits
                and len(hand) == 2
                and hand[0]["value"] == hand[1]["value"]  # value, so 10/J/Q/K pairs count
                and self.wallet >= self.current_bet)      # can afford the 2nd bet

    def split(self):
        if not self.can_split():
            return False

        self.wallet -= self.current_bet          # match the bet on the new hand

        hand = self.hands[self.active_hand]
        new_hand = [hand.pop()]                   # move the 2nd card to a new hand

        hand.append(self.deck.pop())              # deal one fresh card to each
        new_hand.append(self.deck.pop())

        self.hands.insert(self.active_hand + 1, new_hand)
        self.bets.insert(self.active_hand + 1, self.current_bet)
        return True

class Dealer(Participant):
    def must_hit(self, hand_total):
        return hand_total < 17

#Note: The word "shoe" is a casino term. It just means "the shared deck between the dealer and the player in Blackjack"
shoe = playing_cards.build_deck()
dealer = Dealer(shoe)
player = Player(shoe)

#Quit the game any time get_input(prompt) is used
def exit_game():
    print('Thanks for playing!')
    sys.exit()
 
def get_input(prompt):
    value = input(prompt)
    if value.strip().upper() == "QUIT":
        exit_game()
    return value

#Prompt for a bet amount between 0 and 500, and no more than the wallet holds.
def input_bet():
    while True:
        try:
            print(chips_display)
            amount = int(get_input('Input your amount: '))
            
            if amount < 0 or amount > 500:
                print("Amount must be between 0 and 500!")
                continue
            
            if amount > player.wallet:
                print(f"You don't have enough for {amount}!")
                print(f"Current funds: {player.wallet}")
                continue

            return amount
        
        except ValueError:
            print("That's not a valid number!")
            continue           

def ask_yes_no(prompt):
    #Keep asking until the user gives a valid Y/N answer, then return 'y' or 'n'.
    while True:
        answer = get_input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer
        print("Please input Y or N in upper or lowercase.")

def player_economy_ui():
    print("---")
    print(f"Current bet: {player.current_bet}")
    print(f"Wallet: {player.wallet}")

def pregame():
    print("Welcome to Blackjack!", ":slot_machine:")
    print("To begin, place your bet.", ":money-mouth_face:")

    player.current_bet = input_bet()
    player.wallet -= player.current_bet
    player_economy_ui()

    # Ask about modifying the bet first, then whether to start.
    # Keep looping until the player starts the game or the wallet is empty.
    while player.wallet > 0:
        print(chips_display)
        if ask_yes_no('Would you like to modify the bet? [Y/N] ') == "y":
            # add the new amount on top of the current bet, and take that extra out of the wallet
            added = input_bet()
            player.current_bet += added
            player.wallet -= added
            player_economy_ui()

        if ask_yes_no('Start game? [Y/N] ') == "y":
            break

    return player.wallet

def render_hand(hand):
    return ", ".join(f"{card['suit']}{card['rank']}" for card in hand)

def start_of_round():
    up = dealer.current_hand[1]  # dealer's face-up card
    print("---")
    print("Dealer's hand:")
    print(f"[bold red]???[/bold red], {up['suit']}{up['rank']}")

    print("---")
    print("Your hand:")
    print(render_hand(player.current_hand))

    player_economy_ui()

    print("---")
    print("[bold green][BET][/bold green] [bold cyan][DEAL][/bold cyan] [bold #ff8700][STAND][/bold #ff8700] [bold #d70087][DOUBLE][/bold #d70087] [bold red1][QUIT][bold red1]")

def play_current_hand():
    i = player.active_hand
    while True:
        hand = player.current_hand
        total = player.get_hand_total(hand)
        label = f"Hand {i + 1}" if len(player.hands) > 1 else "Your hand"
        print(f"{label}: {render_hand(hand)}  (total {total})")

        if total >= 21:
            print("21! :fire:" if total == 21 else "Bust! :collision:")
            return

        options = ["HIT", "STAND"]
        if player.can_split():
            options.append("SPLIT")
        if len(hand) == 2 and player.wallet >= player.bets[i]:
            options.append("DOUBLE")

        choice = get_input(f"[{' / '.join(options)}] ").strip().upper()

        if choice == "HIT":
            player.deal_card()
        elif choice == "STAND":
            return
        elif choice == "SPLIT" and "SPLIT" in options:
            player.split()
            print("Split! You're now playing two hands.")
            player_economy_ui()
        elif choice == "DOUBLE" and "DOUBLE" in options:
            player.wallet -= player.bets[i]
            player.bets[i] *= 2
            player.deal_card()
            print(f"Doubled to {player.bets[i]} — one card only.")
            print(f"{label}: {render_hand(player.current_hand)}  (total {player.get_hand_total()})")
            return
        else:
            print("Not a valid option.")

def dealer_turn():
    print("---")
    print(f"Dealer's hand: {render_hand(dealer.current_hand)}  (total {dealer.get_hand_total()})")
    while dealer.must_hit(dealer.get_hand_total()):
        dealer.deal_card()
        print(f"Dealer hits: {render_hand(dealer.current_hand)}  (total {dealer.get_hand_total()})")

def settle():
    dealer_total = dealer.get_hand_total()
    print("---")
    for i, hand in enumerate(player.hands):
        bet = player.bets[i]
        player_total = player.get_hand_total(hand)
        label = f"Hand {i + 1}" if len(player.hands) > 1 else "Your hand"

        if player_total > 21:
            print(f"{label}: bust — lose {bet}")  # stake already removed from wallet
        elif dealer_total > 21 or player_total > dealer_total:
            player.wallet += bet * 2               # return stake + winnings
            player.rounds_won += 1
            print(f"[green]{label}: win {bet}[/green]")
        elif player_total == dealer_total:
            player.wallet += bet                   # push — refund the stake
            print(f"{label}: push")
        else:
            print(f"[red]{label}: lose {bet}[/red]")

def game():
    pregame()

    player.deal_new_hand()
    player.bets = [player.current_bet]
    dealer.deal_new_hand()

    start_of_round()

    # Player turn — iterate every hand. A split inserts a new hand at active_hand+1,
    # so the while-over-length naturally picks it up.
    player.active_hand = 0
    while player.active_hand < len(player.hands):
        play_current_hand()
        player.active_hand += 1

    dealer_turn()
    settle()
    player_economy_ui()

if __name__ == "__main__":
    game()

'''    
    check values for player
    if card 1 and card 2 have the same 'value', show SPLIT option
    if get_hand_total(player) < 21, show game_options_display
    if get_hand_total(player) == 21, BLACKJACK
    if STAND and get_hand_total(player) < 21:
        if must_hit(dealer, get_hand_total(dealer)) == FALSE
            deal new card for dealer until at least 17 True
        if player hand total > 21:
            BUST, dealer wins
            remove chips from wallet
        if dealer hand total > 21:
            player wins
            add chips to wallet
        if dealer hand total > player hand total:
            dealer wins round
            remove chips from wallet
        if dealer hand total < player hand total:
            player winds round
            add chips to wallet
        if dealer hand total == player hand total:
            PUSH
            end round
            do nothing

    


One usage note: call it as player.deal_new_hand() and dealer.deal_new_hand() at the start of a round — not deal_new_cards() for the first deal, since deal_new_hand resets current_hand to a fresh 2-card hand, while deal_new_cards assumes a hand already exists and adds one card to it (for hits).


def confirm_initial_bet(wallet, amount):
    player_economy_ui
    print(chips)

    while True:
        try:
            answer = ask_yes_no('Would you like to modify the bet? [Y/N] ')
            if ask_yes_no('Start game? [Y/N] ') == "y":
                amount = input_bet(wallet)

            player.wallet = wallet - amount
            player_economy_ui()
            
            else:
                ask_yes_no('Would you like to modify the bet? [Y/N] ')
                print(chips)
                break
        else:
        

        except:
'''            